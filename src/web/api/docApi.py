from datetime import datetime

from fastapi import APIRouter

from src.web.dto.docItem import DocItem
from src.web.dto.docSample import DocSample
from src.web.service.docService import DocService
from src.web.service.vectorService import VectorService
from fastapi import Depends
from src.web.service.userService import get_current_active_user

router = APIRouter(dependencies=[Depends(get_current_active_user)])

@router.get("/health", tags=["系统"])
async def health_check():
    """系统健康检查"""
    return {
        "status": "healthy",
        "timestamp": datetime.now()
    }

@router.post("/analyse_doc_item")
async def create_doc_item(doc_item: DocItem):
    doc_service = DocService()
    response = doc_service.send_doc_item(doc_item)
    return {"doc_analyse": response, "timestamp": datetime.now()}

@router.post("/create_doc_sample")
async def create_doc_sample(doc_sample: DocSample):
    vector_service = VectorService()
    doc_sample_memory_id = vector_service.save_doc_sample(doc_sample)
    return {"doc_sample_memory_id": doc_sample_memory_id, "timestamp": datetime.now()}

@router.delete("/clean_doc_sample")
async def clean_doc_sample():
    vector_service = VectorService()
    deleted_memories = vector_service.clean_all_doc_sample()
    return {"doc_sample_memory_id": deleted_memories, "timestamp": datetime.now()}