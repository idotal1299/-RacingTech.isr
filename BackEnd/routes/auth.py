# routes/auth.py

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from starlette.responses import JSONResponse
from auth.auth_handler import verify_google_token, create_jwt_token
from services.user_service import create_user_if_not_exists

router = APIRouter()

class GoogleTokenRequest(BaseModel):
    token: str

@router.post("/auth/google")
async def google_auth(request: GoogleTokenRequest):
    try:
        # שלב 1: אימות מול Google
        google_user = verify_google_token(request.token)
        if not google_user:
            raise HTTPException(status_code=401, detail="Invalid Google token")

        # שלב 2: יצירת משתמש במסד אם לא קיים
        user = create_user_if_not_exists(
            sub=google_user["sub"],
            email=google_user["email"],
            name=google_user.get("name"),
            picture=google_user.get("picture")
        )

        # שלב 3: יצירת טוקן JWT
        jwt_token = create_jwt_token(
            sub=google_user["sub"],
            email=google_user["email"]
        )

        return JSONResponse(content={"racetech_token": jwt_token})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Authentication error: {str(e)}")
