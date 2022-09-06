from fastapi import HTTPException
from fastapi.security import OAuth2AuthorizationCodeBearer


from starlette.config import Config
from starlette.requests import Request
from starlette.responses import RedirectResponse

from authlib.integrations.starlette_client import OAuth
from authlib.integrations.starlette_client import OAuthError

import os
import logging

from fastapi import APIRouter
from fastapi.security import OAuth2AuthorizationCodeBearer

from app.core.config import settings

LOGGER = logging.getLogger(__file__)

router = APIRouter()

dir_path = os.path.dirname(os.path.realpath(__file__))
config = Config(os.path.join(dir_path, ".env"))
oauth = OAuth(config)

oauth.register(
    name="authentik",
    server_metadata_url=settings.CONF_URL,
    client_kwargs={"scope": "openid uid profile"},
    client_id=config.get("CLIENT_ID"),
    client_secret=config.get("CLIENT_SECRET"),
)

scopes = {"scope": "openid uid profile"}

# oauth2_scheme = OAuth2AuthorizationCodeBearer(
#     tokenUrl=settings.TOKEN_URL, authorizationUrl=settings.AUTH_URL, scopes=scopes
# )

logger = logging.getLogger(__name__)


@router.get("/login/")
async def login(request: Request):
    """[summary]

    Args:
        request (Request): [description]

    Returns:
        [type]: [description]
    """
    redirect_url = request.url_for("auth")
    # LOGGER.warning(f"/login endpoint: {redirect_url=}")
    return await oauth.authentik.authorize_redirect(request, redirect_url)


@router.get("/auth")
async def auth(request: Request):
    """[summary]

    Args:
        request (Request): [description]

    Raises:
        HTTPException: [description]

    Returns:
        [type]: [description]
    """
    try:
        token = await oauth.authentik.authorize_access_token(request)
    except OAuthError:
        raise HTTPException(status_code=401, detail="Not authorized!")

    id_token = token.get("id_token", None)
    request.session["id_token"] = id_token
    # logger.warning(f"token {token}")
    # decoded_token = jwt.decode(id_token, options={"verify_signature": False})
    uri = settings.APPLICATION_URL + f"?id_token={id_token}"
    return RedirectResponse(url=uri)


@router.get("/logout")
async def logout(request: Request):
    request.session.pop("id_token", None)
    return RedirectResponse(url="/")
