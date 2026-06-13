import chromadb
from sentence_transformers import SentenceTransformer
from pipeline import build_chunks

COLLECTION_NAME = "unofficial_guide_reviews"

model = SentenceTransformer("all-MiniLM-L6-v2")


def build_vector_store():
    chunks = build_chunks()

    client = chromadb.PersistentClient(path="chroma_db")

    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = client.create_collection(name=COLLECTION_NAME)

    documents = [chunk["text"] for chunk in chunks]
    ids = [f"{chunk['source']}-{chunk['review_index']}-{chunk['chunk_index']}" for chunk in chunks]
    metadatas = [
        {
            "source": chunk["source"],
            "review_index": chunk["review_index"],
            "chunk_index": chunk["chunk_index"],
        }
        for chunk in chunks
    ]

    embeddings = model.encode(documents).tolist()

    collection.add(
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids,
    )

    print(f"Stored {len(documents)} chunks in ChromaDB.")
    return collection


def get_collection():
    client = chromadb.PersistentClient(path="chroma_db")
    return client.get_collection(name=COLLECTION_NAME)


def retrieve(query, k=3):
    collection = get_collection()
    query_embedding = model.encode([query]).tolist()[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k,
    )

    retrieved = []

    for i in range(len(results["documents"][0])):
        retrieved.append(
            {
                "text": results["documents"][0][i],
                "source": results["metadatas"][0][i]["source"],
                "review_index": results["metadatas"][0][i]["review_index"],
                "chunk_index": results["metadatas"][0][i]["chunk_index"],
                "distance": results["distances"][0][i],
            }
        )

    return retrieved


def print_results(query):
    print("=" * 80)
    print(f"QUERY: {query}")
    print("=" * 80)

    results = retrieve(query, k=3)

    for i, result in enumerate(results, start=1):
        print(f"\nResult {i}")
        print(f"Source: {result['source']}")
        print(f"Review: {result['review_index']}")
        print(f"Chunk: {result['chunk_index']}")
        print(f"Distance: {result['distance']:.4f}")
        print(result["text"])

import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

def ask(question):
    retrieved_chunks = retrieve(question, k=5)

    context = "\n\n".join(
        f"Source: {chunk['source']}\nReview {chunk['review_index']}\n{chunk['text']}"
        for chunk in retrieved_chunks
    )

    sources = sorted(set(chunk["source"] for chunk in retrieved_chunks))

    prompt = f"""
You are answering questions for an unofficial guide to CUNY City Tech professors.

Use ONLY the context below.
Do not use outside knowledge.
If the context does not contain enough information, say:
"I don't have enough information in the documents to answer that."

Question:
{question}

Context:
{context}

Answer with:
1. A short answer grounded only in the context.
2. Mention the source filenames used.
"""

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You only answer using retrieved document context."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )

    return {
        "answer": response.choices[0].message.content,
        "sources": sources,
        "retrieved_chunks": retrieved_chunks,
    }

if __name__ == "__main__":
    build_vector_store()

    test_queries = [
        "Vaneet Singh easy grader straightforward homework",
        "Jeffery Kroll math extra credit clear explanations",
        "Roman Kezerashvili difficult hard to understand physics",
    ]

    for q in test_queries:
        print_results(q)
        print("\n")
    