import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os
from nltk.tokenize import sent_tokenize

model = SentenceTransformer('all-MiniLM-L6-v2')

def get_sentence_embeddings(text):
    sentences = sent_tokenize(text)
    embeddings = model.encode(sentences)
    return sentences, embeddings

def compute_semantic_density(embeddings):
    sim_matrix = cosine_similarity(embeddings)
    density = np.mean(sim_matrix[np.triu_indices_from(sim_matrix, 1)])
    return density

def compute_cosine_similarity(text1, text2):
    emb1 = model.encode([text1])
    emb2 = model.encode([text2])
    return cosine_similarity(emb1, emb2)[0][0]

# --- Niche memory functions ---
MEMORY_FILE = "niche_memory.pkl"

def load_niche_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "rb") as f:
            return pickle.load(f)
    return []

def save_niche_memory(embeddings_list):
    with open(MEMORY_FILE, "wb") as f:
        pickle.dump(embeddings_list, f)

def add_to_niche_memory(text):
    embeddings_list = load_niche_memory()
    emb = model.encode([text])
    embeddings_list.append(emb[0])
    save_niche_memory(embeddings_list)

def clear_niche_memory():
    if os.path.exists(MEMORY_FILE):
        os.remove(MEMORY_FILE)
