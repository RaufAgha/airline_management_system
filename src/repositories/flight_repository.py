from src.models.flight import Flight
from src.repositories.base_repository import BaseRepository

class FlightRepository(BaseRepository):
    def __init__(self):
        super().__init__("flights", Flight)

    def create_flight(self, flight: Flight):
        return self.create(
            origin=flight.origin,
            destination=flight.destination,
            departure_time=flight.departure_time,
            arrival_time=flight.arrival_time,
            aircraft_id=flight.aircraft_id
        )

    def delete_flight(self, flight_id):
        return self.delete("flight_id", flight_id)


import logging
logger = logging.getLogger(__name__)