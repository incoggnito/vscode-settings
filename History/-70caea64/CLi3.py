import os

from pydantic import AnyHttpUrl, BaseSettings, EmailStr, validator
from typing import List, Union

import logging

from pathlib import Path
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

if os.getenv("APPLICATION_API_VERSION"):
    logger.info("Load env from docker!")
else:
    env_path = Path(".") / ".env"
    load_dotenv(dotenv_path=env_path)
    if os.getenv("APPLICATION_API_VERSION"):
        logger.info("Load env variables from .env file!")
    else:
        logging.error("Can't find the env variables!")
        raise EnvironmentError


class Settings(BaseSettings):
    API_V1_STR: str = os.getenv("APPLICATION_API_VERSION")
    ENVIRONMENT: str = "dev"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    URL: str = os.getenv("AUTHENTIK_URL")
    TOKEN_URL: str = os.getenv("AUTHENTIK_TOKEN_URL")
    AUTH_URL: str = os.getenv("AUTHENTIK_AUTH_URL")
    SCOPES: dict = {"scope": os.getenv("AUTHENTIK_SCOPES")}
    APPLICATION_URL: str = os.getenv("AUTHENTIK_REDIRECT_URI")
    CONF_URL: str = os.getenv("AUTHENTIK_CONF_URL")
    JWKS_URL: str = os.getenv("AUTHENTIK_JWKS_URL")
    ISSUER: str = os.getenv("AUTHENTIK_ISSUER")
    ALGORITHMS: str = os.getenv("AUTHENTIK_ALGORITHMS")
    CLIENT_ID: str = os.getenv("CLIENT_ID")
    TL_GROUP: List[str] = ["TL", "GF", "API"]
    GF_GROUP: List[str]
    ADMIN_GROUP: List[str] = ["ServerAdmin", "HR"]
    SQLALCHEMY_DATABASE_URI: str = os.getenv("DATABASE_URL")
    BMW_USER_ID: int = os.getenv("BMW_USER_ID")
    API_KEY_0: str = os.getenv("API_KEY_0")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    API_KEYS: List[str] = [API_KEY_0]

    logger.info(f"{SQLALCHEMY_DATABASE_URI=}")

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # SQLALCHEMY_DATABASE_URI: Optional[str] = "sqlite:///app.db"
    FIRST_SUPERUSER_UID: int = 38
    FIRST_SUPERUSER_MAIL: EmailStr = "admin@amitronics.net"
    FIRST_SUPERUSER_PW: str = "CHANGEME"

    # POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    # POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    # POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    # POSTGRES_PORT: str = os.getenv(
    #     "POSTGRES_PORT", 5432
    # )  # default postgres port is 5432
    # POSTGRES_DB: str = os.getenv("POSTGRES_DB", "tdd")

    # f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

    class Config:
        case_sensitive = True


settings = Settings()
