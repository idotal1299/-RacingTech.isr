# BackEnd/middleware/auth_middleware.py

from fastapi import Request, HTTPException
from fastapi.routing import APIRoute
from jose import JWTError, jwt
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.status import HTTP_401_UNAUTHORIZED
import os

SECRET_KEY = os.getenv("RACETECH_SECRET", "my-very-secret-key")
ALGORITHM = "HS256"

EXCLUDED_PATHS = ["/auth/google", "/docs", "/openapi.json", "/"]  # פתוח לציבור

class JWTAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        if any(path.startswith(p) for p in EXCLUDED_PATHS):
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Missing token")

        token = auth_header.split(" ")[1]
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            request.state.user = payload
        except JWTError:
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid token")

        return await call_next(request)
