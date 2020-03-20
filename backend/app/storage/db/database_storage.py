from typing import List, Type

from app.storage.db import Base
from app.storage.db.database_builder import DatabaseBuilder
from settings import DATABASE_ENGINE


class DatabaseStorage:
    def __init__(self, model: Type[Base], engine: str = DATABASE_ENGINE):
        self.model = model
        self.db_provider = DatabaseBuilder(database_engine=engine)

    def create(self, entity: Base) -> Base:
        session = self.db_provider.get_session()
        session.add(entity)
        session.commit()
        return entity

    def get(self, **kwargs) -> Base:
        return self._find_by(**kwargs).first()

    def get_all(self, **kwargs) -> List[Base]:
        return self._find_by(**kwargs).all()

    def _find_by(self, **kwargs):
        session = self.db_provider.get_session()
        return session.query(self.model).filter_by(**kwargs)
