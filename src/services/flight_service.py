from src.models.flight import Flight
from src.repositories.flight_repository import FlightRepository
from src.repositories.aircraft_repository import AircraftRepository
from src.utils.exceptions import NotFoundError, AlreadyExistsError

class FlightService:
    def __init__(self, flight_repo: FlightRepository, aircraft_repo: AircraftRepository):
        self.flight_repo = flight_repo
        self.aircraft_repo = aircraft_repo

    def add_flight(self, flight: Flight):
        # Aircraft mövcudluğunu yoxla
        aircrafts = self.aircraft_repo.read_all()
        if not any(a.aircraft_id == flight.aircraft_id for a in aircrafts):
            raise NotFoundError(f"Aircraft ID {flight.aircraft_id} not found!")

        # Flight yarat
        return self.flight_repo.create_flight(flight)

    def get_all_flights(self):
        return self.flight_repo.read_all()

    def delete_flight(self, flight_id: int):
        self.flight_repo.delete_flight(flight_id)


import logging
logger = logging.getLogger(__name__)
