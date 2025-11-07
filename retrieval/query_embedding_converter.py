import os
from dotenv import load_dotenv
from ollama import Client

load_dotenv()
ollama = Client()

async def convert_to_embedding(user_query: str):
    print("Entering convert_to_embedding method")
    query_vector = ollama.embeddings(model=os.getenv('EMBED_MODEL'), prompt=user_query)

    print("Exiting convert_to_embedding method")
    return query_vector["embedding"]