from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


from ..database import Base


class CompletedTask(Base):
    __tablename__ = 'completed_tasks'

    id = Column(Integer, primary_key=True)
    description = Column(String)
    created_at = Column(DateTime, default=func.now())
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship('User', back_populates='completed_tasks')


class OpenTask(Base):
    __tablename__ = 'open_tasks'

    id = Column(Integer, primary_key=True)
    description = Column(String)
    created_at = Column(DateTime, default=func.now())
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship('User', back_populates='open_tasks')
    open_task = relationship('OpenTaskNotes', back_populates='open_task')


class OpenTaskNotes(Base):
    __tablename__ = 'open_task_notes'

    id = Column(Integer, primary_key=True)
    note = Column(String)

    open_task = relationship('OpenTask', back_populates='open_task_notes')
