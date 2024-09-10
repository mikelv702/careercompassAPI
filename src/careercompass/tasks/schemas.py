from datetime import datetime

from pydantic import BaseModel


class CompletedTaskBase(BaseModel):
    id: int
    description: str = None
    created_at: datetime = None


class CreateCompletedTask(BaseModel):
    description: str
