from pathlib import Path
import re

DOCUMENTS_DIR = Path("documents")


def clean_text(text):
    text = text.replace("\r\n", "\n")
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def split_reviews(text):
    parts = re.split(r"\n(?=Review \d+)", text)
    return [part.strip() for part in parts if part.strip()]


def chunk_long_review(review, max_chars=500, overlap=100):
    if len(review) <= max_chars:
        return [review]

    chunks = []
    start = 0

    while start < len(review):
        end = start + max_chars
        chunk = review[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(review):
            break

        start = end - overlap

    return chunks


def load_documents():
    documents = []

    for file_path in DOCUMENTS_DIR.glob("*.txt"):
        raw_text = file_path.read_text(encoding="utf-8")
        cleaned_text = clean_text(raw_text)

        documents.append({
            "source": file_path.name,
            "text": cleaned_text
        })

    return documents


def build_chunks():
    documents = load_documents()
    chunks = []

    for document in documents:
        reviews = split_reviews(document["text"])

        for review_index, review in enumerate(reviews, start=1):
            review_chunks = chunk_long_review(review)

            for chunk_index, chunk_text in enumerate(review_chunks, start=1):
                chunks.append({
                    "source": document["source"],
                    "review_index": review_index,
                    "chunk_index": chunk_index,
                    "text": chunk_text
                })

    return chunks


if __name__ == "__main__":
    documents = load_documents()
    chunks = build_chunks()

    print(f"Loaded documents: {len(documents)}")
    print(f"Total chunks: {len(chunks)}")
    print("\nSample chunks:\n")

    for i, chunk in enumerate(chunks[:5], start=1):
        print("=" * 60)
        print(f"Sample Chunk {i}")
        print(f"Source: {chunk['source']}")
        print(f"Review: {chunk['review_index']}")
        print(f"Chunk: {chunk['chunk_index']}")
        print(chunk["text"])
        print()