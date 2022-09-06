import logging
from typing import Generator, Tuple

from fastapi import Depends, HTTPException, status, Header
from jose import JWTError
from sqlalchemy.orm.session import Session
from fastapi.security import (
    OAuth2AuthorizationCodeBearer,
)

from app.core.auth import TokenVerifier, OAuth2TokenBearer, APIKeyHeader
from app.db.session import SessionLocal
from app.models.user import User
from app import crud
from app.core.config import settings


logger = logging.getLogger(__name__)

verifier = TokenVerifier()

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    tokenUrl=settings.TOKEN_URL,
    authorizationUrl=settings.AUTH_URL,
    scopes=settings.SCOPES,
)


def oauth_token(authorization=Header(None)):
    if authorization:
        return OAuth2AuthorizationCodeBearer(
            tokenUrl=settings.TOKEN_URL,
            authorizationUrl=settings.AUTH_URL,
            scopes=settings.SCOPES,
        )
    else:
        raise Exception


def custom_oauth_token(authorization=Header(None)):
    if not authorization:
        return None
    else:
        return OAuth2TokenBearer(
            tokenUrl=settings.TOKEN_URL,
            authorizationUrl=settings.AUTH_URL,
            scopes=settings.SCOPES,
            auto_error=False,
        )


api_token = APIKeyHeader(name="Authorization")


def api_key(api_key=Header(None), uid=Depends(api_token)):  # TODO simple API Key auth
    if not api_key:
        return None
    else:
        return True


# https://stackoverflow.com/questions/64731890/fastapi-supporting-multiple-authentication-dependencies
def authify(api_key: str = Depends(api_key), token: str = Depends(oauth_token)):
    if not (api_key or token):
        raise Exception


def get_token_verifier() -> Generator:
    yield verifier


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(
    db: Session = Depends(get_db),
    access: Tuple[str, str] = Depends(authify),
    verifier: TokenVerifier = Depends(get_token_verifier),
) -> User:
    access_type, access_token = access

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": f"{access_type}"},
    )

    try:
        if access_type == "api_key":
            user = crud.user.get_by_uid(db, uid=settings.BMW_USER_ID)
            if user:
                return user
            else:
                raise credentials_exception

        elif access_type == "bearer":

            payload = verifier.decode(access_token)
            if payload:
                uid = payload.get("uid", None)
                if not uid:
                    raise credentials_exception

                user = crud.user.get_by_uid(db, uid=uid)

        if user is None and payload is not None:
            user = crud.user.create_user_from_token(db, payload)
            logger.info(f"created user {user.name} with uid {user.uid} from token")

        return user

    except JWTError:
        raise credentials_exception


async def get_user_group(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
) -> str:
    meta = crud.meta.get_latest_by_uid(db, current_user.uid)
    return meta.groups


def get_current_active_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user
