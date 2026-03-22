Semantic Density & SEO Analyzer

A Python-based SEO content analysis tool that evaluates the semantic density of your articles and their relevance to a target SEO topic. The tool includes a GUI and supports niche memory, allowing your system to learn and track content for your specific niche.

Features

Analyze semantic density of articles (how information-rich your content is).

Compute cosine similarity between your article and a target SEO topic or competitor content.

Track and store niche memory, so the system can learn your content style over time.

GUI interface using Tkinter (lightweight, works on Windows without Streamlit).

Visual feedback and actionable insights.

Installation
1. Clone the repository
git clone https://github.com/yourusername/semantic-seo-tool.git
cd semantic-seo-tool

2. Create a virtual environment (recommended)
python -m venv .venv


Activate it:

Windows PowerShell:

.\.venv\Scripts\Activate.ps1


Windows Command Prompt (cmd.exe):

.\.venv\Scripts\activate.bat

3. Upgrade pip
python -m pip install --upgrade pip

4. Install dependencies
pip install sentence-transformers scikit-learn numpy nltk beautifulsoup4 faiss-cpu matplotlib

5. Download NLTK data
import nltk
nltk.download('punkt')

Usage
1. Run the GUI
python main.py


A Tkinter GUI window will open.

2. Input your article

Paste Article: Enter your article in the first text box.

Target SEO Topic / Competitor Text: Enter your target keyword or a competitor’s article in the second text box.

3. Analyze Article

Click “Analyze Article” to:

Compute semantic density of your article.

Compute cosine similarity to your target topic.

Compare with niche memory (if any).

Results appear in the Results box.

4. Niche Memory Management

Add Article to Niche Memory: Saves this article’s embeddings so future articles can be compared against it.

Clear Niche Memory: Removes all stored embeddings.

Niche memory is stored in niche_memory.pkl in the project folder.

Project Structure
semantic-seo-tool/
│
├── main.py                  # Tkinter GUI entry point
├── niche_memory.pkl         # Stores embeddings for niche memory
├── modules/
│   ├── text_cleaner.py      # Text cleaning and URL fetching
│   ├── bert_analyzer.py     # Embeddings, semantic density, cosine similarity, niche memory
│   └── seo_report.py        # Reporting and visualization
├── requirements.txt         # Python dependencies
└── README.md

Extending the Tool

Sentence-Level Analysis: Highlight weak sentences with low semantic similarity.

Keyword Integration: Compare target keywords for semantic relevance.

Competitor Comparison: Automatically fetch and compare top-ranking pages.

Visualization Enhancements: Heatmaps, density charts, or sentence-level color coding.

Tips

Always activate the virtual environment before running the tool.

Keep niche_memory.pkl backed up if you want to preserve your learned niche.

This tool is designed for Windows, but can run on Linux/Mac with minor adjustments to Tkinter and paths.

License

MIT License – feel free to use, modify, and share.

Contact / Support

If you encounter issues, open a GitHub issue or contact the author.

This README is self-contained and allows anyone to:

Clone the repo

Set up the environment

Run the GUI

Use all features without needing any additional instructions.
