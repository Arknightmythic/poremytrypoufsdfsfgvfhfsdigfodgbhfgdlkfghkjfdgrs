import os
from dotenv import load_dotenv
from qdrant_client import AsyncQdrantClient

load_dotenv()

vectordb_client = AsyncQdrantClient(
    url=os.getenv("QDRANT_URL"),
    timeout=60.0
)