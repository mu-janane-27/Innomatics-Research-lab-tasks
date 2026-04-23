def retrieve_chunks(vectorstore, query, k=5):
    """
    Safe retrieval using raw Chroma + manual embeddings
    """

    # Get embedding function from vectorstore
    embedding_function = vectorstore._embedding_function

    # Convert query → embedding
    query_embedding = embedding_function.embed_query(query)

    collection = vectorstore._collection

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )

    docs = []

    for doc_list in results.get("documents", []):
        for text in doc_list:
            if text and isinstance(text, str) and text.strip():
                class SimpleDoc:
                    def __init__(self, content):
                        self.page_content = content

                docs.append(SimpleDoc(text))

    return docs