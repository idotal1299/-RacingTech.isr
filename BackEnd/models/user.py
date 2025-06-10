from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Literal, List, Dict
from datetime import datetime


class User(BaseModel):
    id: str  # מזהה OAuth (למשל Google sub)
    email: EmailStr
    full_name: Optional[str]
    plan: Literal["basic", "premium", "creator"] = "basic"
    registered_at: datetime
    last_login: Optional[datetime]

    # 💳 תשלומים
    stripe_customer_id: Optional[str] = None
    bank_account_id: Optional[str] = None  # חשבון בנק לשיוך יוצר

    # 📊 מידע מקצועי
    iracing_id: Optional[str]
    driver_category: Optional[Literal["GT3", "Formula", "Simracer"]]
    favorite_tracks: List[str] = Field(default_factory=list)

    # 👮 הרשאות
    is_admin: bool = False
    is_creator: bool = False

    # 📈 עתיד: סטטיסטיקות, תגיות
    stats: Optional[Dict[str, float]] = Field(default_factory=dict)  # לדוגמה: consistency, avg pace
    tags: List[str] = Field(default_factory=list)  # לדוגמה: ["aggressive", "clean", "defensive"]

    @staticmethod
    def get_by_id(user_id: str):
        from database.postgres import get_db 
        conn = get_db()
        cursor = conn.cursor()

        # שלב 1: טען נתוני משתמש
        cursor.execute("""
            SELECT email, full_name, plan, registered_at, last_login,
                   stripe_customer_id, bank_account_id,
                   iracing_id, driver_category, is_admin, is_creator
            FROM users WHERE id = %s
        """, (user_id,))
        row = cursor.fetchone()
        if not row:
            return None

        # שלב 2: טען favorite_tracks (בעתיד אם תיצור טבלה נפרדת)
        favorite_tracks = []
        try:
            cursor.execute("SELECT track_id FROM user_favorite_tracks WHERE user_id = %s", (user_id,))
            favorite_tracks = [r[0] for r in cursor.fetchall()]
        except:
            pass  # אם אין טבלה עדיין

        return User(
            id=user_id,
            email=row[0],
            full_name=row[1],
            plan=row[2],
            registered_at=row[3],
            last_login=row[4],
            stripe_customer_id=row[5],
            bank_account_id=row[6],
            iracing_id=row[7],
            driver_category=row[8],
            favorite_tracks=favorite_tracks,
            is_admin=row[9],
            is_creator=row[10],
            stats={},     # בעתיד: ממסד נתונים
            tags=[]       # בעתיד: תגיות
        )
