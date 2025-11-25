from src.models.aircraft import Aircraft
from src.repositories.base_repository import BaseRepository
from src.utils.exceptions import AlreadyExistsError

class AircraftRepository(BaseRepository):
    def __init__(self):
        super().__init__("aircraft", Aircraft)

    def create_aircraft(self, aircraft: Aircraft):
        existing = [a for a in self.read_all() if a.aircraft_id == aircraft.aircraft_id]
        if existing:
            raise AlreadyExistsError(f"Aircraft with ID {aircraft.aircraft_id} already exists.")
        return self.create(
            aircraft_id=aircraft.aircraft_id,
            model=aircraft.model,
            capacity=aircraft.capacity
        )

    def delete_aircraft(self, aircraft_id):
        return self.delete("aircraft_id", aircraft_id)


import logging
logger = logging.getLogger(__name__)