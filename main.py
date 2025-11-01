import tkinter as tk
from tkinter import scrolledtext, messagebox
from modules.text_cleaner import clean_text
from modules.bert_analyzer import get_sentence_embeddings, compute_semantic_density, compute_cosine_similarity, add_to_niche_memory, load_niche_memory, clear_niche_memory
from modules.seo_report import print_report

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

tk.Label(root, text="Results:").pack()
result_text = scrolledtext.ScrolledText(root, width=80, height=10)
result_text.pack()

root.mainloop()
