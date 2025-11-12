from dotenv import load_dotenv
import requests
import json
import os

load_dotenv()
API_URL = os.getenv("RERANK_URL")

async def rerank_documents(query, docs, filenames, top_k=3):
    print("Entering rerank_documents_with_flag method")

    payload = {
        "query": query,
        "docs": docs,
        "filenames": filenames
    }

    try:
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()

        response_list = response.json()
        reranked_docs, reranked_filenames = response_list

        print("Exiting rerank_documents_with_flag method")
        return reranked_docs, reranked_filenames
    except Exception as e:
        print(f"Reranking error: {str(e)}, using original scores")
        return docs[:top_k], filenames[:top_k]
