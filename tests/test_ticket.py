import unittest
import os
from src.models.ticket import Ticket
from src.repositories.ticket_repository import TicketRepository
from src.db.sqlite_connection import SqliteConnection

TEST_DB = "airline_test.db"

class TestTicketRepository(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Əvvəlki test database-i sil
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)
        cls.conn = SqliteConnection.get_instance(TEST_DB)
        cls.repo = TicketRepository()

        cur = cls.conn.cursor()
        # Flight və Passenger cədvəlləri Ticket üçün lazımdır
        cur.execute("""
        CREATE TABLE flights (
            flight_id INTEGER PRIMARY KEY AUTOINCREMENT,
            origin TEXT NOT NULL,
            destination TEXT NOT NULL,
            departure_time TEXT NOT NULL,
            arrival_time TEXT NOT NULL,
            aircraft_id TEXT NOT NULL
        )
        """)
        cur.execute("""
        CREATE TABLE passengers (
            passenger_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT
        )
        """)
        cur.execute("""
        CREATE TABLE tickets (
            ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
            flight_id INTEGER NOT NULL,
            passenger_id INTEGER NOT NULL,
            seat_number TEXT,
            FOREIGN KEY(flight_id) REFERENCES flights(flight_id),
            FOREIGN KEY(passenger_id) REFERENCES passengers(passenger_id)
        )
        """)
        cls.conn.commit()

        # Test üçün Flight və Passenger əlavə edirik
        cur.execute("INSERT INTO flights (origin,destination,departure_time,arrival_time,aircraft_id) VALUES ('Baku','Istanbul','2025-11-12 08:00','2025-11-12 10:00','AC123')")
        cls.flight_id = cur.lastrowid
        cur.execute("INSERT INTO passengers (name,email,phone) VALUES ('John Doe','john@example.com','123456789')")
        cls.passenger_id = cur.lastrowid
        cls.conn.commit()

    def test_create_and_read(self):
        ticket = Ticket(None, self.flight_id, self.passenger_id, "12A")
        tid = self.repo.create(ticket)
        tickets = self.repo.read_all()
        self.assertEqual(len(tickets), 1)
        self.assertEqual(tickets[0].ticket_id, tid)
        self.assertEqual(tickets[0].seat_number, "12A")

    def test_delete(self):
        ticket = Ticket(None, self.flight_id, self.passenger_id, "14B")
        tid = self.repo.create(ticket)
        self.repo.delete(tid)
        tickets = self.repo.read_all()
        for t in tickets:
            self.assertNotEqual(t.ticket_id, tid)

if __name__ == "__main__":
    unittest.main()
