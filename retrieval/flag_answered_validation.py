import os
import psycopg
from dotenv import load_dotenv
from qdrant_client import AsyncQdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue
from langchain_ollama import OllamaEmbeddings

load_dotenv()

async def flag_answered_validation(session_id: str, user_question: str, threshold: float = 0.85) -> bool:
    qdrant_url = os.getenv("QDRANT_URL").strip()
    collection_name = os.getenv("QNA_COLLECTION")
    embed_model = os.getenv("EMBED_MODEL")
    ollama_base_url = os.getenv("OLLAMA_BASE_URL").strip()

    client = AsyncQdrantClient(url=qdrant_url)
    embeddings = OllamaEmbeddings(model=embed_model, base_url=ollama_base_url)

    validation_filter = Filter(
        must=[
            FieldCondition(
                key="filename",
                match=MatchValue(value="validation_history.txt")
            )
        ]
    )

    query_vector = await embeddings.aembed_query(user_question)
    results = await client.search(
        collection_name=collection_name,
        query_vector=query_vector,
        query_filter=validation_filter,
        limit=1
    )
    await client.close()

    if not results:
        print("[Validation Check] Not found in validation_history.txt.")
        return False

    top_result = results[0]
    score = top_result.score
    metadata = top_result.payload or {}

    print(f"[Validation Check] Found:")
    print(f"  • Similarity score : {score:.3f}")
    print(f"  • Sumber           : {metadata.get('filename', '-')}")
    print(f"  • Pertanyaan terkait : {metadata.get('question', '')[:120]}...")

    if score >= threshold:
        print("[Validation Check] High similarity, flagging true.")

        try:
            with psycopg.connect(
                dbname=os.getenv("DBNAME"),
                user=os.getenv("DBUSER"),
                password=os.getenv("DBPASSWORD"),
                host=os.getenv("DBHOST"),
                port=os.getenv("DBPORT"),
            ) as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        UPDATE bkpm.chat_history
                        SET is_answered = TRUE
                        WHERE session_id = %s
                          AND message -> 'data' ->> 'content' = %s
                          AND message -> 'data' ->> 'type' = 'human';
                    """, (session_id, user_question))
                    if cur.rowcount == 0:
                        print("[DB] !!! Tidak ada baris yang ter-update (kemungkinan pesan belum tersimpan)!!!")
                    else:
                        print(f"[DB] Sucess update {cur.rowcount} line.")
                conn.commit()
        except Exception as e:
            print(f"[ERROR] failed DB update: {e}")
            return False

        return True

    print("[Validation Check] Skor under threshold, return false.")
    return False
