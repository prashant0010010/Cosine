import streamlit as st
import requests
import pdfplumber
import docx
from bs4 import BeautifulSoup
import pandas as pd

from modules.text_cleaner import clean_text
from modules.bert_analyzer import analyze_sentences
from modules.gemini_optimizer import rewrite_article_gemini_v2
from modules.readability_analyzer import analyze_readability


st.set_page_config(page_title="AI Content Rewriter", layout="wide")

st.title(" AI Semantic Content Rewriter (Gemini AI)")

# -------------------------------------------------
# HOOK SECTION
# -------------------------------------------------

st.markdown("""
Modern search engines and AI assistants evaluate content using **semantic relevance**, not just keywords.

This tool helps you **rewrite articles using Google Gemini AI** to improve:

• semantic alignment  
• topical relevance  
• entity coverage  
• sentence strength  

Paste an article, provide a keyword, and generate a **semantically improved version** ready for SEO and AI search systems.
""")

st.divider()

# -------------------------------------------------
# INPUT OPTIONS
# -------------------------------------------------

st.header("📥 Provide Your Content")

input_type = st.radio(
    "Choose Input Type",
    ["Paste Text", "URL", "Upload File"]
)

article_text = ""

# ---- TEXT INPUT ----

if input_type == "Paste Text":
    article_text = st.text_area("Paste your article", height=300)

# ---- URL INPUT ----

elif input_type == "URL":

    url = st.text_input("Enter article URL")

    if st.button("Extract Content from URL"):

        try:
            page = requests.get(url)
            soup = BeautifulSoup(page.text, "html.parser")

            paragraphs = soup.find_all("p")
            article_text = " ".join([p.get_text() for p in paragraphs])

            st.success("Content extracted successfully")
            st.text_area("Extracted Content", article_text, height=300)

        except:
            st.error("Failed to extract content")

# ---- FILE INPUT ----

elif input_type == "Upload File":

    uploaded_file = st.file_uploader(
        "Upload article file",
        type=["txt", "pdf", "docx"]
    )

    if uploaded_file:

        if uploaded_file.type == "text/plain":
            article_text = uploaded_file.read().decode("utf-8")

        elif uploaded_file.type == "application/pdf":
            with pdfplumber.open(uploaded_file) as pdf:
                article_text = "\n".join([page.extract_text() for page in pdf.pages])

        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            doc = docx.Document(uploaded_file)
            article_text = "\n".join([p.text for p in doc.paragraphs])

        st.text_area("Extracted Content", article_text, height=300)


# -------------------------------------------------
# TARGET KEYWORD
# -------------------------------------------------

target_keyword = st.text_input("Target Keyword / Topic")

# -------------------------------------------------
# REWRITE BUTTON
# -------------------------------------------------

if st.button("Generate AI Optimized Article"):

    if not article_text.strip():
        st.error("Please provide article content.")
    elif not target_keyword.strip():
        st.error("Please provide target keyword.")
    else:

        with st.spinner("Optimizing content with Gemini AI..."):

            improved_article = rewrite_article_gemini_v2(
                article_text,
                target_keyword,
                st.secrets.get("GEMINI_API_KEY")
            )

        st.success("Optimization complete")

        st.subheader(" Optimized Article")

        st.text_area(
            "AI Improved Content",
            improved_article,
            height=350
        )

        # --------------------------------
        # SENTENCE ANALYSIS
        # --------------------------------

        original_results = analyze_sentences(article_text, target_keyword)
        improved_results = analyze_sentences(improved_article, target_keyword)

        st.subheader(" Sentence Comparison")

        rows = []

        min_len = min(len(original_results), len(improved_results))

        for i in range(min_len):

            old_sentence, old_score, _ = original_results[i]
            new_sentence, new_score, _ = improved_results[i]

            status = (
                "Improved" if new_score > old_score else
                "Declined" if new_score < old_score else
                "Same"
            )

            rows.append({
                "Old Sentence": old_sentence,
                "Old Score": round(old_score,3),
                "New Sentence": new_sentence,
                "New Score": round(new_score,3),
                "Status": status
            })

        df = pd.DataFrame(rows)

        st.dataframe(df, use_container_width=True)

        # --------------------------------
        # READABILITY
        # --------------------------------

        st.subheader(" Readability Analysis")

        readability = analyze_readability(improved_article)

        st.text(readability)

st.divider()

# -------------------------------------------------
# EDUCATIONAL SECTION
# -------------------------------------------------

st.header(" What This Tool Does")

st.markdown("""
The AI Content Rewriter analyzes and improves articles using **semantic optimization techniques**.

Instead of simply inserting keywords, the system improves:

• topic coverage  
• contextual meaning  
• sentence relevance  
• semantic relationships between ideas
""")

st.markdown("""
### The Problem This Tool Solves

Many articles rank poorly because they suffer from:

• weak topic alignment  
• low semantic depth  
• missing entities  
• sentences drifting off topic  

This tool helps correct those problems automatically.
""")

st.markdown("""
### How The Tool Works

1️⃣ Your article is analyzed sentence-by-sentence  
2️⃣ Each sentence is evaluated using **semantic similarity models**  
3️⃣ Weak sentences are identified  
4️⃣ Google Gemini rewrites the article to improve topical alignment  
5️⃣ The improved version is re-analyzed to measure improvement
""")

st.markdown("""
### How Gemini AI Is Used

This tool uses **Google Gemini API** from Google AI Studio.

Gemini is prompted to:

• maintain original meaning  
• improve semantic alignment  
• strengthen topic coverage  
• include relevant contextual terms

The result is an article that better matches **modern AI search systems**.
""")

st.divider()

# -------------------------------------------------
# FAQ
# -------------------------------------------------

st.header(" Frequently Asked Questions")

with st.expander("Does this tool replace human writing?"):
    st.write("""
No. The tool improves structure and semantic alignment, but human editing is still recommended.
""")

with st.expander("Will rewriting affect my article meaning?"):
    st.write("""
The system instructs Gemini to preserve the original meaning while improving topical relevance.
""")

with st.expander("Is the content safe for SEO?"):
    st.write("""
Yes. The tool focuses on improving semantic signals rather than keyword stuffing.
""")

with st.expander("Why analyze sentences individually?"):
    st.write("""
Sentence-level analysis helps detect weak or off-topic sections within the article.
""")

with st.expander("Why use Gemini AI instead of other models?"):
    st.write("""
Gemini provides strong reasoning capabilities and performs well for structured content rewriting tasks.
""")