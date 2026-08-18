from datetime import datetime
from pydantic import BaseModel, ConfigDict

class MessageCreateSchema(BaseModel):
    content: str


class MessageResponseSchema(BaseModel):
    id: str
    user_id: str
    content: str
    role: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)