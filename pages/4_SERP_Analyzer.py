import streamlit as st
import requests
from bs4 import BeautifulSoup

from modules.text_cleaner import clean_text
from modules.bert_analyzer import compute_cosine_similarity
from serpapi import GoogleSearch

st.title(" SERP Semantic Analyzer")

st.markdown("""
Analyze how your article compares to the **top Google search results**.

This tool automatically:

• retrieves top ranking pages  
• extracts their text content  
• measures semantic similarity between your article and ranking pages

Higher similarity usually means stronger **topical coverage and SERP alignment**.
""")

article_text = st.text_area(
    "Paste Your Article",
    placeholder="Paste the article you want to compare with Google SERP results.",
    height=250
)

keyword = st.text_input(
    "Target Keyword",
    placeholder="Enter the keyword you want to analyze SERP results for."
)


# --- Function to fetch SERP links ---
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


# --- Extract text from page ---
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


if st.button("Analyze SERP"):

    if not article_text.strip() or not keyword.strip():
        st.warning("Please provide both article text and keyword.")

    else:

        st.info("Fetching SERP results...")

        results = get_google_results(keyword)

        if not results:
            st.error("No SERP results found. Google may have blocked the request.")
            st.stop()

        article_clean = clean_text(article_text)

        st.subheader("Top SERP Comparisons")

        for url in results:

            page_text = extract_page_text(url)

            if not page_text:
                st.warning(f"Could not extract content from: {url}")
                continue

            page_clean = clean_text(page_text)

            similarity = compute_cosine_similarity(article_clean, page_clean)

            st.markdown(f"### 🔗 {url}")

            st.metric("Semantic Similarity", f"{similarity:.3f}")
            st.progress(float(similarity))

            st.caption(f"Extracted Words: {len(page_clean.split())}")

            if similarity >= 0.75:
                st.success("Strong alignment with this ranking page.")
            elif similarity >= 0.5:
                st.warning("Moderate alignment with this ranking page.")
            else:
                st.error("Low alignment with this ranking page.")

            st.markdown("---")