import streamlit as st

st.set_page_config(page_title="About AI Citation Analyzer", layout="wide")

# -----------------------------
# HERO SECTION
# -----------------------------

st.title(" About AI Citation Readiness Analyzer")

st.markdown("""
### Understand how ready your content is for **AI Search and Generative Engines**

Modern search engines and AI assistants evaluate content using **semantic signals**, not just keywords.

This platform analyzes your content using **multiple AI-driven SEO signals** to help you improve:

• semantic depth  
• topical relevance  
• SERP alignment  
• entity coverage  
• sentence strength  

The goal is simple:

**Help your content become citation-ready for AI search systems.**
""")

st.divider()

# -----------------------------
# TOOL OVERVIEW
# -----------------------------

st.header("Tools Included in This Platform")

st.markdown("""
Each tool analyzes a different **semantic signal** used by modern search engines and AI systems.
""")

tools = [
    {
        "Tool": "AI Citation Readiness Analyzer",
        "Purpose": "Overall GEO readiness score",
        "Feature": "Combines all signals into one score",
        "Link": "ai_citation_analyzer"
    },
    {
        "Tool": "Semantic Density Analyzer",
        "Purpose": "Measures topical cohesion",
        "Feature": "Evaluates how tightly concepts relate",
        "Link": "2_Semantic_Density"
    },
    {
        "Tool": "Cosine Similarity Analyzer",
        "Purpose": "Measures topic alignment",
        "Feature": "Compares article meaning with keyword",
        "Link": "3_Cosine_Similarity"
    },
    {
        "Tool": "SERP Semantic Analyzer",
        "Purpose": "Compare with ranking pages",
        "Feature": "Checks alignment with top results",
        "Link": "4_SERP_Analyzer"
    },
    {
        "Tool": "Entity SEO Analyzer",
        "Purpose": "Identify important entities",
        "Feature": "Extracts people, places, concepts",
        "Link": "5_Entity_SEO_Analyzer"
    }
]

for tool in tools:

    col1, col2, col3, col4 = st.columns([3,3,3,2])

    with col1:
        st.markdown(f"**{tool['Tool']}**")

    with col2:
        st.write(tool["Purpose"])

    with col3:
        st.write(tool["Feature"])

    with col4:
        st.link_button("Open Tool", f"/{tool['Link']}")

st.divider()

# -----------------------------
# PROBLEM SECTION
# -----------------------------

st.header(" Why This Tool Exists")

st.markdown("""
Search engines are evolving beyond traditional keyword matching.

Modern systems — including AI assistants and generative engines — evaluate content based on **semantic understanding**.

However, most SEO tools still focus on:

• keyword density  
• backlinks  
• simple keyword placement  

These metrics often fail to measure **how well content communicates meaning**.

This platform was created to help writers and SEO professionals analyze deeper signals such as:

• semantic similarity  
• topical cohesion  
• entity coverage  
• SERP semantic alignment  

These signals help determine whether content is **contextually rich and AI-interpretable**.
""")

st.divider()

# -----------------------------
# HOW THE TOOLS WORK TOGETHER
# -----------------------------

st.header("How These Tools Work Together")

st.markdown("""
Each analyzer focuses on a **different layer of semantic evaluation**.

When combined, they provide a more complete picture of how search engines and AI systems interpret your content.
""")

col1, col2 = st.columns(2)

with col1:

    st.markdown("""
### Content Structure

Semantic Density evaluates how closely ideas connect inside your article.

Strong semantic density indicates coherent topical coverage.
""")

with col2:

    st.markdown("""
### Topic Alignment

Cosine similarity measures how closely your content matches a specific topic or keyword.
""")

col3, col4 = st.columns(2)

with col3:

    st.markdown("""
### SERP Alignment

SERP analysis compares your article with ranking pages to identify how similar your content is to successful results.
""")

with col4:

    st.markdown("""
### Entity Coverage

Entity analysis identifies key concepts such as people, organizations, locations, and technologies mentioned in your article.
""")

st.divider()

# -----------------------------
# FAQ SECTION
# -----------------------------

st.header("Frequently Asked Questions")

with st.expander("What is semantic density?"):
    st.write("""
Semantic density measures how strongly ideas within an article connect with each other.

Higher density often indicates deeper topical coverage and stronger contextual relationships.
""")

with st.expander("What does cosine similarity measure?"):
    st.write("""
Cosine similarity measures how closely two texts align in meaning.

It is commonly used to evaluate how well an article matches a target topic or keyword.
""")

with st.expander("Why compare with SERP results?"):
    st.write("""
Ranking pages often represent strong topical coverage.

Comparing your article with them helps identify whether your content aligns with search intent.
""")

with st.expander("Why do entities matter for SEO?"):
    st.write("""
Search engines build knowledge graphs using entities.

Entity-rich content helps search engines understand context and relationships between concepts.
""")

with st.expander("What is AI citation readiness?"):
    st.write("""
AI citation readiness measures how well content aligns with signals that generative search systems use to reference and summarize information.
""")