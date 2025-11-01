import matplotlib.pyplot as plt

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
