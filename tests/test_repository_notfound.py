import unittest
import os

from src.db.sqlite_connection import SqliteConnection
from src.repositories.passenger_repository import PassengerRepository
from src.repositories.flight_repository import FlightRepository
from src.repositories.aircraft_repository import AircraftRepository
from src.repositories.ticket_repository import TicketRepository
from src.utils.exceptions import NotFoundError

TEST_DB = "airline_test.db"


class TestRepositoryNotFound(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Ensure a fresh test database (best-effort)
        if os.path.exists(TEST_DB):
            try:
                os.remove(TEST_DB)
            except PermissionError:
                print(f"Warning: could not remove {TEST_DB} (in use). Tests will attempt to reuse/clean it.")
        cls.conn = SqliteConnection.get_instance(TEST_DB)

        # Create simple tables required by repositories
        cur = cls.conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS passengers (
            passenger_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT
        )
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS flights (
            flight_id INTEGER PRIMARY KEY AUTOINCREMENT,
            origin TEXT NOT NULL,
            destination TEXT NOT NULL,
            departure_time TEXT NOT NULL,
            arrival_time TEXT NOT NULL,
            aircraft_id TEXT NOT NULL
        )
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS aircraft (
            aircraft_id INTEGER PRIMARY KEY,
            model TEXT NOT NULL,
            capacity INTEGER NOT NULL
        )
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
            flight_id INTEGER NOT NULL,
            passenger_id INTEGER NOT NULL,
            seat_number TEXT NOT NULL,
            price REAL NOT NULL
        )
        """)

        cls.conn.commit()

        cls.passenger_repo = PassengerRepository()
        cls.flight_repo = FlightRepository()
        cls.aircraft_repo = AircraftRepository()
        cls.ticket_repo = TicketRepository()

    def setUp(self):
        # Clean tables before each test
        cur = self.conn.cursor()
        cur.execute("DELETE FROM tickets")
        cur.execute("DELETE FROM flights")
        cur.execute("DELETE FROM passengers")
        cur.execute("DELETE FROM aircraft")
        self.conn.commit()

    def test_update_nonexistent_passenger_raises(self):
        from src.models.passenger import Passenger
        p = Passenger(9999, "No One", "noone@example.com", "000")
        with self.assertRaises(NotFoundError):
            self.passenger_repo.update_passenger(p)

    def test_delete_nonexistent_passenger_raises(self):
        with self.assertRaises(NotFoundError):
            self.passenger_repo.delete_passenger(9999)

    def test_update_nonexistent_flight_raises(self):
        from src.models.flight import Flight
        f = Flight(9999, "A", "B", "2025-01-01 00:00", "2025-01-01 01:00", "AC0")
        with self.assertRaises(NotFoundError):
            self.flight_repo.update_flight(f)

    def test_delete_nonexistent_flight_raises(self):
        with self.assertRaises(NotFoundError):
            self.flight_repo.delete_flight(9999)

    def test_update_nonexistent_aircraft_raises(self):
        from src.models.aircraft import Aircraft
        a = Aircraft(9999, "X", 10)
        with self.assertRaises(NotFoundError):
            self.aircraft_repo.update_aircraft(a)

    def test_delete_nonexistent_aircraft_raises(self):
        with self.assertRaises(NotFoundError):
            self.aircraft_repo.delete_aircraft(9999)

    def test_update_nonexistent_ticket_raises(self):
        from src.models.ticket import Ticket
        t = Ticket(9999, 1, 1, "1A", 100.0)
        with self.assertRaises(NotFoundError):
            self.ticket_repo.update_ticket(t)

    def test_delete_nonexistent_ticket_raises(self):
        with self.assertRaises(NotFoundError):
            self.ticket_repo.delete_ticket(9999)


if __name__ == "__main__":
    unittest.main()
