# import time
from pathlib import Path

from fastapi import FastAPI, APIRouter  # , Request, Depends

# from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from app.api.v1.api import api_router
from app.core.config import settings
from app.core.auth import 

BASE_PATH = Path(__file__).resolve().parent
# TEMPLATES = Jinja2Templates(directory=str(BASE_PATH / "templates"))

root_router = APIRouter()
app = FastAPI(
    title="Projecthours API", openapi_url=f"{settings.API_V1_STR}/openapi.json", dependencies=[]
)

# TODO: generate real key and save in .env file
SECRET_KEY = "random-string-for-randomness"
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

# @root_router.get("/", status_code=200)
# def root() -> dict:
#     """
#     Root GET
#     """
#     return TEMPLATES.TemplateResponse("index.html")


# @app.middleware("http") TODO Understand
# async def add_process_time_header(request: Request, call_next):
#     start_time = time.time()
#     response = await call_next(request)
#     process_time = time.time() - start_time
#     response.headers["X-Process-Time"] = str(process_time)
#     return response


app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(root_router)

if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
