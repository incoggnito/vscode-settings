import logging
from typing import Dict, Optional, Tuple, Union

import jwt
from sqlalchemy.orm.session import Session
from app.models.user import User
from app.core.security import verify_password
from app.core.config import settings

from fastapi import HTTPException, Security, status

# from fastapi.security.api_key import APIKeyQuery, APIKeyCookie, APIKeyHeader, APIKey
from fastapi.security import OAuth2
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel, APIKeyIn, APIKey
from fastapi.openapi.models import OAuthFlowAuthorizationCode
from fastapi.security.api_key import APIKeyBase
from starlette.requests import Request
from starlette.status import HTTP_403_FORBIDDEN

logger = logging.getLogger(__name__)

"""
auto_error=False enables the usage of multiple authentication strategies 
without the API denying authentication when a key is not present. 
This could be the case if someone has the API key in a cookie and 
not as a query parameter.
"""
# API_KEY_NAME = "api_key"
# api_key_query = APIKeyQuery(name=API_KEY_NAME, auto_error=False)
# api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)
# api_key_cookie = APIKeyCookie(name=API_KEY_NAME, auto_error=False)


# async def get_api_key(
#     api_key_query: str = Security(api_key_query),
#     api_key_header: str = Security(api_key_header),
#     api_key_cookie: str = Security(api_key_cookie),
#     auto_error: bool = True,
# ):
#     if api_key_query in settings.API_KEYS:
#         return api_key_query
#     elif api_key_header in settings.API_KEYS:
#         return api_key_header
#     elif api_key_cookie in settings.API_KEYS:
#         return api_key_cookie
#     else:
#         if auto_error:
#             raise HTTPException(
#                 status_code=status.HTTP_403_FORBIDDEN,
#                 detail="Could not validate API key",
#             )


def authenticate(
    *,
    email: str,
    password: str,
    db: Session,
) -> Optional[User]:
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


class TokenVerifier:
    def __init__(
        self,
    ) -> None:
        self.config = {
            "DOMAIN": settings.URL,
            "CLIENT_ID": settings.CLIENT_ID,
            "ISSUER": settings.ISSUER,
            "ALGORITHMS": settings.ALGORITHMS,
        }
        self.jwks_client = jwt.PyJWKClient(settings.JWKS_URL)
        self.signing_key = None

    def decode(self, token) -> Union[dict, None]:
        try:
            self.signing_key = self.jwks_client.get_signing_key_from_jwt(token).key
        except jwt.exceptions.PyJWKClientError as e:
            logger.error(f"PyJWKClientError {e}")
        except jwt.exceptions.DecodeError as e:
            logger.error(f"DecodeError {e}")
        payload = None

        if token:
            try:
                payload = jwt.decode(
                    token,
                    self.signing_key,
                    algorithms=self.config["ALGORITHMS"],
                    audience=self.config["CLIENT_ID"],
                    issuer=self.config["ISSUER"],
                )
            except Exception as e:
                logger.error(f"Token couldn't be decoded: {e}")
        return payload


class OAuth2TokenBearerAPIKey(OAuth2):
    def __init__(
        self,
        authorizationUrl: str,
        tokenUrl: str,
        refreshUrl: Optional[str] = None,
        scheme_name: Optional[str] = None,
        scopes: Optional[Dict[str, str]] = None,
        description: Optional[str] = None,
        auto_error: bool = True,
    ) -> None:
        self.auto_error = auto_error
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(
            authorizationCode={
                "authorizationUrl": authorizationUrl,
                "tokenUrl": tokenUrl,
                "refreshUrl": refreshUrl,
                "scopes": scopes,
            }
        )
        super().__init__(
            flows=flows,
            scheme_name=scheme_name,
            description=description,
            auto_error=auto_error,
        )

    async def __call__(self, request: Request) -> Tuple[Optional[str], Optional[str]]:
        access_type = None
        header_auth = request.headers.get("Authorization")
        header_scheme, header_param = get_authorization_scheme_param(header_auth)

        if header_scheme.lower() == "bearer":
            access_type = "bearer"
            authorization = True
        elif header_scheme.lower() == "api_key":
            access_type = "api_key"
            authorization = True
        else:
            authorization = False

        if not authorization:
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, detail="Not authenticated"
                )
            else:
                return None, None

        return access_type, header_param


class APIKeyHeader(APIKeyBase):
    def __init__(
        self,
        *,
        name: str,
        scheme_name: Optional[str] = None,
        description: Optional[str] = None,
        auto_error: bool = True,
    ):
        self.model: APIKey = APIKey(
            **{"in": APIKeyIn.header}, name=name, description=description
        )
        self.scheme_name = scheme_name or self.__class__.__name__
        self.auto_error = auto_error

    async def __call__(self, request: Request) -> Optional[str]:
        api_key: str = request.headers.get(self.model.name)
        if not api_key:
            if self.auto_error:
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN, detail="Not authenticated"
                )
            else:
                return None
        return api_key