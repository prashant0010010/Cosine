import streamlit as st
from modules.text_cleaner import clean_text
from modules.bert_analyzer import (
    get_sentence_embeddings,
    compute_semantic_density,
    compute_cosine_similarity
)

st.title("Analyze Article")

st.markdown("""
Understand how well your article aligns with a target topic using **AI-powered semantic analysis**.

This tool evaluates:

• [Semantic Density](#pages/2_Semantic_Density.py) – how information-rich your article is  
• Cosine Similarity – how closely your article matches the target topic
""")

article_text = st.text_area("Paste Article", height=200)
target_text = st.text_input("Target Keyword / Topic")

if st.button("Analyze Article"):

    if not article_text.strip() or not target_text.strip():
        st.warning("Please enter both article and target topic.")
    else:

        article_clean = clean_text(article_text)
        target_clean = clean_text(target_text)

        _, embeddings = get_sentence_embeddings(article_clean)

        density = compute_semantic_density(embeddings)
        similarity = compute_cosine_similarity(article_clean, target_clean)

        st.success("Analysis Complete")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Semantic Density", f"{density:.3f}")

            if st.button("Learn about Semantic Density"):
                st.switch_page("pages/2_Semantic_Density.py")

        with col2:
            st.metric("Cosine Similarity", f"{similarity:.3f}")

            if st.button("Learn about Cosine Similarity"):
                st.switch_page("pages/3_Cosine_Similarity.py")

st.markdown("---")

st.markdown("""
### Why This Matters for SEO

Modern search engines analyze **meaning and context**, not just keywords.

Semantic analysis helps determine:

- topical authority
- content depth
- relevance to user intent
""")