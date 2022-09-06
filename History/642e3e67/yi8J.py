# import time
from pathlib import Path

from fastapi import FastAPI, APIRouter, Depends  # , Request

from starlette.middleware.sessions import SessionMiddleware

from app.api.v1.api import api_router
from app.core.config import settings
from app.api.deps import authify

BASE_PATH = Path(__file__).resolve().parent

root_router = APIRouter()
app = FastAPI(
    title="Projecthours API",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    dependencies=[Depends(authify)],
)

# TODO: generate real key and save in .env file
# SECRET_KEY = "random-string-for-randomness"
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(root_router)

if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
