from typing import Type

from app.storage.db import Base
from app.storage.db.database_builder import DatabaseBuilder
from settings import DATABASE_ENGINE


class DatabaseStorage:
    def __init__(self, model: Type[Base], engine: str = DATABASE_ENGINE):
        self.model = model
        self.db_provider = DatabaseBuilder(database_engine=engine)

    def create(self, entity):
        with self.db_provider.get_connection() as connection:
            command = Base.metadata.tables[self.model.__tablename__].insert()
            data = self._get_data(entity)
            result = connection.execute(command, data)
            new_entity_id = result.inserted_primary_key[0]

        return self.get(id=new_entity_id)

    def get(self, **kwargs):
        query = self._find_by(**kwargs)

        if len(query):
            database_row = query[0]
            return self.model(**dict(database_row))

    def update(self, entity):
        data = self._get_data(entity)
        fields = [f"{key}='{data[key]}'" for key in data.keys()]
        fields_string = ", ".join(fields)
        command = f"update {self.model.__tablename__} set {fields_string} where id={entity.id}"

        with self.db_provider.get_connection() as connection:
            connection.execute(command)

        return self.get(id=entity.id)

    def _get_data(self, entity):
        entity_dict = entity.__dict__
        return {key: entity_dict[key] for key in entity_dict if not key.startswith("_")}

    def _find_by(self, **kwargs):
        command = f"select * from {self.model.__tablename__}"

        if kwargs:
            conditions = []
            for key in kwargs.keys():
                conditions.append(f"{key}='{kwargs[key]}'")
            conditions = " and ".join(conditions)
            command += f" where {conditions}"

        with self.db_provider.get_connection() as connection:
            result_proxy = connection.execute(command)
            result = list(result_proxy)

        return result
