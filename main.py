import tkinter as tk
from tkinter import scrolledtext, messagebox
from modules.text_cleaner import clean_text
from modules.bert_analyzer import get_sentence_embeddings, compute_semantic_density, compute_cosine_similarity, add_to_niche_memory, load_niche_memory, clear_niche_memory
from modules.seo_report import print_report
from modules.bert_analyzer import analyze_sentences
from modules.seo_report import generate_report
from PIL import Image, ImageTk
import io
from modules.seo_report import generate_simple_summary, save_report_as_pdf
from tkinter import filedialog
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog, simpledialog
from PIL import Image, ImageTk
import io
import matplotlib.pyplot as plt
from modules.text_cleaner import clean_text
from modules.bert_analyzer import (
    get_sentence_embeddings,
    compute_semantic_density,
    compute_cosine_similarity,
    analyze_sentences,
    add_to_niche_memory,
    load_niche_memory,
    clear_niche_memory,
)
from modules.seo_report import (
    generate_simple_summary,
    save_report_as_pdf,
    generate_report,   # if you still use it
)


def generate_and_save_report_gui():
    article = article_text.get("1.0", tk.END)
    target = target_text.get("1.0", tk.END)

    if not article.strip() or not target.strip():
        messagebox.showwarning("Input Error", "Please enter both article and target topic.")
        return

    # Run analysis
    sentence_results = analyze_sentences(article, target)
    _, embeddings = get_sentence_embeddings(clean_text(article))
    density = compute_semantic_density(embeddings)
    similarity = compute_cosine_similarity(article, target)

    # Create summary
    summary = generate_simple_summary(sentence_results, density, similarity)

    # Generate horizontal bar chart for sentence similarity
    sentences = [ (s if len(s) <= 80 else s[:77] + "...") for s, _, _ in sentence_results ]  # trim long sentences
    scores = [ sc for _, sc, _ in sentence_results ]

    if not scores:
        messagebox.showwarning("No Data", "No sentences found to plot.")
        return

    plt.figure(figsize=(8, max(3, len(scores)*0.3)))
    plt.barh(range(len(scores)), scores, align='center')
    plt.yticks(range(len(scores)), sentences)
    plt.xlabel("Cosine Similarity")
    plt.title("Sentence Similarity Scores")
    plt.xlim(0, 1)
    plt.tight_layout()

    chart_path = "sentence_similarity.png"
    plt.savefig(chart_path)
    plt.close()  # IMPORTANT to free memory

    # Ask for article title
    title_input = simpledialog.askstring("Article Title", "Enter the article title:")
    if not title_input:
        title_input = "Untitled Article"

    # Show summary in GUI
    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, summary)

    # Display chart in GUI (optional)
    try:
        img = Image.open(chart_path)
        img_tk = ImageTk.PhotoImage(img)
        graph_label.configure(image=img_tk)
        graph_label.image = img_tk
    except Exception:
        pass

    # Ask where to save PDF
    save_path = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF Files", "*.pdf")],
        title="Save SEO Report"
    )

    if save_path:
        save_report_as_pdf(summary, save_path, article_title=title_input, chart_path=chart_path)
        messagebox.showinfo("Report Saved", f"SEO Report saved to:\n{save_path}")


def analyze_article():
    article = article_text.get("1.0", tk.END)
    target = target_text.get("1.0", tk.END)
    
    if not article.strip() or not target.strip():
        messagebox.showwarning("Input Error", "Please enter both article and target topic.")
        return

    article_clean = clean_text(article)
    target_clean = clean_text(target)
    
    sentences, embeddings = get_sentence_embeddings(article_clean)
    density = compute_semantic_density(embeddings)
    similarity = compute_cosine_similarity(article_clean, target_clean)

    niche_embeddings = load_niche_memory()
    niche_sim = "N/A"
    if niche_embeddings:
        # simple average comparison
        niche_sim = compute_cosine_similarity(article_clean, " ".join([str(e) for e in niche_embeddings]))

    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, f"Semantic Density: {density:.4f}\n")
    result_text.insert(tk.END, f"Cosine Similarity to target: {similarity:.4f}\n")
    result_text.insert(tk.END, f"Similarity with niche memory: {niche_sim}\n")

def add_to_memory():
    article = article_text.get("1.0", tk.END)
    add_to_niche_memory(article)
    messagebox.showinfo("Success", "Article added to niche memory!")

def clear_memory():
    clear_niche_memory()
    messagebox.showinfo("Success", "Niche memory cleared!")

def generate_report_gui():
    article = article_text.get("1.0", tk.END)
    target = target_text.get("1.0", tk.END)

    if not article.strip() or not target.strip():
        messagebox.showwarning("Input Error", "Please enter both article and target topic.")
        return

    sentence_results = analyze_sentences(article, target)
    _, embeddings = get_sentence_embeddings(clean_text(article))
    density = compute_semantic_density(embeddings)
    similarity = compute_cosine_similarity(article, target)

    img_bytes, summary_text = generate_report(sentence_results, density, similarity)

    # Display text summary
    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, summary_text)

    # Display graph in GUI
    img = Image.open(io.BytesIO(img_bytes.read()))
    img_tk = ImageTk.PhotoImage(img)
    graph_label.configure(image=img_tk)
    graph_label.image = img_tk

def analyze_sentences_gui():
    """
    Runs the sentence-level analysis and displays weak sentences in the GUI.
    """
    article = article_text.get("1.0", tk.END)
    target = target_text.get("1.0", tk.END)

    if not article.strip() or not target.strip():
        messagebox.showwarning("Input Error", "Please enter both article and target topic.")
        return

    sentence_results = analyze_sentences(article, target)

    # Show results in the result text area
    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, "Sentence-Level Semantic Analysis:\n\n")

    for i, (sentence, similarity, is_weak) in enumerate(sentence_results, 1):
        status = "⚠️ Weak" if is_weak else "✅ Strong"
        result_text.insert(tk.END, f"{i}. ({similarity:.3f}) {status}\n{sentence}\n\n")


# --- Tkinter GUI ---
root = tk.Tk()
root.title("Semantic Density & SEO Tool")

tk.Label(root, text="Paste Article:").pack()
article_text = scrolledtext.ScrolledText(root, width=80, height=10)
article_text.pack()

tk.Label(root, text="Target SEO Topic / Competitor Text:").pack()
target_text = scrolledtext.ScrolledText(root, width=80, height=5)
target_text.pack()

tk.Button(root, text="Analyze Article", command=analyze_article).pack(pady=5)
tk.Button(root, text="Add Article to Niche Memory", command=add_to_memory).pack(pady=5)
tk.Button(root, text="Clear Niche Memory", command=clear_memory).pack(pady=5)
tk.Button(root, text="Analyze Sentences", command=analyze_sentences_gui).pack(pady=5)

tk.Button(root, text="Generate & Save SEO Report", command=generate_and_save_report_gui).pack(pady=5)

tk.Button(root, text="Generate SEO Report", command=generate_report_gui).pack(pady=5)
graph_label = tk.Label(root)
graph_label.pack(pady=5)


tk.Label(root, text="Results:").pack()
result_text = scrolledtext.ScrolledText(root, width=80, height=10)
result_text.pack()

root.mainloop()
