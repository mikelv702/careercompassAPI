from datetime import datetime

from pydantic import BaseModel


class CompletedTaskBase(BaseModel):
    id: int
    description: str = None
    created_at: datetime = None


class CreateCompletedTask(BaseModel):
    description: str


class OpenTaskBase(BaseModel):
    id: int
    description: str = None
    created_at: datetime = None
    notes: list[OpenTaskNoteDisplay] = None

class OpenTaskCreate(BaseModel):
    description: str


class OpenTaskNoteCreate(BaseModel):
    note: str


class OpenTaskNoteDisplay(OpenTaskNoteCreate):
    id: int