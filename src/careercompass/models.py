from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


# class CompletedTask(Base):
#     __tablename__ = 'completed_tasks'

#     id = Column(Integer, primary_key=True)
#     description = Column(String)
#     created_at = Column(DateTime, default=func.now())
#     user_id = Column(Integer, ForeignKey('users.id'))

#     user = relationship('User', back_populates='completed_tasks')


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    full_name = Column(String)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=False)

    completed_tasks = relationship('CompletedTask', back_populates='user')

    def get_display_name(self) -> str: 
        # Later this should return nickname once implemented.
        return self.email