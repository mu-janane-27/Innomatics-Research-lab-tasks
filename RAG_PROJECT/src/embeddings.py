from sentence_transformers import SentenceTransformer
import numpy as np

# Load model once
model = SentenceTransformer("all-MiniLM-L6-v2")

def create_embeddings(chunks):
    texts = [c.page_content for c in chunks]
    embeddings = model.encode(texts)
    return texts, embeddings


def search(query, texts, embeddings, k=5):
    query_embedding = model.encode([query])[0]

    # cosine similarity
    scores = np.dot(embeddings, query_embedding)

    top_k_indices = np.argsort(scores)[-k:][::-1]

    results = [texts[i] for i in top_k_indices]
    return results