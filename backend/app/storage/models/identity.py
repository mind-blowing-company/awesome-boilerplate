from sqlalchemy import Integer, Column, String, ForeignKey
from sqlalchemy.orm import relationship

from app.storage.db import Base


class Identity(Base):
    __tablename__ = "identities"

    def __repr__(self):
        return f'Identity(id="{self.id}", user_id="{self.user_id}", provider_id="{self.provider_id}", user={self.user})'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    provider_id = Column(String(200), nullable=False)
    user = relationship("User", back_populates="identities")
