import matplotlib.pyplot as plt
import io
import base64
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch
import numpy as np
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.units import inch
from datetime import datetime
import os

def print_report(article_density, cosine_value):
    print("\n===== SEO Semantic Analysis Report =====")
    print(f"Semantic Density Score: {article_density:.4f}")
    print(f"Cosine Similarity Score: {cosine_value:.4f}")

    if article_density < 0.5:
        print("→ Your content might be too scattered. Try making it more focused.")
    elif article_density > 0.8:
        print("→ Your content is dense and conceptually tight.")
    else:
        print("→ Balanced semantic flow detected.")

    if cosine_value < 0.5:
        print("→ Low similarity: might not align with your target SEO topic.")
    else:
        print("→ High similarity: strong SEO topical relevance.")

def plot_density_chart(density_score):
    plt.bar(['Semantic Density'], [density_score])
    plt.ylim(0, 1)
    plt.title('Semantic Density Visualization')
    plt.show()

def generate_report(sentence_results, overall_density, overall_similarity):
    """
    Create a bar graph of sentence similarities and generate a text summary.
    Returns (plot_image_path, summary_text)
    """

    sentences = [s for s, _, _ in sentence_results]
    scores = [sc for _, sc, _ in sentence_results]

    # --- Plot setup ---
    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.bar(range(len(scores)), scores, color=["green" if s > 0.5 else "red" for s in scores])
    ax.set_ylim(0, 1)
    ax.set_title("Sentence-Level Semantic Similarity")
    ax.set_xlabel("Sentence Index")
    ax.set_ylabel("Similarity to Target Topic")

    # Save plot to memory
    img_bytes = io.BytesIO()
    plt.tight_layout()
    plt.savefig(img_bytes, format='png')
    img_bytes.seek(0)

    # Generate pseudo-AI summary (rule-based for now)
    avg_score = np.mean(scores)
    weak_sentences = sum(1 for s in scores if s < 0.5)
    strong_sentences = len(scores) - weak_sentences

    summary = (
        f"📊 **AI Summary Report**\n\n"
        f"- Overall Semantic Density: {overall_density:.3f}\n"
        f"- Overall Cosine Similarity: {overall_similarity:.3f}\n"
        f"- Average Sentence Similarity: {avg_score:.3f}\n\n"
        f"Out of {len(scores)} sentences, {strong_sentences} are semantically strong, "
        f"while {weak_sentences} may need rewriting to align with your target topic.\n\n"
    )

    if avg_score < 0.5:
        summary += "⚠️ The article appears loosely connected to the target topic. Consider improving focus and topic consistency.\n"
    elif avg_score < 0.7:
        summary += "🟡 The article is moderately aligned. Some sections could be refined for stronger topic relevance.\n"
    else:
        summary += "✅ Excellent alignment! The article is highly relevant to the target SEO topic.\n"

    return img_bytes, summary

def generate_simple_summary(sentence_results, density, similarity):
    """
    Generates a simple SEO-style summary text.
    """
    scores = [s for _, s, _ in sentence_results]
    avg_score = np.mean(scores) if scores else 0
    weak_count = sum(1 for s in scores if s < 0.5)
    strong_count = len(scores) - weak_count

    summary = (
        f"📋 **SEO Summary Report**\n\n"
        f"Semantic Density: {density:.3f}\n"
        f"Overall Cosine Similarity: {similarity:.3f}\n"
        f"Average Sentence Similarity: {avg_score:.3f}\n"
        f"Strong Sentences: {strong_count}\n"
        f"Weak Sentences: {weak_count}\n\n"
    )

    # Simple AI-style feedback
    if avg_score < 0.5:
        summary += "⚠️ The article appears loosely related to the target topic. Improve focus and topic consistency.\n"
    elif avg_score < 0.7:
        summary += "🟡 The article is moderately aligned. Consider refining sections for stronger relevance.\n"
    else:
        summary += "✅ Excellent alignment! The article is highly relevant to the target SEO topic.\n"

    return summary


def save_report_as_pdf(summary_text, file_path="SEO_Report.pdf", article_title="Untitled Article", chart_path=None):
    """
    Saves the SEO report summary as a PDF file with title, date/time, and optional graph.
    """
    doc = SimpleDocTemplate(file_path, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    # Header info
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    story.append(Paragraph("<b>SEO Semantic Analysis Report</b>", styles["Title"]))
    story.append(Paragraph(f"<b>Article Title:</b> {article_title}", styles["Normal"]))
    story.append(Paragraph(f"<b>Generated On:</b> {current_time}", styles["Normal"]))
    story.append(Spacer(1, 0.3 * inch))

    # Add summary text
    for line in summary_text.split("\n"):
        story.append(Paragraph(line, styles["Normal"]))
        story.append(Spacer(1, 0.1 * inch))

    # Add chart image if exists
    if chart_path and os.path.exists(chart_path):
        story.append(Spacer(1, 0.3 * inch))
        story.append(Paragraph("<b>Sentence Similarity Chart</b>", styles["Heading2"]))
        story.append(Spacer(1, 0.2 * inch))
        story.append(Image(chart_path, width=5.5*inch, height=3.5*inch))

    doc.build(story)
    return file_path