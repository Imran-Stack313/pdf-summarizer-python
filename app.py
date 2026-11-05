def get_summary(text, num_sentences=6):
    text = clean_text(text)
    sentences = re.split(r'(?<=[.!?])\s+', text)
    # Sirf achhi wali lines lo - na bahut chhoti, na bahut badi
    sentences = [s.strip() for s in sentences if 40 < len(s.strip()) < 350]
    sentences = [s for s in sentences if s.count(' ') > 5]
    # Table / diagram wali gandi lines hatao
    bad = ['|', '→', '___', 'CHAPTER', 'Figure', 'Table', 'http', 'www.', '©', 'Page']
    sentences = [s for s in sentences if not any(b in s for b in bad)]
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
    summary = " ".join([s for _, s in top])
    return summary[:1200]  # Max 1200 characters hi dikhayega
