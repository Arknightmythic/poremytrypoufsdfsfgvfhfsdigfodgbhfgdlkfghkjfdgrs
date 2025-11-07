import os
from dotenv import load_dotenv
import requests

load_dotenv()

async def classify_collection(user_query: str, history_context: str) -> str:
    print("Entering generate_answer method")
    prompt = """
<introduction>
You are an assistant for the Virtual Assistant of BKPM (Badan Koordinasi Penanaman Modal).
Your task will be to classify user's query into different types of request related to BKPM.
You will receive <user_query> to be classified.
You will receive <context> for added context to help you classify the query.
<context> is the chat history of you and this user.
</introduction>

<guide>
if the query is about "tata cara" or "panduan", output:
panduan_collection

if the query is about "peraturan", output:
peraturan_collection

if the query is about "definisi" or "arti", output:
uraian_collection

if the query is a request to chat with a human agent/customer service/helpdesk, output:
helpdesk
if the query is about general or everyday knowledge (such as cooking, health, lifestyle, entertainment, sports, weather, or any topic unrelated to investment, licensing, or BKPM services),
output:
skip_collection_check
</guide>

<instructions>
- Input will be in Bahasa Indonesia.
- Your output must be in Bahasa Indonesia too.
- You must follow the given <guide> to classify the query.
- You can use <context> to help classification process in case <user_query> needs more context.
- You may not use <context> if it is blank.
- If you output "skip_collection_check", it means the query is unrelated to BKPM and should not be processed against any document collection.
</instructions>
"""
    user = f"""
<context>
{history_context}
</context>
    
<query>
{user_query}
</query>
"""
    payload = {
        "model": os.getenv('LLM_MODEL'),
        "messages": [
            {
                "role": "system",
                "content": prompt
            },
            {
                "role": "user",
                "content": user
            }
        ],
        "stream": False
        }
    response = requests.post("http://localhost:11434/api/chat", json=payload)
    response.raise_for_status()
    data = response.json()
    print("Exiting generate_answer method")
    message = data.get("message", {})
    return message.get("content", "").strip()