from pathlib import Path

from fastapi import FastAPI, APIRouter, Depends  # , Request

from starlette.middleware.sessions import SessionMiddleware

from app.api.v1.api import api_router
from app.core.config import settings

BASE_PATH = Path(__file__).resolve().parent

root_router = APIRouter()
app = FastAPI(
    title="Projecthours API",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)
app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(root_router)