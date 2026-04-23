from src.loader import load_pdf
from src.chunker import chunk_documents
from src.embeddings import create_embeddings, search
from src.llm import call_llm


def build_pipeline(file_path):
    documents = load_pdf(file_path)
    chunks = chunk_documents(documents)

    texts, embeddings = create_embeddings(chunks)

    return texts, embeddings


def generate_answer(data, query):
    texts, embeddings = data

    docs = search(query, texts, embeddings)

    context = "\n".join(docs)

    prompt = f"""
Answer based on the context below.

Context:
{context}

Question: {query}
"""

    return call_llm(prompt)