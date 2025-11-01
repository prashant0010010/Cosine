import requests
from bs4 import BeautifulSoup
import re
import nltk

nltk.download('punkt', quiet=True)

def fetch_text_from_url(url):
    """Fetch visible text content from a webpage."""
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    for script in soup(['script', 'style']):
        script.extract()
    text = soup.get_text(separator=' ')
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def clean_text(text):
    """Basic cleaning and normalization."""
    text = re.sub(r'\s+', ' ', text)
    return text.strip()
