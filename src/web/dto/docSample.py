from pydantic import BaseModel

class DocSample(BaseModel):
    topic: str
    score: float
    content: str
    category: str
    importance: float