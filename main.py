from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from retrieval.routes import ChatflowRoutes
from extraction.routes import PDFRoutes
from deletion.routes import DeleteRoutes

class ChatflowAPI:
    def __init__(self):
        self.app = FastAPI()

        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        self.include_routers()
        self.app.mount("/api", self.app)

    def include_routers(self):
        chatflow_routes = ChatflowRoutes()
        self.app.include_router(chatflow_routes.router, prefix="/chat")

        pdf_routes = PDFRoutes()
        self.app.include_router(pdf_routes.router, prefix="/extract")

        delete_routes = DeleteRoutes()
        self.app.include_router(delete_routes.router, prefix="/delete")

    def run(self):
        uvicorn.run(
            self.app,
            port=9534,
        )

dokuprime_sync_api = ChatflowAPI()
app = dokuprime_sync_api.app

if __name__ == "__main__":
    dokuprime_sync_api.run()