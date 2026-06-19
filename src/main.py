from fastapi import FastAPI
from src.web.api.usersApi import router as users_router
from src.web.api.docApi import router as doc_router


app = FastAPI()

app.include_router(users_router)
app.include_router(doc_router)

