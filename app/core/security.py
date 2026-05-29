from fastapi import HTTPException, Security, status
from fastapi.security import HTTPBearer
from fastapi.security import HTTPAuthorizationCredentials
from app.core.exceptions.custom_exceptions import InvalidTokenException

from app.core.config import settings


bearer_scheme = HTTPBearer()


class AuthHandler:

    async def verify_api_token(
        self,
        credentials: HTTPAuthorizationCredentials = Security(
            bearer_scheme
        )
    ) -> str:

        token = credentials.credentials

        if token != settings.REVIEW_AI_API_TOKEN:

            raise InvalidTokenException("Invalid authentication token")

        return token


auth_handler = AuthHandler()