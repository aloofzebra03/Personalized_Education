import streamlit as st
# import json
# import sys

# PROJECT_ROOT = r"C:/Users/aryan/Desktop/Personalized_Education/Personalized_Education"
# sys.path.insert(0, PROJECT_ROOT)

# from Creating_Section_Params.schema import NextSectionChoice
# from Creating_Section_Text.pipeline import ingest_and_build_store, run_one

st.set_page_config(page_title="Adaptive Tutor", layout="centered")
st.title("Personalized Next-Section Tutor")

# Display profile placeholder
st.subheader("Your Profile")
st.write("<student_params.json contents here>")  # Placeholder for student params

# Display next-section placeholder
st.markdown("### Next Section: **<Section Name>**")
st.write("<Generated section content will appear here>")  # Placeholder for content

# Next button
if st.button("Next"):
    # Placeholder action
    st.write("Next button clicked! Parameters would update here.")
