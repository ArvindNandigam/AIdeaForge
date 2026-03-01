import streamlit as st
from file_handler import extract_text
from pipeline import run_pipeline

st.set_page_config(layout="wide")
st.title("AIdeaForge - Multimodal AI Prototype")

mode = st.radio("Choose Input Type:", ["Manual Prompt", "Upload File"])

raw_text = None

if mode == "Manual Prompt":
    raw_text = st.text_area("Enter campus idea")

else:
    uploaded_file = st.file_uploader("Upload TXT or PDF", type=["txt", "pdf"])
    if uploaded_file:
        raw_text = extract_text(uploaded_file)

if st.button("Run AI Workflow") and raw_text:

    with st.spinner("Processing via HuggingFace API..."):
        result = run_pipeline(raw_text)

    st.subheader("Structured Extraction")
    st.code(result["structured"])

    st.subheader("Generated Event Plan")
    st.write(result["plan"])

    if result["image"]:
        st.subheader("Generated Poster")
        st.image(result["image"])