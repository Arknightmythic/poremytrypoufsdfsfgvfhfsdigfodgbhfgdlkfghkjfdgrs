import os
from dotenv import load_dotenv
import requests

load_dotenv()

async def select_answer(user_query: str, context_docs: list[str]) -> str:
    print("Entering select_answer method")
    context = "\n======\n".join(context_docs)
    prompt = f"""
You are a knowledgeable assistant.
You will be given contents of information and select which ones are the most suitable to the user's query.
The contents will be separated by '======'
You only need to answer which descriptions are the most suitable with number(s).
Only output the number(s).

<example>
(contents 1)
======
(contents 2)
======
(contents 3)

and then you think that (content 2) is the best description, then your answer should be:
2

if you think many best descriptions matches the user queries, output should be like:
1,2,3
</example>

<descriptions>
{context}
</descriptions>

<user_query>
{user_query}
</user_query>
"""
    payload = {"model": os.getenv('LLM_MODEL'), "prompt": prompt, "stream": False}
    response = requests.post(f"{os.getenv("OLLAMA_BASE_URL")}api/generate", json=payload)
    response.raise_for_status()
    data = response.json()
    print("Exiting select_answer method")
    return data.get("response", "").strip()