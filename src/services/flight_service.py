# src/services/flight_service.py
from src.models.flight import Flight, FlightRecord
from src.repositories.flight_repository import FlightRepository
from src.repositories.aircraft_repository import AircraftRepository
from src.utils.exceptions import NotFoundError, AlreadyExistsError
import logging

logger = logging.getLogger(__name__)

class FlightService:
    def __init__(self, flight_repo: FlightRepository, aircraft_repo: AircraftRepository):
        self.flight_repo = flight_repo
        self.aircraft_repo = aircraft_repo

    def add_flight(self, flight: Flight):
        # Aircraft mövcudluğunu yoxla (use record read for safety)
        aircraft = self.aircraft_repo.read_by_id_record(flight.aircraft_id) if hasattr(self.aircraft_repo, 'read_by_id_record') else self.aircraft_repo.read_by_id(flight.aircraft_id)
        if not aircraft:
            raise NotFoundError(f"Aircraft ID {flight.aircraft_id} not found!")

        # Flight yarat - accept either Flight or FlightRecord
        return self.flight_repo.create_flight(flight)

    def get_all_flights(self):
        return self.flight_repo.read_all()

    def delete_flight(self, flight_id: int):
        if not self.flight_repo.read_by_id(flight_id):
            raise NotFoundError(f"Flight ID {flight_id} not found!")
        self.flight_repo.delete(flight_id)
