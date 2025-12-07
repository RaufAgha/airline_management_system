# src/repositories/aircraft_repository.py
from src.models.aircraft import Aircraft
from src.models.aircraft import AircraftRecord, aircraft_from_dict
from src.utils.exceptions import NotFoundError
from src.repositories.base_repository import BaseRepository
from src.utils.exceptions import AlreadyExistsError

import logging
logger = logging.getLogger(__name__)

class AircraftRepository(BaseRepository):
    def __init__(self):
        super().__init__("aircraft", Aircraft, id_column="aircraft_id")

    def create_aircraft(self, aircraft: Aircraft):
        if self.read_by_id(aircraft.aircraft_id):
            raise AlreadyExistsError(f"Aircraft ID {aircraft.aircraft_id} already exists")
        aid = getattr(aircraft, "aircraft_id")
        model = getattr(aircraft, "model")
        capacity = getattr(aircraft, "capacity")
        cur = self.conn.cursor()
        cur.execute("INSERT INTO aircraft (aircraft_id, model, capacity) VALUES (?, ?, ?)",
                    (aid, model, capacity))
        self.conn.commit()
        return aid

    def update_aircraft(self, aircraft: Aircraft):
        if not aircraft.aircraft_id:
            raise ValueError("aircraft_id is required for update")
        cur = self.conn.cursor()
        cur.execute("UPDATE aircraft SET model = ?, capacity = ? WHERE aircraft_id = ?",
                    (aircraft.model, aircraft.capacity, aircraft.aircraft_id))
        if cur.rowcount == 0:
            raise NotFoundError(f"Aircraft with ID {aircraft.aircraft_id} not found")
        self.conn.commit()
        return aircraft.aircraft_id

    def delete_aircraft(self, aircraft_id: int):
        self.delete(aircraft_id)

    # Record reads
    def read_by_id_record(self, id_value) -> AircraftRecord | None:
        cur = self.conn.cursor()
        cur.execute(f"SELECT * FROM {self.table_name} WHERE {self.id_column} = ?", (id_value,))
        row = cur.fetchone()
        if not row:
            return None
        return aircraft_from_dict(dict(row))

    def read_all_records(self) -> list[AircraftRecord]:
        cur = self.conn.cursor()
        cur.execute(f"SELECT * FROM {self.table_name}")
        rows = cur.fetchall()
        return [aircraft_from_dict(dict(r)) for r in rows]
