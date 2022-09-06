import logging
from typing import Optional, Union

import jwt
from sqlalchemy.orm.session import Session
from app.models.user import User
from app.core.security import verify_password
from app.core.config import settings


logger = logging.getLogger(__name__)

"""
auto_error=False enables the usage of multiple authentication strategies 
without the API denying authentication when a key is not present. 
This could be the case if someone has the API key in a cookie and 
not as a query parameter.
"""


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