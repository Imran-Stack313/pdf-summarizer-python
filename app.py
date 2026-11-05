import streamlit as st
import PyPDF2

st.title("PDF Summarizer")
st.write("Upload PDF and get short summary")

uploaded_file = st.file_uploader("Choose PDF", type="pdf")

if uploaded_file:
    reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()

    st.write("Total Characters:", len(text))
    st.write("Preview:")
    st.write(text[:2000])
    st.success("PDF Read Successfully! AI Summary feature coming soon.")
