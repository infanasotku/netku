from fastapi.routing import APIRouter


class INFORouter:
    def __init__(self):
        self.router = APIRouter()

        self.router.add_api_route("/health", self.health, methods=["GET"])

    async def health(self):
        return
