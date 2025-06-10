# services/user_service.py

from models.user import User
from sqlalchemy.orm import Session
from datetime import datetime

# מחפש משתמש לפי ID, מחזיר None אם לא נמצא
def get_user_by_id(user_id: str, db: Session) -> User | None:
    return db.query(User).filter(User.id == user_id).first()

# בודק אם המשתמש קיים, ואם לא – יוצר אותו
def create_user_if_not_exists(user_id: str, email: str, db: Session) -> User:
    user = get_user_by_id(user_id, db)
    if user:
        return user

    new_user = User(
        id=user_id,
        email=email,
        registered_at=datetime.utcnow()
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
