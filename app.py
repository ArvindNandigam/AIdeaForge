import streamlit as st
from pipeline import run_pipeline

st.set_page_config(page_title="AIdeaForge", layout="wide")

st.title("AIdeaForge - Multimodal AI Prototype")

input_type = st.radio("Choose Input Type:", ["Manual Prompt", "Upload File"])

user_input = ""

if input_type == "Manual Prompt":
    user_input = st.text_area("Enter campus idea")

elif input_type == "Upload File":
    uploaded_file = st.file_uploader("Upload .txt file", type=["txt"])
    if uploaded_file:
        user_input = uploaded_file.read().decode("utf-8")

if st.button("Generate"):
    if user_input.strip() == "":
        st.warning("Please provide input.")
    else:
        with st.spinner("Generating AI outputs..."):
            result = run_pipeline(user_input)

        st.subheader("Structured Extraction")
        st.json(result["structured"])

        st.subheader("Generated Event Plan")
        st.write(result["plan"])

        st.subheader("Generated Poster")
        st.write("DEBUG IMAGE VALUE:", result["image"])
        st.image(result["image"])