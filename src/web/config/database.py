# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# SQLite 数据库（适合开发）
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:root123@localhost/third_model"

# 创建数据库引擎
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# 声明基类
class Base(DeclarativeBase):
    pass