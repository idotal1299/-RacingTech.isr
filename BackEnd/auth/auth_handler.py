# auth/auth_handler.py

import os
import time
from jose import jwt, JWTError
from google.oauth2 import id_token
from google.auth.transport import requests as grequests

# משתני סביבה
SECRET_KEY = os.getenv("RACETECH_SECRET", "my-very-secret-key")
ALGORITHM = "HS256"
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "your-client-id.apps.googleusercontent.com")

# יצירת טוקן JWT חתום
def create_jwt_token(sub: str, email: str) -> str:
    payload = {
        "sub": sub,
        "email": email,
        "exp": int(time.time()) + 3600  # שעה תוקף
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

# פענוח טוקן JWT בצד השרת
def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        raise ValueError("Invalid token") from e

# אימות מול Google של id_token (מה-Client)
def verify_google_token(token: str) -> dict | None:
    try:
        id_info = id_token.verify_oauth2_token(
            token,
            grequests.Request(),
            GOOGLE_CLIENT_ID
        )
        return {
            "sub": id_info["sub"],
            "email": id_info["email"],
            "name": id_info.get("name"),
            "picture": id_info.get("picture")
        }
    except Exception:
        return None
