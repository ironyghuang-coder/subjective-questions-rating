from pydantic import BaseModel

class UserItem(BaseModel):
    id: int | None = None
    user_name: str
    wid: str
    phone: str
    email: str
    password: str
    is_active: int | None = None
    is_locked: int | None = None

