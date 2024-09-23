from datetime import datetime

from pydantic import BaseModel


class CreateProjectSchema(BaseModel):
    title: str
    description: str
    estimated_due: datetime
    custom_status: str
    completed: bool
    status_note: str

class ProjectSchema(CreateProjectSchema):
    id: int
    user_id: int
    created_at: datetime

