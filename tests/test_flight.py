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
            try:
                os.remove(TEST_DB)
            except PermissionError:
                print(f"Warning: could not remove {TEST_DB} (in use). Tests will attempt to reuse/clean it.")
        cls.conn = SqliteConnection.get_instance(TEST_DB)
        cls.repo = FlightRepository()

        # Flight cədvəlini yarat
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
        cls.conn.commit()

    def setUp(self):
        # Hər testdən əvvəl flights cədvəlini təmizlə
        cur = self.conn.cursor()
        cur.execute("DELETE FROM flights")
        self.conn.commit()

    def test_create_and_read(self):
        flight = Flight(None, "Baku", "Istanbul", "2025-11-12 08:00", "2025-11-12 10:00", "AC123")
<<<<<<< HEAD
        fid = self.repo.create_flight(flight)
=======
        fid = self.repo.create_flight(flight) 
>>>>>>> e6117d3378075bac6133ff2fe9f6ee053617e09b
        flights = self.repo.read_all()
        self.assertEqual(len(flights), 1)
        self.assertEqual(flights[0].flight_id, fid)
        self.assertEqual(flights[0].origin, "Baku")
        self.assertEqual(flights[0].destination, "Istanbul")

    def test_delete(self):
        flight = Flight(None, "Paris", "London", "2025-11-13 09:00", "2025-11-13 10:30", "AC124")
<<<<<<< HEAD
        fid = self.repo.create_flight(flight)
        self.repo.delete_flight(fid)
=======
        fid = self.repo.create_flight(flight)  
        self.repo.delete_flight(fid)           
>>>>>>> e6117d3378075bac6133ff2fe9f6ee053617e09b
        flights = self.repo.read_all()
        self.assertTrue(all(f.flight_id != fid for f in flights))

if __name__ == "__main__":
    unittest.main()
