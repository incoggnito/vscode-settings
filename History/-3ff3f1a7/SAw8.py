import logging
from typing import Optional

from fastapi import Depends, APIRouter, HTTPException, Security, status
from fastapi.security.api_key import APIKeyQuery, APIKeyCookie, APIKeyHeader, APIKey
from fastapi.security import OAuth2
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.openapi.models import OAuthFlowAuthorizationCode
from starlette.requests import Request

from app.api.deps import authify, get_current_user, get_user_group
from app.models.user import User
from app.core.config import settings


logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/secure/me/")
async def private(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/secure/group/")
async def group(group: str = Depends(get_user_group)):
    return {"group": group}


@router.get("/secure/apikey/")
async def test_api_key():
    return {"entered api key": "test", "status": "ok"}


# api_key: APIKey = Depends(get_current_user)

# class OAuth2TokenBearerAPIKey(OAuth2):
#     def __init__(
#         self,
#         tokenUrl: str,
#         scheme_name: str = None,
#         scopes: dict = None,
#         auto_error: bool = True,
#     ) -> None:
#         self.auto_error = auto_error
#         if not scopes:
#             scopes = {}
#         flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl, "scopes": scopes})
#         super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

#     async def __call__(self, request: Request) -> Optional[str]:
#         # api_key_query: str = Security(api_key_query),
#         # api_key_header: str = Security(api_key_header),
#         # api_key_cookie: str = Security(api_key_cookie),
#         api_key = get_api_key(auto_error=self.auto_error)
#         header_auth = request.headers.get("Authorization")
#         if api_key:
#             param = {"uid": 100}  # machine to machine connection -> needs UID for db queries?
#             logger.info(f"OAuth2TokenBearerAPIKey __call__ {api_key=}")
#             return param

#         header_scheme, header_param = get_authorization_scheme_param(header_auth)

#         if header_scheme.lower() == "bearer":
#             authorization = True
#         else:
#             authorization = False

#         if not authorization or header_scheme.lower() != "bearer":
#             if self.auto_error:
#                 raise HTTPException(
#                     status_code=status.HTTP_403_FORBIDDEN, detail="Not authenticated"
#                 )
#             else:
#                 return None

#         return header_param
