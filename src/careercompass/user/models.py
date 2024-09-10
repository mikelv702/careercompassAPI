from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from ..database import Base


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