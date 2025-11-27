import unittest
import os
from src.models.flight import Flight
from src.repositories.flight_repository import FlightRepository
from src.db.sqlite_connection import SqliteConnection

TEST_DB = "airline_test.db"

class TestFlightRepository(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Əvvəlki test database-i sil
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)
        cls.conn = SqliteConnection.get_instance(TEST_DB)
        cls.repo = FlightRepository()

        # Flight cədvəli
        cur = cls.conn.cursor()
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
        cls.conn.commit()

    def test_create_and_read(self):
        flight = Flight(None, "Baku", "Istanbul", "2025-11-12 08:00", "2025-11-12 10:00", "AC123")
        fid = self.repo.create_flight(flight) 
        flights = self.repo.read_all()
        self.assertEqual(len(flights), 1)
        self.assertEqual(flights[0].flight_id, fid)
        self.assertEqual(flights[0].origin, "Baku")

    def test_delete(self):
        flight = Flight(None, "Paris", "London", "2025-11-13 09:00", "2025-11-13 10:30", "AC124")
        fid = self.repo.create_flight(flight)  
        self.repo.delete_flight(fid)           
        flights = self.repo.read_all()
        for f in flights:
            self.assertNotEqual(f.flight_id, fid)

if __name__ == "__main__":
    unittest.main()
