from sqlalchemy.orm import Session
from src.web.model.userEntity import User
from src.web.dto.userItem import UserItem
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from src.web.config.database import get_db

SECRET_KEY = "secret-key-keep-it-secret"  # 生产环境使用环境变量
ALGORITHM = "HS256"

# ===== 密码哈希 =====
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ===== OAuth2 方案 =====
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_user_by_user_id(db: Session, user_id: int) -> type[User] | None:
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_user_name(db: Session, username: str) -> type[User] | None:
    return db.query(User).filter(User.user_name == username).first()


def create_user(db: Session, user: UserItem):
    """创建用户"""
    hashed_password = get_password_hash(user.password)
    db_user = User(
        user_name=user.user_name,
        wid=user.wid,
        phone=user.phone,
        email=user.email,
        hashed_password=hashed_password,
        is_active = user.is_active if user.is_active is not None else 1,
        is_locked = user.is_locked if user.is_locked is not None else 0,
        created_at = datetime.now(),
        updated_at = datetime.now()
    )
    db.add(db_user)
    db.commit()        # 提交事务
    db.refresh(db_user)  # 刷新对象，获取数据库生成的 id
    return db_user

def authenticate_by_username_password(db: Session, username: str, password: str)->type[User] | None:
    """验证用户凭据"""
    user = get_user_by_user_name(db, username)
    if user is None:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """创建 JWT 访问令牌"""
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],db: Session = Depends(get_db)) -> type[User] | None:
    """从令牌中获取当前用户（依赖函数）"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user_by_user_name(db, username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.is_locked==1:
        raise HTTPException(status_code=400, detail="用户已被禁用")
    return current_user


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """生成密码哈希"""
    return pwd_context.hash(password)