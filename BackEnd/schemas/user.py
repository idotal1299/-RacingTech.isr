from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Literal, List
from datetime import datetime

class UserResponse(BaseModel):
    id: str  # מזהה OAuth (למשל Google sub)
    email: EmailStr
    full_name: Optional[str]
    plan: Literal["basic", "premium", "creator"] = "basic"
    registered_at: datetime
    last_login: Optional[datetime]

    # תשלומים
    stripe_customer_id: Optional[str] = None
    bank_account_id: Optional[str] = None

    # מידע מקצועי
    iracing_id: Optional[str]
    driver_category: Optional[Literal["GT3", "Formula", "Simracer"]]
    favorite_tracks: List[str] = Field(default_factory=list)

    # הרשאות
    is_admin: bool = False
    is_creator: bool = False

    class Config:
        orm_mode = True
