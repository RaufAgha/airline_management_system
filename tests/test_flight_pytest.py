import os
import pytest
from src.models.flight import Flight
from src.repositories.flight_repository import FlightRepository
from src.db.sqlite_connection import SqliteConnection

TEST_DB = "airline_test.db"

@pytest.fixture(scope="module")
def conn_and_repo():
    # remove old DB
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    conn = SqliteConnection.get_instance(TEST_DB)
    repo = FlightRepository()
    # create table
    cur = conn.cursor()
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
    conn.commit()
    yield repo
    # teardown
    try:
        conn.conn.close()
    except Exception:
        pass
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

@pytest.fixture(autouse=True)
def clear_table():
    # ensure table empty before each test
    conn = SqliteConnection.get_instance(TEST_DB)
    cur = conn.cursor()
    cur.execute("DELETE FROM flights")
    conn.commit()

def test_create_and_read(conn_and_repo):
    repo = conn_and_repo
    f = Flight(None, "Baku", "Istanbul", "2025-11-12 08:00", "2025-11-12 10:00", "AC123")
    fid = repo.create_flight(f)
    assert isinstance(fid, int) and fid > 0
    rf = repo.read_by_id(fid)
    assert rf is not None
    assert rf.origin == "Baku"

def test_update_flight(conn_and_repo):
    repo = conn_and_repo
    f = Flight(None, "A", "B", "2025-01-01 00:00", "2025-01-01 02:00", "AC1")
    fid = repo.create_flight(f)
    f.flight_id = fid
    f.origin = "C"
    updated_id = repo.update_flight(f)
    assert updated_id == fid
    rf = repo.read_by_id(fid)
    assert rf.origin == "C"

def test_delete_flight(conn_and_repo):
    repo = conn_and_repo
    f = Flight(None, "X", "Y", "2025-02-01 00:00", "2025-02-01 02:00", "AC2")
    fid = repo.create_flight(f)
    repo.delete_flight(fid)
    assert repo.read_by_id(fid) is None
