# app.py
import sys, os, json, ast
import pandas as pd
import streamlit as st
import pysqlite3
sys.modules["sqlite3"] = pysqlite3

# ──────────────────────────────────────────────────────────────────────────────
# Allow absolute imports of your packages
PROJECT_ROOT = r"/mount/src/personalized_education/"
sys.path.insert(0, PROJECT_ROOT)

from Creating_Section_Params.schema import NextSectionChoice, ALLOWED_KG_NODES
from Creating_Section_Text.pipeline import ingest_and_build_store, run_one
from Creating_Student_Params_From_Json.pipeline import run_profile_generation_pipeline
# ──────────────────────────────────────────────────────────────────────────────

STUDENT_CSV = "Streamlit_UI/data/langchain_student_params_50_streamlit_testing_with_rollnos.csv"

# Initialize vector store once per session
@st.cache_resource
def init_vector_store():
    ingest_and_build_store()

def load_student_df(path: str) -> pd.DataFrame:
    return pd.read_csv(path)

def save_student_df(path: str, df: pd.DataFrame):
    df.to_csv(path, index=False)

def parse_row_to_params(row: pd.Series) -> dict:
    d = row.to_dict()
    # Normalize last_section to list
    raw = d.get("last_section", "")
    if isinstance(raw, str):
        try:
            d["last_section"] = json.loads(raw)
        except:
            d["last_section"] = ast.literal_eval(raw)
    if not isinstance(d["last_section"], list):
        d["last_section"] = [d["last_section"]]
    # Normalize knowledge_graph_nodes_covered
    kg = d.get("knowledge_graph_nodes_covered", [])
    if isinstance(kg, str):
        try:
            d["knowledge_graph_nodes_covered"] = json.loads(kg)
        except:
            d["knowledge_graph_nodes_covered"] = ast.literal_eval(kg)
    return d

def generate_next_section(params: dict) -> NextSectionChoice:
    from Creating_Section_Params.schema import StudentParameters
    from Creating_Section_Params.prompt_builder import prompt, output_parser, SECTIONS
    from Creating_Section_Params.model_loader import get_llm

    student_json = json.dumps(params, indent=2)
    schema_json = StudentParameters.model_json_schema()
    chain = prompt | get_llm() | output_parser
    return chain.invoke({
        "student_json": student_json,
        "student_schema_json": schema_json,
        "sections": SECTIONS,
    })

# Streamlit app setup
st.set_page_config(page_title="Adaptive Tutor", layout="centered")
st.title("Personalized Next-Section Tutor")

init_vector_store()

# Load or refresh profiles cache
def get_profiles():
    return load_student_df(STUDENT_CSV)

df = get_profiles()

# Roll No input
roll_no = st.text_input("Enter Roll No:")
selected = None
if roll_no:
    mask = df['Roll_No'].astype(str) == roll_no
    if mask.any():
        selected = int(df.index[mask][0])
    else:
        with st.spinner(f"Generating profile for Roll No {roll_no}…"):
            new_profile = run_profile_generation_pipeline(roll_no=roll_no)
            new_profile = new_profile.model_dump() if hasattr(new_profile, 'model_dump') else new_profile
            new_profile['Roll_No'] = roll_no
            df2 = load_student_df(STUDENT_CSV)
            df2 = pd.concat([df2, pd.DataFrame([new_profile])], ignore_index=True)
            save_student_df(STUDENT_CSV, df2)
            selected = df2.index[-1]
            df = df2

# Proceed only when a profile is loaded or generated
if selected is not None:
    # Initialize prev state
    if "prev_index" not in st.session_state:
        st.session_state.prev_index = selected
        st.session_state.prev_last_section = parse_row_to_params(df.iloc[selected])["last_section"]

    # Profile change handling
    if selected != st.session_state.prev_index:
        # Save the most recently generated section before switching
        if "choice" in st.session_state and st.session_state.choice:
            st.session_state.prev_last_section.append(st.session_state.choice.section_name)
        # Persist history for old profile
        df_latest = load_student_df(STUDENT_CSV)
        df_latest.at[
            st.session_state.prev_index, "last_section"
        ] = json.dumps(st.session_state.prev_last_section)
        save_student_df(STUDENT_CSV, df_latest)
        # Reset for new profile
        st.session_state.prev_index = selected
        st.session_state.prev_last_section = parse_row_to_params(df.iloc[selected])["last_section"]
        st.session_state.choice = None
        st.session_state.content = None

    # Display profile
    student_params = parse_row_to_params(df.iloc[selected])
    st.subheader(f"Profile (Roll No {roll_no})")
    st.json(student_params)

    # Determine next section
    if "choice" not in st.session_state or not st.session_state.choice:
        with st.spinner("Determining best next section…"):
            st.session_state.choice = generate_next_section(student_params)

    # Render content
    if "content" not in st.session_state or not st.session_state.content:
        with st.spinner(f"Generating “{st.session_state.choice.section_name}”…"):
            st.session_state.content = run_one(
                student_params["ongoing_concept"],
                st.session_state.choice
            )

    section_name = st.session_state.choice.section_name
    st.markdown(f"### Next Section: **{section_name}**")
    st.write(st.session_state.content)

    # Next button
    if st.button("Next"):
        df2 = load_student_df(STUDENT_CSV)
        # Rollover
        if section_name == "What-if Scenarios":
            old_concept = student_params["ongoing_concept"]
            idx = ALLOWED_KG_NODES.index(old_concept)
            new_concept = ALLOWED_KG_NODES[idx+1] if idx+1 < len(ALLOWED_KG_NODES) else old_concept
            covered = student_params.get("knowledge_graph_nodes_covered", [])
            covered.append(old_concept)
            df2.at[selected, "knowledge_graph_nodes_covered"] = json.dumps(covered)
            df2.at[selected, "ongoing_concept"] = new_concept
            df2.at[selected, "last_section"] = json.dumps([])
            st.session_state.prev_last_section = []
            st.success(f"{old_concept} completed. Moving on to next concept: {new_concept}")
        else:
            secs = st.session_state.prev_last_section.copy()
            secs.append(section_name)
            df2.at[selected, "last_section"] = json.dumps(secs)
            st.session_state.prev_last_section = secs
        save_student_df(STUDENT_CSV, df2)
        st.session_state.choice = None
        st.session_state.content = None
        st.rerun()
