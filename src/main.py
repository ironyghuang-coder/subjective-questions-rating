from fastapi import Depends, FastAPI, HTTPException
from datetime import datetime
from src.web.config.database import get_db
from src.web.service import userService
from web.dto.docItem import DocItem
from web.dto.docSample import DocSample
from src.web.service.docService import DocService
from src.web.service.vectorService import VectorService
from sqlalchemy.orm import Session
from src.web.dto.userItem import UserItem

# 创建 FastAPI 应用实例
app = FastAPI()


# 定义根路径的 GET 路由
# 健康检查端点
@app.get("/health", tags=["系统"])
async def health_check():
    """系统健康检查"""
    return {
        "status": "healthy",
        "timestamp": datetime.now()
    }

@app.post("/analyse_doc_item")
async def create_doc_item(doc_item: DocItem):
    doc_service = DocService()
    response = doc_service.send_doc_item(doc_item)
    return {"doc_analyse": response, "timestamp": datetime.now()}

@app.post("/create_doc_sample")
async def create_doc_sample(doc_sample: DocSample):
    vector_service = VectorService()
    doc_sample_memory_id = vector_service.save_doc_sample(doc_sample)
    return {"doc_sample_memory_id": doc_sample_memory_id, "timestamp": datetime.now()}

@app.delete("/clean_doc_sample")
async def clean_doc_sample():
    vector_service = VectorService()
    deleted_memories = vector_service.clean_all_doc_sample()
    return {"doc_sample_memory_id": deleted_memories, "timestamp": datetime.now()}

@app.get("/users/{user_id}")
async def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = userService.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="用户不存在")
    return db_user

@app.post("/users/")
def create_user(user: UserItem, db: Session = Depends(get_db)):
    return userService.create_user(db=db, user=user)