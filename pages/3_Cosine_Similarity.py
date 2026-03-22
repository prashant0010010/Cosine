import streamlit as st
from modules.text_cleaner import clean_text
from modules.bert_analyzer import compute_cosine_similarity

st.title("Cosine Similarity Analyzer")

st.markdown("""
### What is Cosine Similarity?

Cosine similarity measures **how close the meaning of two texts are**.

In SEO this helps determine:

• how well your article matches a target keyword  
• how similar your content is to competitor pages  
• how aligned your topic is with search intent
""")

article_text = st.text_area("Paste Article", height=200)
target_text = st.text_area("Target Keyword / Competitor Text", height=150)

if st.button("Calculate Similarity"):

    if not article_text.strip() or not target_text.strip():
        st.warning("Please enter both article and target topic.")
    else:

        article_clean = clean_text(article_text)
        target_clean = clean_text(target_text)

        similarity = compute_cosine_similarity(article_clean, target_clean)

        st.metric("Cosine Similarity", f"{similarity:.3f}")

        # Interpretation
        if similarity >= 0.76:
            st.success("""
        🟢 **High Topic Alignment**

        Your article strongly aligns with the target keyword or competitor content. This indicates strong topical relevance.
        """)

        elif similarity >= 0.51:
            st.warning("""
        🟡 **Moderate Topic Alignment**

        Your article partially matches the target topic but could improve semantic relevance by adding more related terms or deeper contextual coverage.
        """)

        else:
            st.error("""
        🔴 **Low Topic Alignment**

        The article meaning differs significantly from the target topic. Consider revising the content to better match the intended search query.
        """)

st.markdown("---")
st.markdown("### Cosine Similarity Interpretation")

st.progress(0.50)
st.markdown("""
🔴 **0.00 – 0.50 → Low relevance**

The article meaning differs significantly from the target topic.
""")

st.progress(0.75)
st.markdown("""
🟡 **0.51 – 0.75 → Moderate relevance**

The article partially matches the topic but could improve alignment.
""")

st.progress(1.0)
st.markdown("""
🟢 **0.76 – 1.00 → High relevance**

The article strongly aligns with the target keyword or competitor content.
""")
st.markdown("""
## Why Cosine Similarity Matters

Search engines increasingly evaluate **semantic similarity between queries and documents**.

Higher similarity often indicates:

• stronger keyword alignment  
• better topical relevance  
• improved ranking potential
""")
st.markdown("## Frequently Asked Questions")

with st.expander("What is cosine similarity?"):
    st.write("""
Cosine similarity is a mathematical method used to measure how similar two texts are.

It compares the direction of two vectors representing documents rather than their raw word counts.
""")

with st.expander("How are articles converted into vectors?"):
    st.write("""
Before calculating similarity, text must be converted into numerical vectors.

This can be done using methods such as TF-IDF, word counts, or modern embedding models.
""")

with st.expander("What preprocessing is required before calculating similarity?"):
    st.write("""
Text preprocessing typically involves removing stop words, cleaning punctuation, and normalizing vocabulary through stemming or lemmatization.
""")

with st.expander("What mathematical components are used in cosine similarity?"):
    st.write("""
Cosine similarity uses two key components: the dot product between vectors and the magnitude of each vector.

The final similarity score is calculated by dividing the dot product by the product of the vector magnitudes.
""")

with st.expander("Why is cosine similarity useful for SEO analysis?"):
    st.write("""
Cosine similarity helps determine whether an article aligns with a target keyword or topic.

Higher similarity usually indicates stronger topical relevance and better semantic alignment with search intent.
""")