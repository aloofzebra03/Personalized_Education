# app.py
import sys, os, json, ast
import pandas as pd
import streamlit as st
import time

import pysqlite3
sys.modules["sqlite3"] = pysqlite3

# ──────────────────────────────────────────────────────────────────────────────
# Allow absolute imports of your packages
PROJECT_ROOT = r"/mount/src/personalized_education/"
sys.path.insert(0, PROJECT_ROOT)

from Creating_Section_Params.schema import NextSectionChoice, ALLOWED_KG_NODES
from Creating_Section_Text.pipeline   import ingest_and_build_store, run_one
# ──────────────────────────────────────────────────────────────────────────────

STUDENT_CSV = "Streamlit_UI/data/langchain_student_params_50_streamlit_testing.csv"

# ──────────────────────────────────────────────────────────────────────────────
@st.cache_resource
def init_vector_store():
    ingest_and_build_store()

def load_student_df(path: str) -> pd.DataFrame:
    return pd.read_csv(path)

def save_student_df(path: str, df: pd.DataFrame):
    df.to_csv(path, index=False)

def parse_row_to_params(row: pd.Series) -> dict:
    d = row.to_dict()
    # last_section as real list
    raw = d.get("last_section", "")
    if isinstance(raw, str):
        try:    d["last_section"] = json.loads(raw)
        except: d["last_section"] = ast.literal_eval(raw)
    if not isinstance(d["last_section"], list):
        d["last_section"] = [d["last_section"]]
    # knowledge_graph_nodes_covered
    kg = d.get("knowledge_graph_nodes_covered", [])
    if isinstance(kg, str):
        try:    d["knowledge_graph_nodes_covered"] = json.loads(kg)
        except: d["knowledge_graph_nodes_covered"] = ast.literal_eval(kg)
    return d

def generate_next_section(params: dict) -> NextSectionChoice:
    from Creating_Section_Params.schema        import StudentParameters
    from Creating_Section_Params.prompt_builder import prompt, output_parser, SECTIONS
    from Creating_Section_Params.model_loader  import get_llm

    student_json = json.dumps(params, indent=2)
    schema_json  = StudentParameters.model_json_schema()
    chain        = prompt | get_llm() | output_parser
    return chain.invoke({
        "student_json":        student_json,
        "student_schema_json": schema_json,
        "sections":            SECTIONS,
    })
# ──────────────────────────────────────────────────────────────────────────────

st.set_page_config(page_title="Adaptive Tutor", layout="centered")
st.title(" Personalized Next-Section Tutor")

init_vector_store()

# 1) Load CSV & let them pick a row
df       = load_student_df(STUDENT_CSV)
selected = st.selectbox("Select student row", df.index.tolist(), format_func=lambda i: f"Row {i}")

# 2) Persist the 'prev' state for last_section
if "prev_row" not in st.session_state:
    st.session_state.prev_row = selected
    st.session_state.prev_last_section = parse_row_to_params(df.iloc[selected])["last_section"]

# If they switch rows, write back any history & reset
if selected != st.session_state.prev_row:
    # save old student's last_section
    df_latest = load_student_df(STUDENT_CSV)
    df_latest.at[
        st.session_state.prev_row, "last_section"
    ] = json.dumps(st.session_state.prev_last_section)
    save_student_df(STUDENT_CSV, df_latest)

    # reset for new student
    st.session_state.prev_row          = selected
    st.session_state.prev_last_section = parse_row_to_params(df.iloc[selected])["last_section"]
    # clear any old LLM state
    st.session_state.choice  = None
    st.session_state.content = None

# 3) Load & show current profile
student_params = parse_row_to_params(df.iloc[selected])
st.subheader(f"Profile (row {selected})")
st.json(student_params)

# 4) Auto-generate the choice if missing
if "choice" not in st.session_state or st.session_state.choice is None:
    with st.spinner("Determining best next section…"):
        st.session_state.choice = generate_next_section(student_params)

# time.sleep(5)  # Give a moment for the spinner to show
# 5) Auto-fetch the section text if missing
if "content" not in st.session_state or st.session_state.content is None:
    with st.spinner(f"Generating “{st.session_state.choice.section_name}”…"):
        st.session_state.content = run_one(
            student_params["ongoing_concept"],
            st.session_state.choice
        )
# time.sleep(5)  # Give a moment for the spinner to show
# 6) Display
section_name = st.session_state.choice.section_name
st.markdown(f"### Next Section: **{section_name}**")
st.write(st.session_state.content)


# 7) NEXT button handles both rollover & normal append
if st.button("Next"):
    df2 = load_student_df(STUDENT_CSV)

    if section_name == "What-if Scenarios":
        # --- rollover into next concept ---
        old_concept = student_params["ongoing_concept"]
        idx         = ALLOWED_KG_NODES.index(old_concept)
        new_concept = ALLOWED_KG_NODES[idx+1] if idx+1 < len(ALLOWED_KG_NODES) else old_concept

        # append old_concept to covered
        covered = student_params.get("knowledge_graph_nodes_covered", [])
        covered.append(old_concept)

        # persist rollover
        df2.at[selected, "knowledge_graph_nodes_covered"] = json.dumps(covered)
        df2.at[selected, "ongoing_concept"]              = new_concept
        df2.at[selected, "last_section"]                = json.dumps([])  # clear history

        save_student_df(STUDENT_CSV, df2)

        # reset memory for new concept
        st.session_state.prev_last_section = []
        st.session_state.choice            = None
        st.session_state.content           = None

        st.success(f"{old_concept} completed! Moving on to the next concept: **{new_concept}**")

        st.rerun()

    else:
        # --- normal next-section append ---
        secs = st.session_state.prev_last_section
        secs.append(section_name)

        df2.at[selected, "last_section"] = json.dumps(secs)
        save_student_df(STUDENT_CSV, df2)

        st.session_state.prev_last_section = secs
        st.session_state.choice            = None
        st.session_state.content           = None

        st.rerun()
