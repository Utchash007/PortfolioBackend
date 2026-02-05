from beanie import Document
from pydantic import BaseModel,Field
from typing import Optional
from datetime import datetime
class InitState(Document):
    state: int
    createdAt: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name ="InitState"