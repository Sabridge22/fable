from datetime import datetime
from pydantic import BaseModel

class MessageCreateSchema(BaseModel):
    content: str


class MessageResponseSchema(BaseModel):
    id: str
    user_id: str
    content: str
    role: str
    created_at: datetime

    class Config:
        from_attributes = True