import streamlit as st
from modules.text_cleaner import clean_text
from modules.bert_analyzer import (
    get_sentence_embeddings,
    compute_semantic_density
)

st.title(" Semantic Density Analyzer")

st.markdown("""
### What is Semantic Density?

Semantic density measures **how tightly connected the ideas in your article are**.

High semantic density means:

• sentences support the main topic  
• information is contextually connected  
• content is rich in meaningful relationships

Low density usually means the article drifts off-topic.
""")

article_text = st.text_area("Paste Article to Analyze", height=250)

if st.button("Calculate Semantic Density"):

    if not article_text.strip():
        st.warning("Please paste an article first.")
    else:

        article_clean = clean_text(article_text)
        _, embeddings = get_sentence_embeddings(article_clean)

        density = compute_semantic_density(embeddings)

        st.metric("Semantic Density", f"{density:.3f}")

        # Interpretation based on result
        if density >= 0.71:
            st.success("""
        🟢 **Strong Semantic Density**

        Your article shows strong topical cohesion. Most sentences are closely related to the main topic, indicating high informational relevance and structured semantic relationships.
        """)

        elif density >= 0.41:
            st.warning("""
        🟡 **Moderate Semantic Density**

        Your article is generally focused on the topic but some sentences may drift slightly off-topic or lack contextual depth.
        """)

        else:
            st.error("""
        🔴 **Weak Semantic Density**

        Your article may contain loosely connected ideas or insufficient contextual relationships. Consider improving topical focus and adding more related concepts.
        """)

st.markdown("---")
st.markdown("### Semantic Density Interpretation")

st.progress(0.40)
st.markdown("""
🔴 **0.00 – 0.40 → Weak**

Content may drift away from the topic or contain loosely connected ideas.
""")

st.progress(0.70)
st.markdown("""
🟡 **0.41 – 0.70 → Moderate**

Content stays mostly relevant but could improve topical depth.
""")

st.progress(1.0)
st.markdown("""
🟢 **0.71 – 1.00 → Strong**

Content demonstrates strong topical cohesion and semantic relationships.
""")
st.markdown("""
## How Semantic Density Helps SEO

Search engines analyze whether your content **stays focused on the topic**.

High semantic density can indicate:

• strong topical authority  
• deeper content coverage  
• better alignment with search intent

Well-structured content usually has higher semantic density.
""")

st.markdown("## Frequently Asked Questions")

with st.expander("What is semantic density?"):
    st.write("""
Semantic density refers to how much meaningful information is packed into a piece of text relative to its length.

Instead of focusing on keyword repetition, semantic density measures whether sentences carry contextually relevant ideas and concepts related to the main topic.
""")

with st.expander("How is semantic density analyzed in this tool?"):
    st.write("""
This tool estimates semantic density using sentence embeddings. Each sentence is converted into a semantic vector using transformer models.

The system then measures how closely sentences relate to each other. Higher similarity between sentences indicates stronger topical cohesion.
""")

with st.expander("What data is required to calculate semantic density?"):
    st.write("""
The analysis requires the article text and several preprocessing steps including cleaning, tokenization, and stop word removal.

After preprocessing, sentence embeddings are generated and compared to determine how strongly ideas are connected.
""")

with st.expander("What tools are commonly used for semantic analysis?"):
    st.write("""
Natural Language Processing libraries such as spaCy, NLTK, and Gensim are often used for semantic analysis.

These tools allow text to be converted into numerical vectors using methods like word embeddings.
""")

with st.expander("Why does semantic density matter for SEO?"):
    st.write("""
Search engines evaluate whether content remains focused on a specific topic.

Articles with higher semantic density often demonstrate stronger topical authority and clearer contextual relevance.
""")