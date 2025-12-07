# src/repositories/flight_repository.py
from src.models.flight import Flight
from src.models.flight import FlightRecord, flight_from_dict
from src.utils.exceptions import NotFoundError
from src.repositories.base_repository import BaseRepository
from src.utils.exceptions import AlreadyExistsError

import logging
logger = logging.getLogger(__name__)

class FlightRepository(BaseRepository):
    def __init__(self):
        super().__init__("flights", Flight, id_column="flight_id")

    def create_flight(self, flight: Flight):
        # Accept either mutable Flight or immutable FlightRecord
        origin = getattr(flight, "origin")
        destination = getattr(flight, "destination")
        departure_time = getattr(flight, "departure_time")
        arrival_time = getattr(flight, "arrival_time")
        aircraft_id = getattr(flight, "aircraft_id")

        cur = self.conn.cursor()
        cur.execute("INSERT INTO flights (origin, destination, departure_time, arrival_time, aircraft_id) VALUES (?, ?, ?, ?, ?)",
                    (origin, destination, departure_time, arrival_time, aircraft_id))
        self.conn.commit()
        return cur.lastrowid

    def update_flight(self, flight: Flight):
        if not flight.flight_id:
            raise ValueError("flight_id is required for update")
        cur = self.conn.cursor()
        cur.execute("UPDATE flights SET origin = ?, destination = ?, departure_time = ?, arrival_time = ?, aircraft_id = ? WHERE flight_id = ?",
                    (flight.origin, flight.destination, flight.departure_time, flight.arrival_time, flight.aircraft_id, flight.flight_id))
        if cur.rowcount == 0:
            raise NotFoundError(f"Flight with ID {flight.flight_id} not found")
        self.conn.commit()
        return flight.flight_id

    def delete_flight(self, flight_id: int):
        # wrapper for CLI consistency
        self.delete(flight_id)

    # --- Record-based read helpers ---
    def read_by_id_record(self, id_value) -> FlightRecord | None:
        cur = self.conn.cursor()
        cur.execute(f"SELECT * FROM {self.table_name} WHERE {self.id_column} = ?", (id_value,))
        row = cur.fetchone()
        if not row:
            return None
        return flight_from_dict(dict(row))

    def read_all_records(self) -> list[FlightRecord]:
        cur = self.conn.cursor()
        cur.execute(f"SELECT * FROM {self.table_name}")
        rows = cur.fetchall()
        return [flight_from_dict(dict(r)) for r in rows]
