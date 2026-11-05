import streamlit as st
import re
from collections import Counter
from PyPDF2 import PdfReader

st.title("PDF Summarizer")
st.write("Upload PDF and get short summary")

uploaded_file = st.file_uploader("Choose PDF", type="pdf")

def clean_text(text):
    return re.sub(r'\s+', ' ', text)

def get_summary(text, num_sentences=6):
    text = clean_text(text)
    sentences = re.split(r'(?<=[.!?])\s+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 30]
    if len(sentences) <= num_sentences:
        return " ".join(sentences)
    words = re.findall(r'\w+', text.lower())
    stopwords = set(['the','is','are','was','were','a','an','and','or','of','to','in','on','for','with','by','this','that','it','as','at','from','be','has','have','had','will','would','can','could','should','we','our','you','your','they','their','he','she','his','her','not','but','if','then','than','so','such'])
    words = [w for w in words if w not in stopwords and len(w) > 3]
    freq = Counter(words)
    scored = []
    for s in sentences:
        s_words = re.findall(r'\w+', s.lower())
        score = sum(freq.get(w, 0) for w in s_words)
        scored.append((score, s))
    scored.sort(reverse=True)
    top = sorted(scored[:num_sentences], key=lambda x: sentences.index(x[1]))
    return " ".join([s for _, s in top])

if uploaded_file is not None:
    reader = PdfReader(uploaded_file)
    full_text = ""
    for page in reader.pages:
        t = page.extract_text()
        if t:
            full_text += t + " "
    st.success(f"PDF Read Successfully! Total Characters: {len(full_text)}")
    with st.spinner("Summary bana raha hu..."):
        summary = get_summary(full_text, 6)
    st.subheader("📌 Summary")
    st.write(summary)
    with st.expander("Preview Full Text"):
        st.write(full_text[:5000])
