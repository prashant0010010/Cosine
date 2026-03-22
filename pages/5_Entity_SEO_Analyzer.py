import streamlit as st
import spacy
from collections import Counter

st.title("Entity SEO Analyzer")

st.markdown("""
Entity analysis helps identify **important concepts inside your article**.

Modern search engines rely on **entities and their relationships** to understand topical depth and authority.

This tool extracts entities such as:

• People  
• Locations  
• Organizations  
• Products  
• Events  
• Concepts
""")

# -------- SAFE MODEL LOADER (DEPLOYMENT READY) --------
@st.cache_resource
def load_model():
    return spacy.load("en_core_web_sm")

nlp = load_model()

# -------- INPUT --------
article_text = st.text_area(
    "Paste Article",
    placeholder="Paste your article to extract entities and analyze semantic topical coverage.",
    height=260
)

# -------- BUTTON --------
if st.button("Analyze Entities"):

    if not article_text.strip():
        st.warning("Please paste an article first.")
        st.stop()

    doc = nlp(article_text)

    # -------- ENTITY EXTRACTION --------
    entities = [(ent.text.strip(), ent.label_) for ent in doc.ents if len(ent.text.strip()) > 2]

    if not entities:
        st.error("No entities detected. Try using richer content.")
        st.stop()

    entity_counts = Counter(entities)

    st.subheader("Detected Entities")

    for (entity, label), count in entity_counts.most_common():
        st.markdown(
            f"<span style='background:#262730;padding:6px 10px;border-radius:10px;margin:4px;display:inline-block'>"
            f"<b>{entity}</b> ({label}) — {count}x</span>",
            unsafe_allow_html=True
        )

    st.markdown("---")

    # -------- METRICS --------
    total_mentions = sum(entity_counts.values())
    unique_entities = len(entity_counts)
    total_words = len(article_text.split())

    entity_density = total_mentions / total_words
    entity_diversity = unique_entities / total_mentions

    col1, col2 = st.columns(2)

    col1.metric("Total Entity Mentions", total_mentions)
    col1.metric("Entity Density", f"{entity_density:.3f}")

    col2.metric("Unique Entities", unique_entities)
    col2.metric("Entity Diversity", f"{entity_diversity:.3f}")

    st.progress(min(entity_density * 4, 1.0))

    # -------- INTERPRETATION --------
    st.subheader(" SEO Interpretation")

    if entity_density > 0.045:
        st.success("Excellent entity-rich content. Strong semantic authority signals.")
    elif entity_density > 0.025:
        st.warning("Moderate entity coverage. Consider adding more topic-specific entities.")
    else:
        st.error("Low entity coverage. Content may lack contextual depth.")

    if entity_diversity < 0.5:
        st.info("You are repeating few entities too often. Add broader contextual references.")

    st.markdown("""
###  Why Entities Matter in SEO

Search engines build **knowledge graphs** using entities.

Entity-rich content usually results in:

• stronger topical authority  
• deeper semantic understanding  
• improved ranking potential  
• better AI search visibility
""")