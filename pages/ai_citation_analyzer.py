import streamlit as st
import requests
from bs4 import BeautifulSoup
from serpapi import GoogleSearch
import spacy

from modules.text_cleaner import clean_text
from modules.bert_analyzer import (
    compute_cosine_similarity,
    analyze_sentences,
    get_sentence_embeddings,
    compute_semantic_density
)


st.markdown("""
<meta name="title" content="AI Citation Readiness Analyzer – Check If Your Content Is AI Search Ready">
<meta name="description" content="Analyze how ready your article is for AI search engines and generative engines using semantic density, topic alignment, SERP similarity, sentence strength and entity coverage.">
""", unsafe_allow_html=True)
# -------------------------
# LOAD SPACY MODEL
# -------------------------

@st.cache_resource
def load_model():
    return spacy.load("en_core_web_sm")

nlp = load_model()


# -------------------------
# PAGE TITLE
# -------------------------

st.title("AI Citation Readiness Analyzer")
st.text("AI Citation Readiness Analyzer")

st.markdown("""
This analyzer evaluates how ready your article is for **AI search engines and generative engines**.

It combines multiple signals:

• Semantic Density  
• Topic Alignment  
• Sentence Strength  
• SERP Alignment  
• Entity Coverage  

The result is a **Citation Readiness Score**.
""")


# -------------------------
# INPUT
# -------------------------

article_text = st.text_area("Paste Article", height=260)

target_keyword = st.text_input("Target Keyword")

analyze = st.button("Analyze AI Citation Readiness")


# -------------------------
# HELPER FUNCTIONS
# -------------------------

