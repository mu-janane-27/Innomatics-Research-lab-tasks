# RAG-Based Customer Support Assistant

This project implements a **Retrieval-Augmented Generation (RAG)** system that answers user queries based on a given PDF knowledge base.

---

## Overview

The system processes a document, converts it into embeddings, retrieves relevant information, and generates accurate responses using a Large Language Model (LLM).

---

## Features

- PDF ingestion and processing  
- Text chunking  
- Embedding generation using Sentence Transformers  
- Retrieval-based answer generation  
- LLM integration using Groq API  
- Basic Human-in-the-Loop (HITL) concept  

---

## Workflow

User Query → Retrieval → Context → LLM → Answer  

---

## Tech Stack

- Python  
- Sentence Transformers  
- LangChain (basic usage)  
- Groq API (LLM)  

---

## Project Structure

RAG_Project
- src
- data
- screenshots
- main.py
- requirements.txt
- README.md


---

## How to Run

1. Install dependencies:
pip install -r requirements.txt


2. Add your API key in `llm.py`:

API_KEY = "YOUR_API_KEY_HERE"


3. Run the project:

python main.py


---

## Note

This project demonstrates a simplified RAG pipeline using embedding-based retrieval.  
Vector database (ChromaDB) and advanced orchestration concepts were studied during development.

---

## Conclusion

This system improves response accuracy by grounding answers in retrieved context rather than generating responses blindly.

---

## Author

Janane M U
