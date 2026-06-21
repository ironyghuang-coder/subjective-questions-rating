from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.web.api.usersApi import router as users_router
from src.web.api.docApi import router as doc_router
from fastapi.middleware.gzip import GZipMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],         # 允许所有源
    allow_credentials=True,
    allow_methods=["*"],         # 允许所有方法
    allow_headers=["*"],         # 允许所有请求头
)

#响应大小超过 1000 字节时自动压缩
app.add_middleware(GZipMiddleware, minimum_size=1000)

app.include_router(users_router)
app.include_router(doc_router)

