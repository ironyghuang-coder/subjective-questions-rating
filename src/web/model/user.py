from src.web.config.database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime

class User(Base):
    __tablename__ = "users"  # 表名

    id = Column(Integer, primary_key=True, index=True)  # 主键，自增
    user_name = Column(String)
    wid = Column(String, unique=True, index=True)        # 微信ID 唯一，建索引
    phone = Column(String, unique=True, index=True)      # 手机号码 唯一，建索引
    email = Column(String, unique=True, index=True)      # 邮件 唯一，建索引
    hashed_password = Column(String)                     # 哈希密码
    is_active = Column(Boolean, default=True)            # 是否活跃
    is_locked = Column(Boolean, default=True)            # 是否锁定
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
