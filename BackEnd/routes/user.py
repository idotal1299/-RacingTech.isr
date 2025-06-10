# routes/user.py

from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.orm import Session
from database.postgres import get_db
from services.user_service import get_user_by_id
from schemas.user import UserResponse
from starlette.status import HTTP_401_UNAUTHORIZED

router = APIRouter()

@router.get("/user/plan", response_model=UserResponse)
def get_user_plan(request: Request, db: Session = Depends(get_db)):
    user_data = request.state.user  # הגיע מה-JWT Middleware

    user_id = user_data.get("sub")
    if not user_id:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user = get_user_by_id(user_id, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user
