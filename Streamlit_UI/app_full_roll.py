import sys, os, json, ast
import pandas as pd
import streamlit as st
import time
from gtts import gTTS
import tempfile
import base64
import pysqlite3
sys.modules["sqlite3"] = pysqlite3

# ──────────────────────────────────────────────────────────────────────────────
# Allow absolute imports of your packages
PROJECT_ROOT = r"/mount/src/personalized_education/"
sys.path.insert(0, PROJECT_ROOT)

# ──────────────────────────────────────────────────────────────────────────────
# Page config + theme overrides
st.set_page_config(
    page_title="🌟 Adaptive Tutor for Kids",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ──────────────────────────────────────────────────────────────────────────────
# Replace your existing CSS block with this one
st.markdown("""
<style>
  /* Global background & text */
  html, body, .stApp, .block-container {
    background-color: #fffbf0 !important;  /* gentle lavender */
    color: #2C3E50 !important;             /* dark slate for readability */
  }

  /* Make all <label> text dark so form labels show up */
  label, .stSidebar label {
    color: #2C3E50 !important;
    font-weight: 500;
  }

  /* Input placeholders */
  input::placeholder,
  textarea::placeholder {
    color: #555555 !important;
    opacity: 1 !important;
  }

  /* Dark sidebar background & light text */
  [data-testid="stSidebar"] {
    background-color: #2C3E50 !important;  /* dark slate */
    color: #ECF0F1 !important;             /* off-white for contrast */
  }
  [data-testid="stSidebar"] label,
  [data-testid="stSidebar"] .stTextInput,
  [data-testid="stSidebar"] .stSelectbox,
  [data-testid="stSidebar"] a {
    color: #ECF0F1 !important;
  }

  /* Main title */
  .big-title {
    font-size: 2.5rem;
    color: #6C3483 !important;  /* deep purple */
    text-align: center;
    margin-bottom: 1rem;
  }

  /* Section cards */
  .section-card {
    background: #E0CEE0;               /* soft mauve */
    border: 2px solid #C39BD3;         /* muted purple border */
    border-radius: 16px;
    padding: 20px;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    margin-bottom: 16px;
  }
  .section-card h2 {
    color: #4A235A !important;         /* richer purple */
    margin: 0 0 0.5rem;
  }

  /* Chat bubbles */
  .chat-container {
    display: flex;
    align-items: flex-start;
    margin-bottom: 1rem;
  }
  .chat-bubble {
    background: #E9D6F2;               /* pale lavender */
    color: #2C3E50 !important;
    border: 1px solid #C39BD3;
    border-radius: 16px;
    padding: 12px;
    box-shadow: 1px 1px 6px rgba(0,0,0,0.1);
    font-family: 'Comic Sans MS', cursive, sans-serif;
  }

  /* Buttons */
  .stButton > button {
    background-color: #8E44AD !important;  /* bold purple */
    color: #FFFFFF !important;
    font-weight: bold;
    border: none;
    border-radius: 12px;
    padding: 0.6rem 1.2rem;
    transition: background-color 0.2s ease;
  }
  .stButton > button:hover {
    background-color: #71368A !important;  /* darker on hover */
  }

  /* Inputs and selects */
  input,
  .stTextInput > div > div > input,
  .stSelectbox > div > div > div > select {
    border: 2px solid #C39BD3 !important;
    border-radius: 8px !important;
    padding: 0.4rem !important;
    color: #2C3E50 !important;
    background-color: #FFFFFF !important;
  }

  /* Ensure balloons float above everything */
  .stApp .stBalloon {
    z-index: 9999 !important;
  }

  /* Info box override for visibility */
  [data-testid="stAlert"] {
    background-color: #EAF7FF !important;       /* light blue background */
    color: #2C3E50 !important;                  /* dark slate text */
    border-left: 4px solid #4A90E2 !important;  /* accent border */
  }
/* Ensure the “Please type your roll number to begin!” info box has dark text */
  [data-testid="stAlert"], /* covers st.warning, st.error, st.success, st.info */
  [data-testid="stInfo"] { 
    background-color: #EAF7FF !important;   /* light blue bg */
    color: #2C3E50 !important;              /* dark slate text */
    border-left: 4px solid #4A90E2 !important;
  }
  /* Force all inner text and icon to be dark */
  [data-testid="stAlert"] *,
  [data-testid="stInfo"] * {
    color: #2C3E50 !important;
    fill:  #2C3E50 !important;  /* for SVG icon */
  }
  [data-testid="stForm"] .stButton > button {
  background-color: #8E44AD !important;
  color: #FFFFFF !important;
  font-weight: bold;
  border: none;
  border-radius: 12px;
  padding: 0.6rem 1.2rem;
  transition: background-color 0.2s ease;
}
[data-testid="stForm"] .stButton > button:hover {
  background-color: #71368A !important;
}
</style>
""", unsafe_allow_html=True)


def mascot_says(text: str):
    url = mascots[selected_mascot]
    st.markdown(f"""
    <div class="chat-container">
      <img src="{url}" style="width:64px; height:64px; margin-right:8px; border-radius:8px;" />
      <div class="chat-bubble">{text}</div>
    </div>
    """, unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────

from Creating_Section_Params.schema import NextSectionChoice, ALLOWED_KG_NODES
from Creating_Section_Text.pipeline import ingest_and_build_store, run_one
from Creating_Student_Params_From_Json.pipeline import run_profile_generation_pipeline

STUDENT_CSV = "Streamlit_UI/data/langchain_student_params_50_streamlit_testing_with_rollnos.csv"

# Initialize vector store once per session
@st.cache_resource
def init_vector_store():
    return ingest_and_build_store()

# Data utilities
def load_student_df(path: str) -> pd.DataFrame:
    return pd.read_csv(path)

def save_student_df(path: str, df: pd.DataFrame):
    df.to_csv(path, index=False)

# Normalize row data
def parse_row_to_params(row: pd.Series) -> dict:
    d = row.to_dict()
    raw = d.get("last_section", "")
    if isinstance(raw, str):
        try:
            d["last_section"] = json.loads(raw)
        except:
            d["last_section"] = ast.literal_eval(raw)
    if not isinstance(d["last_section"], list):
        d["last_section"] = [d["last_section"]]
    kg = d.get("knowledge_graph_nodes_covered", [])
    if isinstance(kg, str):
        try:
            d["knowledge_graph_nodes_covered"] = json.loads(kg)
        except:
            d["knowledge_graph_nodes_covered"] = ast.literal_eval(kg)
    return d

# Next section generator
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

# ──────────────────────────────────────────────────────────────────────────────
# Input + sidebar
roll_no = st.text_input("Enter your Roll No:")

mascots = {
    "Wise Owl": "https://cdn-icons-png.flaticon.com/512/3529/3529365.png",
    "Fun Robot": "https://cdn-icons-png.flaticon.com/512/909/909877.png",
    "Magic Unicorn": "https://cdn-icons-png.flaticon.com/512/4584/4584502.png",
    "Gritty": "https://i.imgur.com/3HnZwB7.jpeg"
}
selected_mascot = st.sidebar.selectbox("Choose your mascot:", list(mascots.keys()))
st.sidebar.image(mascots[selected_mascot], width=128)

with st.sidebar:
    st.title("📚 Menu")
    app_mode = st.radio("Go to:", ["Home", "Progress"])
    st.markdown("---")
# Early exit if no roll_no on Home
if app_mode == "Home" and not roll_no:
    st.markdown("<div class='big-title'>Welcome to Adaptive Tutor! 🌈</div>", unsafe_allow_html=True)
    st.info("Please type your roll number to begin! 😊")
    st.stop()

# Load/init data & vector store
init_vector_store()
df = load_student_df(STUDENT_CSV)
mask = df['Roll_No'].astype(str) == roll_no
selected_idx = int(df.index[mask][0]) if mask.any() else None

# If switching roll_no: persist previous last_section
if 'prev_idx' in st.session_state and selected_idx is not None and selected_idx != st.session_state.prev_idx:
    df_prev = load_student_df(STUDENT_CSV)
    df_prev.at[st.session_state.prev_idx, 'last_section'] = json.dumps(st.session_state.prev_last_section)
    save_student_df(STUDENT_CSV, df_prev)
    for k in ['choice', 'content']:
        st.session_state.pop(k, None)
    st.session_state.concept_started = False
    st.session_state.prev_idx = selected_idx
    st.session_state.prev_last_section = []

# Profile creation if missing
if selected_idx is None and roll_no:
    with st.spinner(f"Creating magical profile for Roll No: {roll_no}… ✨"):
        new_profile = run_profile_generation_pipeline(roll_no=roll_no)
        new_profile = new_profile.model_dump() if hasattr(new_profile, 'model_dump') else new_profile
        new_profile['Roll_No'] = roll_no
        df = pd.concat([df, pd.DataFrame([new_profile])], ignore_index=True)
        save_student_df(STUDENT_CSV, df)
        selected_idx = df.index[-1]

# Stop if still no profile
if selected_idx is None:
    st.stop()

if app_mode == "Home" and selected_idx is not None:
    # if they’ve already submitted once, skip the form:
    if not st.session_state.get("concept_started", False):
        with st.form("choose_concept_form"):
            chosen = st.selectbox(
                "📖 Which concept would you like to start studying with today?",
                ALLOWED_KG_NODES,
                key="concept_choice"
            )
            start = st.form_submit_button("Start Learning 🚀")

        # until they hit that button, stop here:
        if not start:
            st.stop()

        # once they do:
        current = df.at[selected_idx, 'ongoing_concept']
        if chosen != current:
            df.at[selected_idx, 'ongoing_concept'] = chosen
            df.at[selected_idx, 'last_section']      = json.dumps([])
            save_student_df(STUDENT_CSV, df)

        # mark that we can proceed:
        st.session_state.concept_started = True
        # fresh run so parse student_params below with updated CSV
        st.rerun()
# ─────────────────────────────────────────────────────────────────────────

# Parse params and init prev state
student_params = parse_row_to_params(df.iloc[selected_idx])
if 'prev_idx' not in st.session_state:
    st.session_state.prev_idx = selected_idx
    st.session_state.prev_last_section = student_params.get('last_section', []).copy()

# My Profile + Next Section view
if app_mode in ["Home"]:
    # st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.subheader(f"📝 Profile (Roll No: {roll_no})")
    # st.write(f"**Concept Clarity:** {student_params['conceptual_clarity_level']} / 5")
    # st.write(f"**Attention Span:** {student_params['attention_span_category']} / 3")
    st.write(f"**Covered Concepts:** {', '.join(student_params.get('knowledge_graph_nodes_covered', []))}")
    st.write(f"**Ongoing Concept:** {student_params['ongoing_concept']}")
    st.markdown("</div>", unsafe_allow_html=True)

    # ─── Remixed “next section” logic ────────────────────────────────────────────
    SEQUENCE = [
        "Concept Definition",
        "Explanation (with analogies)",
        "Details (facts, sub-concepts)",
        "Intuition",
        "Logical Flow",
        "Working",
        "Critical Thinking",
        "MCQs",
        "Real-Life Application",
        "What-if Scenarios"
    ]

    if 'choice' not in st.session_state:
        with st.spinner("Deciding your next fun section… 🤖"):
            # keep the original object
            choice = generate_next_section(student_params)

        # figure out what we ran last
        last_sections = student_params.get('last_section', [])
        last = last_sections[-1] if last_sections else None

        # compute the “next” name from SEQUENCE
        if last in SEQUENCE:
            idx = SEQUENCE.index(last)
            next_name = SEQUENCE[idx+1] if idx+1 < len(SEQUENCE) else SEQUENCE[-1]
        else:
            next_name = SEQUENCE[0]

        # override just the section_name field
        choice.section_name = next_name

        # store back into session
        st.session_state.choice = choice
    # ────────────────────────────────────────────────────────────────────────────────
    if 'content' not in st.session_state:
        with st.spinner(f"Preparing **{st.session_state.choice.section_name}** … 📖"):
            st.session_state.content = run_one(
                student_params['ongoing_concept'],
                st.session_state.choice
            )
    st.markdown(f"<div class='section-card'><h2>🎬 {st.session_state.choice.section_name}</h2></div>", unsafe_allow_html=True)
    st.write(st.session_state.content)

    
# … after you’ve set up your columns …
# … after you’ve set up your columns …
col_listen, col_next = st.columns([1, 4])

# 1) Generate audio only when the user clicks “Listen”
if col_listen.button("🔊 Listen", key="listen_btn"):
    with st.spinner("Generating audio… 🤖✨"):
        tts = gTTS(st.session_state.content, lang="en")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            tts.write_to_fp(tmp)
            st.session_state.audio_path = tmp.name
    st.session_state.show_audio = True

# 2) Once generated, display the audio player (no speed dropdown)
if st.session_state.get("show_audio") and st.session_state.get("audio_path"):
    audio_bytes = open(st.session_state.audio_path, "rb").read()
    st.audio(audio_bytes, format="audio/mp3")

# 3) Single Next Section button
if col_next.button("Next Section 🚀", key="next_section_btn"):
    # Clear any audio state so it resets on next section
    st.session_state.pop("audio_path", None)
    st.session_state.pop("show_audio", None)

    # … your existing “next section” logic …
    section_name = st.session_state.choice.section_name
    df2 = load_student_df(STUDENT_CSV)
    if section_name == "What-if Scenarios":
        old = student_params['ongoing_concept']
        idx = ALLOWED_KG_NODES.index(old)
        new_concept = ALLOWED_KG_NODES[idx+1] if idx+1 < len(ALLOWED_KG_NODES) else old
        covered = student_params.get('knowledge_graph_nodes_covered', []) + [old]
        df2.at[selected_idx, 'knowledge_graph_nodes_covered'] = json.dumps(covered)
        df2.at[selected_idx, 'ongoing_concept'] = new_concept
        df2.at[selected_idx, 'last_section'] = json.dumps([])
        st.balloons()
        time.sleep(1)
        mascot_says(f"Yay! You rocked '{old}' 🎉 Let's hop to '{new_concept}' next! 🌟")
        st.session_state.prev_last_section = []
    else:
        st.session_state.prev_last_section.append(section_name)
        df2.at[selected_idx, 'last_section'] = json.dumps(st.session_state.prev_last_section)
        mascot_says(f"Fantastic! You finished '{section_name}'! 🏅")
    save_student_df(STUDENT_CSV, df2)
    for k in ['choice', 'content']:
        st.session_state.pop(k, None)
    st.rerun()

# Progress view
if app_mode == "Progress":
    total = len(ALLOWED_KG_NODES)
    done = len(student_params.get('knowledge_graph_nodes_covered', []))
    progress = int(done / total * 100)
    st.subheader("🎯 Learning Progress")
    st.progress(progress)
    st.write(f"You have completed **{done}** out of **{total}** concepts! Keep going! 🚀")
