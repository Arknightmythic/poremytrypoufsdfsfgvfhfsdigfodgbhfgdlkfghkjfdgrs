import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

async def ingest_category(session_id:str, question: str, col_name: str):
    print("Ingesting category for user's question")

    if col_name == "panduan_collection":
        category = "panduan"
    elif col_name == "peraturan_collection":
        category = "peraturan"
    elif col_name == "uraian_collection":
        category = "uraian"
    elif col_name == "faq_collection":
        category = "faq"

    conn = psycopg.connect(
        dbname=os.getenv("DBNAME"),
        user=os.getenv("DBUSER"),
        password=os.getenv("DBPASSWORD"),
        host=os.getenv("DBHOST"),
        port=os.getenv("DBPORT"),
    )
    
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE bkpm.chat_history
            SET category = %s
            WHERE session_id = %s
              AND message -> 'data' ->> 'content' = %s
              AND message -> 'data' ->> 'type' = 'human';
        """, (category, session_id, question))
        conn.commit()
    conn.close()

    print(f"Message categorized as {category} successfuly")
    return category
