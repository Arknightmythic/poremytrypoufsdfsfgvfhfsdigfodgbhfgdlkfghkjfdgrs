import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

async def ingest_question_category(session_id:str, question: str, category: str, sub_category: str):
    print("Ingesting category for user's question")

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
            SET question_category = %s, question_sub_category = %s
            WHERE session_id = %s
              AND message -> 'data' ->> 'content' = %s
              AND message -> 'data' ->> 'type' = 'human';
        """, (category, sub_category, session_id, question))
        conn.commit()
    conn.close()

    print(f"session id {session_id} ; question {question}")
    print(f"Message categorized as {category} and {sub_category} successfuly")
    return category, sub_category
