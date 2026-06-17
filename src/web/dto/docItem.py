from pydantic import BaseModel


class DocItem(BaseModel):
    topic: str
    description: str | None = None  # 可选
    content: str
    category: str | None = None     # 可选