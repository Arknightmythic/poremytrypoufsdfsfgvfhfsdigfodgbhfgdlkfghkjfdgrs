import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, SearchRequest

load_dotenv()

async def retrieve_knowledge(query_vector: list[float], collection_name: str):
    print("Entering retrieve_knowledge method")
    client = QdrantClient(url=os.getenv('QDRANT_URL'))
    results = client.search(
        collection_name= collection_name,
        query_vector=query_vector,
        limit=os.getenv('TOP_K')
    )
    print("Exiting retrieve_knowledge method")
    return [hit.payload for hit in results]

# async def retrieve_knowledge(query_vector: list[float], collection_name: str):
#     print("Entering retrieve_knowledge method")
#     client = QdrantClient(url=os.getenv('QDRANT_URL'))
#     results = []
#     results_panduan = client.search(
#         collection_name= "panduan_collection",
#         query_vector=query_vector,
#         limit=10
#     )
#     results_peraturan = client.search(
#         collection_name= "peraturan_collection",
#         query_vector=query_vector,
#         limit=10
#     )
#     results_uraian = client.search(
#         collection_name= "uraian_collection",
#         query_vector=query_vector,
#         limit=10
#     )
#     for r in results_panduan:
#         results.append(r.payload)
#     for r in results_peraturan:
#         results.append(r.payload)
#     for r in results_uraian:
#         results.append(r.payload)
#     print("Exiting retrieve_knowledge method")
#     return results