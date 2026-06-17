from sqlalchemy.orm import Session
from src.web.model.user import User

def get_user(db: Session, user_id: int) -> type[User] | None:
    return db.query(User).filter(User.id == user_id).first()