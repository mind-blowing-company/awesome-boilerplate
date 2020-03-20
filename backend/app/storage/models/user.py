from sqlalchemy import Column, Integer, String

from app.storage.db import Base


class User(Base):
    __tablename__ = "users"

    def __repr__(self):
        return f'User(id="{self.id}", username="{self.username}", password="{self.password}")'

    id = Column(Integer, primary_key=True)
    username = Column(String(15), nullable=False, unique=True)
    password = Column(String(200), nullable=False)
