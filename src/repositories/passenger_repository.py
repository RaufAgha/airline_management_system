from src.models.passenger import Passenger
from src.repositories.base_repository import BaseRepository
from src.utils.exceptions import AlreadyExistsError

class PassengerRepository(BaseRepository):
    def __init__(self):
        super().__init__("passengers", Passenger)

    def create_passenger(self, passenger: Passenger):
        # Duplicate email yoxlama
        existing = [p for p in self.read_all() if p.email == passenger.email]
        if existing:
            raise AlreadyExistsError(f"Passenger with email {passenger.email} already exists.")
        return self.create(
            name=passenger.name,
            email=passenger.email,
            phone=passenger.phone
        )

    def delete_passenger(self, passenger_id):
        return self.delete("passenger_id", passenger_id)


import logging
logger = logging.getLogger(__name__)