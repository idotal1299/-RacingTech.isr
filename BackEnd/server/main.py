# server/main.py

import os
import time
import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from jose import jwt, JWTError
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.status import HTTP_401_UNAUTHORIZED

# -------------------- CONFIG --------------------
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "your-client-id.apps.googleusercontent.com")
SECRET_KEY = os.getenv("RACETECH_SECRET", "my-very-secret-key")
ALGORITHM = "HS256"
EXCLUDED_PATHS = ["/auth/google", "/docs", "/openapi.json", "/"]  # ראוטים שלא דורשים אימות

# -------------------- INIT APP --------------------
app = FastAPI()

# -------------------- JWT MIDDLEWARE --------------------
class JWTAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        if any(path.startswith(p) for p in EXCLUDED_PATHS):
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Missing or malformed token")

        token = auth_header.split(" ")[1]
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            request.state.user = payload
        except JWTError:
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")


        return await call_next(request)

# -------------------- MIDDLEWARE --------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # בפרודקשן להחליף ל: ["https://racetech.isr"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(JWTAuthMiddleware)

# -------------------- ROUTERS --------------------
from routes import user, auth        # כולל /auth/google ו- /api/me
from API import ws_lap               # מסלול שידור הקפות

app.include_router(user.router, prefix="/api")     # כולל /api/me
app.include_router(auth.router)                    # כולל /auth/google
app.include_router(ws_lap.router)

# -------------------- DEBUG / TEST --------------------
@app.get("/protected")
def protected_route(request: Request):
    user = request.state.user
    return {"message": "Authorized", "user": user}

# -------------------- MAIN --------------------
if __name__ == "__main__":
    uvicorn.run("server.main:app", host="0.0.0.0", port=8000, reload=True)
# For production, use a proper ASGI server like Daphne or Uvicorn with Gunicorn
