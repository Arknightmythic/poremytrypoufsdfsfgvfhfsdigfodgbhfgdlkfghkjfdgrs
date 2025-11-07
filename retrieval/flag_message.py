import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

async def flag_message(session_id:str, question: str):
    print("Flagging Message as 'Cannot Answer'")

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
            SET is_cannot_answer = TRUE
            WHERE session_id = %s
              AND message -> 'data' ->> 'content' = %s
              AND message -> 'data' ->> 'type' = 'human';
        """, (session_id, question))
        conn.commit()
    conn.close()

    print("Message flagged successfuly")
