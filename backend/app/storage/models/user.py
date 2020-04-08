from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.storage.db import Base


class User(Base):
    __tablename__ = "users"

    def __repr__(self):
        return f'User(id="{self.id}", username="{self.username}", password="{self.password}", email="{self.email}", identities={self.identities})'

    id = Column(Integer, primary_key=True)
    username = Column(String(200), nullable=False, unique=True)
    password = Column(String(200), nullable=False)
    email = Column(String(200), nullable=True, unique=True)
    identities = relationship("Identity", back_populates="user")
