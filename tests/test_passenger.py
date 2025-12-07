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
            try:
                os.remove(TEST_DB)
            except PermissionError:
                # file may be locked by another process; continue and let tests clear tables
                print(f"Warning: could not remove {TEST_DB} (in use). Tests will attempt to reuse/clean it.")
        cls.conn = SqliteConnection.get_instance(TEST_DB)
        cls.repo = PassengerRepository()

        cur = cls.conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS passengers (
            passenger_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT
        )
        """)
        cls.conn.commit()

    def setUp(self):
        # Hər testdən əvvəl cədvəli təmizlə
        cur = self.conn.cursor()
        cur.execute("DELETE FROM passengers")
        self.conn.commit()

    def test_create_and_read(self):
        passenger = Passenger(None, "John Doe", "john@example.com", "123456789")
<<<<<<< HEAD
        pid = self.repo.create_passenger(passenger)
=======
        pid = self.repo.create_passenger(passenger)  
>>>>>>> e6117d3378075bac6133ff2fe9f6ee053617e09b
        passengers = self.repo.read_all()
        self.assertEqual(len(passengers), 1)
        self.assertEqual(passengers[0].passenger_id, pid)
        self.assertEqual(passengers[0].name, "John Doe")
        self.assertEqual(passengers[0].email, "john@example.com")

    def test_delete(self):
        passenger = Passenger(None, "Jane Doe", "jane@example.com", "987654321")
<<<<<<< HEAD
        pid = self.repo.create_passenger(passenger)
        self.repo.delete_passenger(pid)
=======
        pid = self.repo.create_passenger(passenger) 
        self.repo.delete_passenger(pid)              
>>>>>>> e6117d3378075bac6133ff2fe9f6ee053617e09b
        passengers = self.repo.read_all()
        self.assertTrue(all(p.passenger_id != pid for p in passengers))

if __name__ == "__main__":
    unittest.main()
