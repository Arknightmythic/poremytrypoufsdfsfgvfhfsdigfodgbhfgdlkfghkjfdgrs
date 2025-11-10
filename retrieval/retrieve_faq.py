import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient

load_dotenv()

async def retrieve_faq(query_vector: list[float], threshold: float = 1, client=None):
    print("[INFO] Entering retrieve_faq method")

    if client is None:
        client = QdrantClient(url=os.getenv("QDRANT_URL"))

    collection_name = "faq_collection"
    limit = 1 

    results = client.search(
        collection_name=collection_name,
        query_vector=query_vector,
        limit=limit
    )

    if not results:
        print("[INFO] No FAQ results found")
        return {"matched": False, "answer": None, "score": 0.0}

    top_hit = results[0]
    score = top_hit.score
    answer_text = top_hit.payload.get("text") or top_hit.payload.get("page_content")
    metadata = top_hit.payload.get("metadata") or {}
    filename = metadata.get("filename") if metadata else None

    print("[DEBUG] top_hit.payload:", top_hit.payload)
    print("[DEBUG] filename:", filename)

    print(f"[INFO] FAQ Top-1 Score: {score}")

    return {
        "matched": score >= threshold,
        "answer": answer_text,
        "score": score,
        "metadata": top_hit.payload,
        "filename": filename
    }
