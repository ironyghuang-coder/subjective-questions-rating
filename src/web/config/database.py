# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import logging

# SQLite 数据库（适合开发）
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:root123@localhost/subject_rating_dev"

# 1. 配置 logging
logging.basicConfig()
# 获取 sqlalchemy.engine 的 logger
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# 创建数据库引擎
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 声明基类
class Base(DeclarativeBase):
    pass