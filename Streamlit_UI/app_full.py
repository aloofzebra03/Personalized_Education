# app.py
import sys, os, json
import pandas as pd
import streamlit as st
import ast

# ──────────────────────────────────────────────────────────────────────────────
# Make your project root visible so imports work
PROJECT_ROOT = r"C:/Users/aryan/Desktop/Personalized_Education/Personalized_Education"
sys.path.insert(0, PROJECT_ROOT)

from Creating_Section_Params.schema import NextSectionChoice
from Creating_Section_Text.pipeline import ingest_and_build_store, run_one
# ──────────────────────────────────────────────────────────────────────────────

# Path to your CSV of student params
STUDENT_CSV = "Streamlit_UI/data/langchain_student_params_50_streamlit_testing.csv"

# ──────────────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────────────

@st.cache_resource
def init_vector_store():
    """Ingest PDFs once per session."""
    ingest_and_build_store()

def load_student_df(path: str) -> pd.DataFrame:
    """Load the entire CSV fresh each run."""
    return pd.read_csv(path)

def parse_row_to_params(row: pd.Series) -> dict:
    d = row.to_dict()
    raw = d.get("last_section", "")

    if isinstance(raw, str):
        parsed = None
        # try proper JSON first
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            # fall back to Python literal eval (handles single-quotes)
            parsed = ast.literal_eval(raw)
        d["last_section"] = parsed
    return d

def save_student_df(path: str, df: pd.DataFrame):
    df.to_csv(path, index=False)

def generate_next_section(params: dict) -> NextSectionChoice:
    """Invoke your chain to pick the next section."""
    from Creating_Section_Params.schema import StudentParameters
    from Creating_Section_Params.prompt_builder import prompt, output_parser, SECTIONS
    from Creating_Section_Params.model_loader import get_llm

    student_json = json.dumps(params, indent=2)
    schema_json  = StudentParameters.model_json_schema()
    chain        = prompt | get_llm() | output_parser

    return chain.invoke({
        "student_json":        student_json,
        "student_schema_json": schema_json,
        "sections":            SECTIONS,
    })

# ──────────────────────────────────────────────────────────────────────────────
# Streamlit App
# ──────────────────────────────────────────────────────────────────────────────

st.set_page_config(page_title="Adaptive Tutor", layout="centered")
st.title("Personalized Next-Section Tutor")

# 1) Build vector store once
init_vector_store()

# 2) Load CSV & show dropdown
df = load_student_df(STUDENT_CSV)
selected = st.selectbox(
    "Select student row",
    df.index.tolist(),
    format_func=lambda i: f"Row {i}"
)

# 3) Ensure session_state keys exist
for key in ("prev_row", "prev_last_section", "choice", "content"):
    if key not in st.session_state:
        st.session_state[key] = None

# 4) If first load, just record row+last_section
if st.session_state.prev_row is None:
    st.session_state.prev_row         = selected
    st.session_state.prev_last_section = parse_row_to_params(df.iloc[selected])["last_section"]

# 5) If the user switched students, save the old profile and reset
elif selected != st.session_state.prev_row:
    if st.session_state.choice is not None and st.session_state.prev_last_section[-1] != st.session_state.choice.section_name:
        st.session_state.prev_last_section.append(
            st.session_state.choice.section_name
        )
    # write back the stored last_section of the previous student
    df.at[
        st.session_state.prev_row, "last_section"
    ] = json.dumps(st.session_state.prev_last_section)
    save_student_df(STUDENT_CSV, df)

    # clear old choice/content
    st.session_state.choice  = None
    st.session_state.content = None

    # update to the new student
    st.session_state.prev_row          = selected
    st.session_state.prev_last_section = parse_row_to_params(df.iloc[selected])["last_section"]

# 6) Load the current student’s params and display
student_params = parse_row_to_params(df.iloc[selected])
st.subheader(f"Profile (row {selected})")
st.json(student_params)

# 7) Auto-generate next section if needed
if st.session_state.choice is None:
    with st.spinner("Determining best next section…"):
        st.session_state.choice = generate_next_section(student_params)

# 8) Auto-fetch section text if needed
if st.session_state.choice and st.session_state.content is None:
    with st.spinner(f"Generating “{st.session_state.choice.section_name}”…"):
        st.session_state.content = run_one(
            student_params["ongoing_concept"],
            st.session_state.choice
        )

# 9) Display the next section & content
st.markdown(f"### Next Section: **{st.session_state.choice.section_name}**")
st.write(st.session_state.content)

# 10) “Next” button: append, save, and rerun
if st.button("Next"):
    # append to our in-memory list
    secs = st.session_state.prev_last_section
    secs.append(st.session_state.choice.section_name)

    # write back to CSV
    df2 = load_student_df(STUDENT_CSV)
    df2.at[selected, "last_section"] = json.dumps(secs)
    save_student_df(STUDENT_CSV, df2)

    # update session_state so next student-switch saves correctly
    st.session_state.prev_last_section = secs

    # reset and rerun to show the following section
    st.session_state.choice  = None
    st.session_state.content = None
    st.rerun()
