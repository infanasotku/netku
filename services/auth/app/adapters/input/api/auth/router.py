from fastapi import APIRouter

from app.adapters.input.api.auth import token


router = APIRouter()

router.include_router(token.router, prefix="/token")
