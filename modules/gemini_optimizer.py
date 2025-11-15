from google import genai
from google.genai import types

SYSTEM_PROMPT = """
You are an expert SEO Content Rewriter. Your task is to rewrite the provided
'Original Article' to maximize its Semantic Similarity and Semantic Density
with the Target Keyword.
Maintain the core facts and narrative. Critically, improve sentence-level
semantic alignment by weaving in related LSI terms.
Do not add extra sections or introductory/concluding remarks.
Return ONLY the fully rewritten article text.
"""

def rewrite_article_gemini_v2(original_article, target_keyword, api_key=None):
    try:
        client = genai.Client(api_key=api_key)
    except Exception as e:
        return f"Error initializing Gemini client: {e}"

    user_prompt = f"""
    Target Keyword: {target_keyword}

    Original Article:
    ---
    {original_article}
    ---
    """

    config = types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT
    )

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",   # ✅ latest correct model name
            contents=user_prompt,
            config=config
        )
        return response.text
    except Exception as e:
        return f"An error occurred during API call: {e}"
