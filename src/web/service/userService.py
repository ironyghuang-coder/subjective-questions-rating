from sqlalchemy.orm import Session
from src.web.model.user import User
from src.web.dto.userItem import UserItem

def get_user(db: Session, user_id: int) -> type[User] | None:
    return db.query(User).filter(User.id == user_id).first()


def create_user(db: Session, user: UserItem):
    """创建用户"""
    fake_hashed_password = user.password + "notreallyhashed"  # 实际应使用 passlib 哈希
    db_user = User(
        user_name=user.user_name,
        wid=user.wid,
        phone=user.phone,
        email=user.email,
        hashed_password=fake_hashed_password
    )
    db.add(db_user)
    db.commit()        # 提交事务
    db.refresh(db_user)  # 刷新对象，获取数据库生成的 id
    return db_user