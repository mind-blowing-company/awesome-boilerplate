from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.storage.db import Base


class DatabaseBuilder:
    engine = None
    session = None

    def __init__(self, database_engine: str):
        self.db_engine = database_engine

    def _get_engine(self):
        if not self.engine:
            self.engine = create_engine(self.db_engine)
        return self.engine

    def get_session(self) -> Session:
        self._create_tables()
        return sessionmaker(bind=self._get_engine())()

    def _create_tables(self):
        Base.metadata.create_all(self._get_engine(), checkfirst=True)
