from sqlalchemy import create_engine

from app.storage.db import Base


class DatabaseBuilder:
    engine = None
    session = None

    def __init__(self, database_engine: str):
        self.db_engine = database_engine
        Base.metadata.create_all(self._get_engine(), checkfirst=True)

    def _get_engine(self):
        if not self.engine:
            if "sqlite" in self.db_engine:
                self.engine = create_engine(self.db_engine)
            else:
                self.engine = create_engine(self.db_engine, pool_size=20, max_overflow=0)

        return self.engine

    def get_connection(self):
        return self._get_engine().connect()