def get_google_results(query):

    params = {
        "engine": "google",
        "q": query,
        "num": 5,
        "api_key": st.secrets.get("SERPAPI_KEY")
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    links = []

    for item in results.get("organic_results", []):
        links.append(item["link"])

    return links


def extract_page_text(url):

    try:
        headers = {"User-Agent": "Mozilla/5.0"}

        r = requests.get(url, headers=headers, timeout=10)

        soup = BeautifulSoup(r.text, "html.parser")

        paragraphs = soup.find_all("p")

        text = " ".join([p.get_text() for p in paragraphs])

        return text

    except:
        return ""


# -------------------------
# ANALYSIS
# -------------------------

if analyze:

    if not article_text.strip() or not target_keyword.strip():
        st.warning("Please enter article and keyword.")
        st.stop()

    with st.spinner("Analyzing article..."):

        article_clean = clean_text(article_text)

        # -------------------------
        # SEMANTIC DENSITY
        # -------------------------

        sentences, embeddings = get_sentence_embeddings(article_clean)

        semantic_density = compute_semantic_density(embeddings)

        semantic_signal = min(semantic_density * 25, 25)


        # -------------------------
        # COSINE SIMILARITY
        # -------------------------

        topic_alignment = compute_cosine_similarity(article_clean, target_keyword)

        topic_signal = topic_alignment * 20


        # -------------------------
        # SENTENCE ANALYZER
        # -------------------------

        sentence_results = analyze_sentences(article_clean, target_keyword)

        strong = [s for s in sentence_results if not s[2] and s[1] >= 0.71]
        moderate = [s for s in sentence_results if not s[2] and 0.41 <= s[1] < 0.71]
        weak = [s for s in sentence_results if s[2]]

        if len(sentence_results) > 0:
            sentence_signal = (len(strong) / len(sentence_results)) * 15
        else:
            sentence_signal = 0


        # -------------------------
        # SERP ANALYZER
        # -------------------------

        serp_links = get_google_results(target_keyword)

        serp_scores = []

        for url in serp_links:

            page_text = extract_page_text(url)

            if not page_text:
                continue

            page_clean = clean_text(page_text)

            sim = compute_cosine_similarity(article_clean, page_clean)

            serp_scores.append(sim)

        if serp_scores:
            serp_similarity = sum(serp_scores) / len(serp_scores)
        else:
            serp_similarity = 0

        serp_signal = serp_similarity * 20


        # -------------------------
        # ENTITY ANALYSIS
        # -------------------------

        doc = nlp(article_text)

        entities = [ent.text for ent in doc.ents if len(ent.text) > 2]

        entity_count = len(entities)

        entity_signal = min((entity_count / 25) * 20, 20)


        # -------------------------
        # FINAL SCORE
        # -------------------------

        raw_score = (
            semantic_signal +
            topic_signal +
            sentence_signal +
            serp_signal +
            entity_signal
        )

        citation_score = float(round((raw_score / 100) * 100, 2))


    # -------------------------
    # OUTPUT
    # -------------------------

    st.divider()

    st.subheader("AI Citation Readiness Score")

    st.metric("Citation Score", f"{citation_score}%")

    st.progress(float(citation_score) / 100)

    if citation_score >= 80:
        st.success("Excellent — highly citation ready.")
    elif citation_score >= 60:
        st.warning("Moderate — improvements recommended.")
    else:
        st.error("Low — article needs stronger semantic coverage.")


    # -------------------------
    # SIGNAL BREAKDOWN
    # -------------------------

    st.subheader("Signal Breakdown")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Semantic Density", f"{semantic_density:.3f}")
        st.metric("Topic Alignment", f"{topic_alignment:.3f}")

    with col2:
        st.metric("SERP Alignment", f"{serp_similarity:.3f}")
        st.metric("Sentence Strength", len(strong))

    with col3:
        st.metric("Entities Found", entity_count)
        st.metric("Weak Sentences", len(weak))


    # -------------------------
    # SENTENCE DETAILS
    # -------------------------

    with st.expander("Sentence Analysis"):

        for sent, score, is_weak in sentence_results:

            if score >= 0.71:
                st.success(f"{score:.2f} — {sent}")
            elif score >= 0.41:
                st.warning(f"{score:.2f} — {sent}")
            else:
                st.error(f"{score:.2f} — {sent}")


    # -------------------------
    # ENTITY DISPLAY
    # -------------------------

    with st.expander("Detected Entities"):

        if not entities:
            st.info("No entities detected.")
        else:
            for e in entities:
                st.write("•", e)


    # -------------------------
    # EXPLANATION
    # -------------------------
st.divider()

st.header("Why This Tool Exists")

st.markdown("""
Traditional SEO tools mainly focus on **keywords and backlinks**.

However, modern search engines increasingly rely on **semantic understanding** and contextual relationships between ideas.

Content may fail to rank or appear in AI-generated answers because it lacks:

• semantic cohesion  
• contextual depth  
• entity coverage  
• topical alignment  

The AI Citation Readiness Analyzer was designed to evaluate these deeper signals.
""")
with st.expander("How This Score Works"):

        st.markdown("""
AI Citation Readiness estimates how well your article aligns with signals used by modern AI search engines.

Signals analyzed:

Semantic Density — topical cohesion  
Topic Alignment — relevance to keyword  
Sentence Strength — semantic clarity  
SERP Alignment — similarity to ranking pages  
Entity Coverage — contextual authority

Higher scores indicate stronger potential for **AI citation and semantic authority**.
""")
st.markdown("""
### Evaluate How Ready Your Content Is for AI Search Engines

Modern search engines and generative AI systems evaluate content using **semantic signals**, not just keywords.

This analyzer measures whether your article has the **semantic structure, topical depth, and contextual signals** required for AI systems to understand and cite your content.

The tool analyzes five critical signals:

• Semantic Density  
• Topic Alignment  
• Sentence Strength  
• SERP Alignment  
• Entity Coverage  

These signals combine to generate a **Citation Readiness Score** that estimates how well your content aligns with modern AI search systems.
""")
st.header("How the AI Citation Analyzer Works")

st.markdown("""
The analyzer processes your article through several semantic analysis stages.

### Step 1 — Content Cleaning
The article is normalized by removing noise and formatting inconsistencies.

### Step 2 — Sentence Embedding
Each sentence is converted into a semantic embedding using transformer models.

### Step 3 — Semantic Signal Calculation
Multiple signals are measured:

• semantic density  
• topic alignment  
• sentence strength  
• SERP similarity  
• entity detection

### Step 4 — Citation Readiness Score
All signals are combined into a final score indicating how well the content aligns with AI search systems.
""")
st.header("Frequently Asked Questions")

with st.expander("What is AI citation readiness?"):
    st.write("""
AI citation readiness refers to how well a piece of content aligns with signals that generative AI systems use when selecting sources to reference or summarize.
""")

with st.expander("Why does semantic density matter?"):
    st.write("""
Semantic density measures topical cohesion. Articles with strong semantic density maintain consistent focus on a central topic and related concepts.
""")

with st.expander("Why compare content with SERP results?"):
    st.write("""
SERP comparison helps determine whether your article covers the same topics and concepts as high-ranking pages.
""")

with st.expander("Why are entities important in SEO?"):
    st.write("""
Entities help search engines understand relationships between concepts. Articles containing relevant entities often demonstrate stronger contextual authority.
""")

with st.expander("Can this tool guarantee AI citation?"):
    st.write("""
No tool can guarantee citations, but improving semantic signals increases the likelihood that AI systems understand and reference your content.
""")
    
st.markdown("---")

st.subheader("⚙ Legacy Tool (Version 1.0)")

st.markdown("""
The original analyzer is still available for advanced workflows.

It includes:

• niche memory system  
• sentence analysis  
• full SEO PDF reports  
• experimental features
""")

if st.button("Open Version 1 Analyzer"):
    st.switch_page("main.py")