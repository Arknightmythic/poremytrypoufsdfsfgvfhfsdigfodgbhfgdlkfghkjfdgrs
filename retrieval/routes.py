from fastapi import APIRouter, Header, Depends
from .chatflow import ChatflowHandler
from .entity.chat_request import ChatRequest
from middleware.auth import verify_api_key

class ChatflowRoutes:
    def __init__(self):
        self.router = APIRouter()
        self.handler = ChatflowHandler()
        self.setup_routes()
        print("Chatflow routes initialized")

    def setup_routes(self):
        @self.router.post("/")
        async def chatflow_call(user_query: ChatRequest, key_checked: str = Depends(verify_api_key)):
            return await self.handler.chatflow_call(user_query)
