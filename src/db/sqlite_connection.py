import sqlite3

class SqliteConnection:
    # Allow one connection instance per database path to avoid tests/CLI sharing the wrong DB
    _instances = {}

    def __init__(self, db_path="airline.db"):
        self.db_path = db_path
        # Increase timeout to reduce 'database is locked' errors under contention
        # Allow cross-thread use in case caller uses threads (check_same_thread=False)
        # Note: disabling check_same_thread transfers responsibility for thread-safety to the caller.
        self.conn = sqlite3.connect(db_path, timeout=30.0, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        # Enforce foreign key constraints and enable WAL for better concurrency
        try:
            self.conn.execute("PRAGMA foreign_keys = ON")
            # Enable Write-Ahead Logging to reduce write lock contention
            self.conn.execute("PRAGMA journal_mode = WAL")
            # Use a reasonable synchronous level for performance
            self.conn.execute("PRAGMA synchronous = NORMAL")
        except Exception:
            pass

    @classmethod
    def get_instance(cls, db_path="airline.db"):
        # Return a cached instance for the requested db_path, create if missing
        if db_path not in cls._instances:
            cls._instances[db_path] = cls(db_path)
        return cls._instances[db_path]

    def cursor(self):
        return self.conn.cursor()

    def commit(self):
        self.conn.commit()

    def init_db(self):
        cur = self.conn.cursor()

        cur.execute("""
        CREATE TABLE IF NOT EXISTS aircraft (
            aircraft_id TEXT PRIMARY KEY,
            model TEXT NOT NULL,
            capacity INTEGER NOT NULL
        )
        """)

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

        cur.execute("""
        CREATE TABLE IF NOT EXISTS passengers (
            passenger_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT NOT NULL
        )
        """)

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

    def close(self):
        try:
            self.conn.close()
        except Exception:
            pass
