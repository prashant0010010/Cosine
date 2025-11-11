import streamlit as st
import matplotlib.pyplot as plt
import io
from PIL import Image

from modules.text_cleaner import clean_text
from modules.bert_analyzer import (
    get_sentence_embeddings,
    compute_semantic_density,
    compute_cosine_similarity,
    analyze_sentences,
    add_to_niche_memory,
    load_niche_memory,
    clear_niche_memory,
)
from modules.seo_report import (
    generate_simple_summary,
    save_report_as_pdf,
    generate_report,
)
from modules.readability_analyzer import analyze_readability


# --- Streamlit UI ---
st.set_page_config(page_title="Semantic Density & SEO Tool", layout="wide")
st.title("🔍 Semantic Density & SEO Analyzer")

# --- Inputs ---
article_text = st.text_area("Paste Article:", height=200)
target_text = st.text_area("Target SEO Topic / Competitor Text:", height=150)

# --- Define functions (same logic as Tkinter version) ---
def generate_and_save_report_gui():
    if not article_text.strip() or not target_text.strip():
        st.warning("Please enter both article and target topic.")
        return

    # Run analysis
    sentence_results = analyze_sentences(article_text, target_text)
    _, embeddings = get_sentence_embeddings(clean_text(article_text))
    density = compute_semantic_density(embeddings)
    similarity = compute_cosine_similarity(article_text, target_text)

    # Create summary
    summary = generate_simple_summary(sentence_results, density, similarity)

    # Generate horizontal bar chart
    sentences = [(s if len(s) <= 80 else s[:77] + "...") for s, _, _ in sentence_results]
    scores = [sc for _, sc, _ in sentence_results]

    if not scores:
        st.warning("No sentences found to plot.")
        return

    fig, ax = plt.subplots(figsize=(8, max(3, len(scores) * 0.3)))
    ax.barh(range(len(scores)), scores, align='center')
    ax.set_yticks(range(len(scores)))
    ax.set_yticklabels(sentences)
    ax.set_xlabel("Cosine Similarity")
    ax.set_title("Sentence Similarity Scores")
    ax.set_xlim(0, 1)
    plt.tight_layout()

    chart_path = "sentence_similarity.png"
    plt.savefig(chart_path)
    st.pyplot(fig)
    plt.close()

    title_input = st.text_input("Enter the article title:", "Untitled Article")

    st.subheader("🧾 SEO Summary")
    st.text(summary)

    if st.button("Save SEO Report as PDF"):
        save_report_as_pdf(summary, "SEO_Report.pdf", article_title=title_input, chart_path=chart_path)
        st.success("SEO Report saved as SEO_Report.pdf")


def analyze_article():
    if not article_text.strip() or not target_text.strip():
        st.warning("Please enter both article and target topic.")
        return

    article_clean = clean_text(article_text)
    target_clean = clean_text(target_text)

    _, embeddings = get_sentence_embeddings(article_clean)
    density = compute_semantic_density(embeddings)
    similarity = compute_cosine_similarity(article_clean, target_clean)

    niche_embeddings = load_niche_memory()
    niche_sim = "N/A"
    if niche_embeddings:
        niche_sim = compute_cosine_similarity(article_clean, " ".join([str(e) for e in niche_embeddings]))

    st.write(f"**Semantic Density:** {density:.4f}")
    st.write(f"**Cosine Similarity to target:** {similarity:.4f}")
    st.write(f"**Similarity with niche memory:** {niche_sim}")


def add_to_memory():
    if not article_text.strip():
        st.warning("Please enter article text before adding to memory.")
        return
    add_to_niche_memory(article_text)
    st.success("Article added to niche memory!")


def clear_memory():
    clear_niche_memory()
    st.success("Niche memory cleared!")


def generate_report_gui():
    if not article_text.strip() or not target_text.strip():
        st.warning("Please enter both article and target topic.")
        return

    sentence_results = analyze_sentences(article_text, target_text)
    _, embeddings = get_sentence_embeddings(clean_text(article_text))
    density = compute_semantic_density(embeddings)
    similarity = compute_cosine_similarity(article_text, target_text)

    img_bytes, summary_text = generate_report(sentence_results, density, similarity)

    st.subheader("📊 SEO Report Summary")
    st.text(summary_text)

    img = Image.open(io.BytesIO(img_bytes.read()))
    st.image(img, caption="Sentence Similarity Chart")


def analyze_sentences_gui():
    if not article_text.strip() or not target_text.strip():
        st.warning("Please enter both article and target topic.")
        return

    sentence_results = analyze_sentences(article_text, target_text)

    st.subheader("Sentence-Level Semantic Analysis")
    for i, (sentence, similarity, is_weak) in enumerate(sentence_results, 1):
        status = "⚠️ Weak" if is_weak else "✅ Strong"
        st.write(f"**{i}. ({similarity:.3f}) {status}**\n{sentence}\n")


def analyze_readability_gui():
    if not article_text.strip():
        st.warning("Please enter the article text.")
        return

    report = analyze_readability(article_text)
    st.subheader("🧠 Readability Report")
    st.text(report)


# --- Buttons ---
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Analyze Article"):
        analyze_article()

with col2:
    if st.button("Add Article to Niche Memory"):
        add_to_memory()

with col3:
    if st.button("Clear Niche Memory"):
        clear_memory()

st.markdown("---")

col4, col5, col6 = st.columns(3)

with col4:
    if st.button("Analyze Sentences"):
        analyze_sentences_gui()

with col5:
    if st.button("Generate SEO Report"):
        generate_report_gui()

with col6:
    if st.button("Generate & Save SEO Report"):
        generate_and_save_report_gui()

st.markdown("---")

if st.button("Analyze Readability"):
    analyze_readability_gui()
