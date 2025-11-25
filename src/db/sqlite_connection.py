import sqlite3

class SqliteConnection:
    _instance = None

    def __init__(self, db_path="airline.db"):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row

    @classmethod
    def get_instance(cls, db_path="airline.db"):
        if cls._instance is None:
            cls._instance = cls(db_path)
        return cls._instance

    def cursor(self):
        return self.conn.cursor()

    def commit(self):
        self.conn.commit()

    # ----------------- init_db funksiyası -----------------
    def init_db(self):
        cur = self.conn.cursor()
        # Aircraft table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS aircraft (
            aircraft_id TEXT PRIMARY KEY,
            model TEXT NOT NULL,
            capacity INTEGER NOT NULL
        )
        """)
        # Flight table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS flights (
            flight_id INTEGER PRIMARY KEY AUTOINCREMENT,
            origin TEXT NOT NULL,
            destination TEXT NOT NULL,
            departure_time TEXT NOT NULL,
            arrival_time TEXT NOT NULL,
            aircraft_id TEXT NOT NULL,
            FOREIGN KEY (aircraft_id) REFERENCES aircraft(aircraft_id)
        )
        """)
        # Passenger table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS passengers (
            passenger_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT NOT NULL
        )
        """)
        # Ticket table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
            flight_id INTEGER NOT NULL,
            passenger_id INTEGER NOT NULL,
            seat_number TEXT NOT NULL,
            price REAL NOT NULL,
            FOREIGN KEY (flight_id) REFERENCES flights(flight_id),
            FOREIGN KEY (passenger_id) REFERENCES passengers(passenger_id)
        )
        """)
        self.conn.commit()


import logging
logger = logging.getLogger(__name__)