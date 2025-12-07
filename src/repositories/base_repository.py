# src/repositories/base_repository.py
from src.db.sqlite_connection import SqliteConnection
from src.utils.exceptions import NotFoundError
import logging

logger = logging.getLogger(__name__)

class BaseRepository:
    def __init__(self, table_name: str, model_class, id_column: int = None):
        # Prefer the most recently created SqliteConnection instance (useful for tests
        # where a test DB is created via SqliteConnection.get_instance(TEST_DB)
        instances = getattr(SqliteConnection, '_instances', {})
        if instances:
            # dict preserves insertion order; pick the last-created instance
            self.conn = list(instances.values())[-1]
        else:
            self.conn = SqliteConnection.get_instance()
        self.table_name = table_name
        self.model_class = model_class
        self.id_column = id_column or f"{table_name[:-1]}_id"

    def read_all(self):
        cur = self.conn.cursor()
        cur.execute(f"SELECT * FROM {self.table_name}")
        rows = cur.fetchall()
        return [self.model_class(**dict(row)) for row in rows]

    def read_by_id(self, id_value):
        cur = self.conn.cursor()
        cur.execute(f"SELECT * FROM {self.table_name} WHERE {self.id_column} = ?", (id_value,))
        row = cur.fetchone()
        if not row:
            return None
        return self.model_class(**dict(row))

    def delete(self, id_value):
        cur = self.conn.cursor()
        cur.execute(f"DELETE FROM {self.table_name} WHERE {self.id_column} = ?", (id_value,))
        # If no rows were affected, the item did not exist
        if cur.rowcount == 0:
            raise NotFoundError(f"{self.table_name[:-1].capitalize()} with ID {id_value} not found")
        self.conn.commit()
        logger.info(f"{self.table_name.capitalize()} with ID {id_value} deleted")
