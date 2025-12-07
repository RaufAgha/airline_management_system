import os
import unittest
from src.db.sqlite_connection import SqliteConnection
from src.repositories.ticket_repository import TicketRepository
from src.repositories.passenger_repository import PassengerRepository
from src.repositories.flight_repository import FlightRepository
from src.services.booking_service import BookingService
from src.models.ticket import Ticket
from src.utils.exceptions import NotFoundError, InvalidInputError

TEST_DB = "airline_test.db"


class TestBookingService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if os.path.exists(TEST_DB):
            try:
                os.remove(TEST_DB)
            except PermissionError:
                pass
        cls.conn = SqliteConnection.get_instance(TEST_DB)
        # create tables
        cur = cls.conn.cursor()
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
        CREATE TABLE IF NOT EXISTS passengers (
            passenger_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT
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

    def setUp(self):
        # use repositories and service
        self.ticket_repo = TicketRepository()
        self.passenger_repo = PassengerRepository()
        self.flight_repo = FlightRepository()
        self.booking_service = BookingService(self.ticket_repo, self.passenger_repo, self.flight_repo)
        # clear tables
        cur = self.conn.cursor()
        cur.execute("DELETE FROM tickets")
        cur.execute("DELETE FROM passengers")
        cur.execute("DELETE FROM flights")
        self.conn.commit()

    def test_create_ticket_with_missing_flight_raises(self):
        # create a passenger only
        cur = self.conn.cursor()
        cur.execute("INSERT INTO passengers (name,email,phone) VALUES ('Alice','alice@example.com','123')")
        pid = cur.lastrowid
        self.conn.commit()

        ticket = Ticket(None, 999999, pid, '1A', 50.0)
        with self.assertRaises(NotFoundError):
            self.booking_service.create_ticket(ticket)

    def test_create_ticket_with_invalid_ids_raises(self):
        ticket = Ticket(None, 'not-an-int', 'also-not-int', '1A', 50.0)
        with self.assertRaises(InvalidInputError):
            self.booking_service.create_ticket(ticket)


if __name__ == "__main__":
    unittest.main()
