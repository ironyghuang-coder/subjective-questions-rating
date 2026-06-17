from pydantic import BaseModel

class UserItem(BaseModel):
    id: int
    user_name: str
    user_id: int
    wid: str
    phone: str
    email: str
    hashed_password: str
    is_active: bool
    is_locked: bool
    