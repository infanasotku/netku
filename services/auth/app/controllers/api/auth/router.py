from fastapi import APIRouter

from app.controllers.api.auth import token


router = APIRouter()

router.include_router(token.router, prefix="/token")
