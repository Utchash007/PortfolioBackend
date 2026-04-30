from beanie import Document
from pydantic import Field
from typing import Optional
from datetime import datetime


class InitState(Document):
    state: int
    file_hash: Optional[str] = None
    createdAt: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "InitState"
