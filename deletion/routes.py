from fastapi import APIRouter, Depends
from .handler import ChunkDeletionHandler
from middleware.auth import verify_api_key

class DeleteRoutes:
    def __init__(self):
        self.router = APIRouter()
        self.handler = ChunkDeletionHandler()
        self.setup_routes()
        print("Deletion routes initialized")

    def setup_routes(self):
        @self.router.delete("/")
        async def delete_chunk(id: str, category: str, key_checked: str = Depends(verify_api_key)):
            return await self.handler.delete_points_by_file_id(file_id_value=id, category=category)
