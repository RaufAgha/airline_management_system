from src.db.sqlite_connection import SqliteConnection
from src.utils.exceptions import NotFoundError, AlreadyExistsError

class BaseRepository:
    def __init__(self, table_name, model_class):
        self.conn = SqliteConnection.get_instance()
        self.table_name = table_name
        self.model_class = model_class

    def create(self, **kwargs):
        columns = ", ".join(kwargs.keys())
        placeholders = ", ".join(["?"] * len(kwargs))
        values = tuple(kwargs.values())
        cur = self.conn.cursor()
        cur.execute(f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})", values)
        self.conn.commit()
        return cur.lastrowid

    def read_all(self):
        cur = self.conn.cursor()
        cur.execute(f"SELECT * FROM {self.table_name}")
        rows = cur.fetchall()
        return [self.model_class(**dict(row)) for row in rows]

    def delete(self, id_column, id_value):
        cur = self.conn.cursor()
        cur.execute(f"DELETE FROM {self.table_name} WHERE {id_column} = ?", (id_value,))
        if cur.rowcount == 0:
            raise NotFoundError(f"{self.table_name[:-1].capitalize()} with ID {id_value} not found.")
        self.conn.commit()


import logging
logger = logging.getLogger(__name__)