import time
import os
from typing import List
from langchain_community.vectorstores import Qdrant
from langchain_ollama import OllamaEmbeddings
from qdrant_client import QdrantClient
from langchain.schema import Document
from dotenv import load_dotenv

load_dotenv()

EMBEDDINGS_BASE_URL = os.getenv("OLLAMA_BASE_URL")
EMBEDDINGS_MODEL = os.getenv("EMBED_MODEL")
QDRANT_URL = os.getenv("QDRANT_URL")

embedding_model = OllamaEmbeddings(
    model=EMBEDDINGS_MODEL,
    base_url=EMBEDDINGS_BASE_URL
)
client = QdrantClient(url=QDRANT_URL)


def get_existing_doc_ids(collection_name: str) -> set:
    try:
        scroll_res = client.scroll(
            collection_name=collection_name,
            limit=10000,
            with_payload=True,
            with_vectors=False
        )
        ids = set()
        for point in scroll_res[0]:
            payload = point.payload or {}
            doc_id = payload.get("document_id")
            if doc_id:
                ids.add(doc_id)
        return ids
    except Exception as e:
        print(f"Ambil existing IDs di '{collection_name}': {e}")
        return set()

# def upsert_documents(
#     documents: List[Document],
#     batch_size: int = 64,
#     sleep_time: float = 0.2
# ):
#     collection_name = "bkpm_collection"
#     print(f"\nCollection Process '{collection_name}' ({len(documents)} docs)")

#     existing_collections = [c.name for c in client.get_collections().collections]
#     vectorstore = None

#     if collection_name in existing_collections:
#         print(f"Collection '{collection_name}' sudah ada — akan menambah dokumen baru.")
#         vectorstore = Qdrant(
#             client=client,
#             collection_name=collection_name,
#             embeddings=embedding_model
#         )
#     else:
#         print(f"Collection '{collection_name}' belum ada — akan dibuat baru.")

#     for i in range(0, len(documents), batch_size):
#         batch = documents[i:i+batch_size]
#         print(f"  → Batch Process {i // batch_size + 1} ({len(batch)} docs)...")

#         if vectorstore is None:
#             vectorstore = Qdrant.from_documents(
#                 documents=batch,
#                 embedding=embedding_model,
#                 url=QDRANT_URL,
#                 collection_name=collection_name
#             )
#         else:
#             vectorstore.add_documents(batch)

#         time.sleep(sleep_time)

#     print(f"Collection '{collection_name}' upserted {len(documents)} docs")

# ------------------------------------------------------------------
# ----- KALO DIPISAH COLLECTIONNYA JADI PERKATEGORI ----------------
# ------------------------------------------------------------------
def upsert_documents(
    documents: List[Document],
    category_field: str = "category",
    batch_size: int = 64,
    sleep_time: float = 0.2
):
    
    category_map = {}
    for doc in documents:
        category = doc.metadata.get(category_field, "umum")
        category_map.setdefault(category, []).append(doc)

    existing_collections = [c.name for c in client.get_collections().collections]

    for category, docs in category_map.items():
        collection_name = f"{category.replace(' ', '_').lower()}_collection"
        print(f"\nCollection Process '{collection_name}' ({len(docs)} docs)")

        # if collection_name in existing_collections:
        #     print(f"Collection '{collection_name}' sudah ada — cek duplikasi...")
        #     existing_ids = get_existing_doc_ids(collection_name)
        #     new_docs = [d for d in docs if d.metadata.get("document_id") not in existing_ids]
        #     if not new_docs:
        #         print("Tidak ada dokumen baru untuk diinsert.")
        #         continue
        #     vectorstore = Qdrant(
        #         client=client,
        #         collection_name=collection_name,
        #         embeddings=embedding_model
        #     )
        # else:
        new_docs = docs
        vectorstore = None  
        for i in range(0, len(new_docs), batch_size):
            batch = new_docs[i:i+batch_size]
            print(f"  → Batch Process {i // batch_size + 1} ({len(batch)} docs)...")

            if vectorstore is None:
                vectorstore = Qdrant.from_documents(
                    documents=batch,
                    embedding=embedding_model,
                    url=QDRANT_URL,
                    collection_name=collection_name
                )
            else:
                vectorstore.add_documents(batch)

            time.sleep(sleep_time)

        print(f"Collection '{collection_name}' upserted {len(new_docs)} docs")
