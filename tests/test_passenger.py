import unittest
import os
from src.models.passenger import Passenger
from src.repositories.passenger_repository import PassengerRepository
from src.db.sqlite_connection import SqliteConnection

TEST_DB = "airline_test.db"

class TestPassengerRepository(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)
        cls.conn = SqliteConnection.get_instance(TEST_DB)
        cls.repo = PassengerRepository()

        cur = cls.conn.cursor()
        cur.execute("""
        CREATE TABLE passengers (
            passenger_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT
        )
        """)
        cls.conn.commit()

    def test_create_and_read(self):
        passenger = Passenger(None, "John Doe", "john@example.com", "123456789")
        pid = self.repo.create_passenger(passenger)  # <- dəyişiklik
        passengers = self.repo.read_all()
        self.assertEqual(len(passengers), 1)
        self.assertEqual(passengers[0].passenger_id, pid)
        self.assertEqual(passengers[0].name, "John Doe")

    def test_delete(self):
        passenger = Passenger(None, "Jane Doe", "jane@example.com", "987654321")
        pid = self.repo.create_passenger(passenger)  # <- dəyişiklik
        self.repo.delete_passenger(pid)              # <- dəyişiklik
        passengers = self.repo.read_all()
        for p in passengers:
            self.assertNotEqual(p.passenger_id, pid)

if __name__ == "__main__":
    unittest.main()
