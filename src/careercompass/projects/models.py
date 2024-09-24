from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Boolean
from sqlalchemy.sql import func


from ..database import Base


class ProjectsModel(Base):
    __tablename__ = 'cc_projects'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String)
    description = Column(String)
    custom_status = Column(String)
    completed = Column(Boolean)
    created_at = Column(DateTime, default=func.now())
    estimated_due = Column(DateTime)
    status_note = Column(String)
