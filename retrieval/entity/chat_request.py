from pydantic import BaseModel

class ChatRequest(BaseModel):
    platform_unique_id: str
    query: str
    conversation_id: str = ""
    platform: str