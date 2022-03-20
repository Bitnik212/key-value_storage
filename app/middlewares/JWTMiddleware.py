from fastapi import HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.requests import Request

from app.utils.JWTUtil import JWTUtil


class JWTMiddleware(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTMiddleware, self).__init__(auto_error=auto_error)
        self.util = JWTUtil()

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials:
        credentials: HTTPAuthorizationCredentials = await super(JWTMiddleware, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.util.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")


