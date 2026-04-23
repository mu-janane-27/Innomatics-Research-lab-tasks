from src.rag_pipeline import build_pipeline, generate_answer

def main():
    db = build_pipeline("data/notes.pdf")

    while True:
        query = input("\nAsk: ")

        if query == "exit":
            break

        print("\nAnswer:\n", generate_answer(db, query))

if __name__ == "__main__":
    main()