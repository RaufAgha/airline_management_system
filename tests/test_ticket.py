import unittest
import os
from src.models.ticket import Ticket
from src.repositories.ticket_repository import TicketRepository
from src.db.sqlite_connection import SqliteConnection

TEST_DB = "airline_test.db"

class TestTicketRepository(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        if os.path.exists(TEST_DB):
            try:
                os.remove(TEST_DB)
            except PermissionError:
                print(f"Warning: could not remove {TEST_DB} (in use). Tests will attempt to reuse/clean it.")
        cls.conn = SqliteConnection.get_instance(TEST_DB)
        cls.repo = TicketRepository()

        cur = cls.conn.cursor()
        # Lazımi cədvəllər
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
            email TEXT NOT NULL,
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

        # Test üçün Flight və Passenger əlavə edirik
        cur.execute("INSERT INTO flights (origin,destination,departure_time,arrival_time,aircraft_id) VALUES ('Baku','Istanbul','2025-11-12 08:00','2025-11-12 10:00','AC123')")
        cls.flight_id = cur.lastrowid
        cur.execute("INSERT INTO passengers (name,email,phone) VALUES ('John Doe','john@example.com','123456789')")
        cls.passenger_id = cur.lastrowid
        cls.conn.commit()

    def setUp(self):
        # Hər testdən əvvəl tickets cədvəlini təmizlə
        cur = self.conn.cursor()
        cur.execute("DELETE FROM tickets")
        self.conn.commit()

    def test_create_and_read(self):
        ticket = Ticket(None, self.flight_id, self.passenger_id, "12A", 100.0)
<<<<<<< HEAD
        tid = self.repo.create_ticket(ticket)
=======
        tid = self.repo.create_ticket(ticket)  
>>>>>>> e6117d3378075bac6133ff2fe9f6ee053617e09b
        tickets = self.repo.read_all()
        self.assertEqual(len(tickets), 1)
        self.assertEqual(tickets[0].ticket_id, tid)
        self.assertEqual(tickets[0].seat_number, "12A")

    def test_delete(self):
        ticket = Ticket(None, self.flight_id, self.passenger_id, "14B", 120.0)
<<<<<<< HEAD
        tid = self.repo.create_ticket(ticket)
        self.repo.delete_ticket(tid)
=======
        tid = self.repo.create_ticket(ticket)  
        self.repo.delete_ticket(tid)          
>>>>>>> e6117d3378075bac6133ff2fe9f6ee053617e09b
        tickets = self.repo.read_all()
        self.assertTrue(all(t.ticket_id != tid for t in tickets))

if __name__ == "__main__":
    unittest.main()
