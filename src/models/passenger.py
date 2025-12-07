from dataclasses import dataclass, replace, asdict
from typing import Optional


# src/models/passenger.py
class Passenger:
    """Mutable OO model kept for compatibility."""
    def __init__(self, passenger_id: int, name: str, email: str, phone: str):
        self.passenger_id = passenger_id
        self.name = name
        self.email = email
        self.phone = phone

    def info(self):
        return f"ID: {self.passenger_id}, Name: {self.name}, Email: {self.email}, Phone: {self.phone}"


@dataclass(frozen=True)
class PassengerRecord:
    passenger_id: Optional[int]
    name: str
    email: str
    phone: str


def make_passenger_record(passenger_id: Optional[int], name: str, email: str, phone: str) -> PassengerRecord:
    return PassengerRecord(passenger_id, name, email, phone)


def update_passenger_record(p: PassengerRecord, **changes) -> PassengerRecord:
    return replace(p, **changes)


def passenger_to_dict(p: PassengerRecord) -> dict:
    return asdict(p)


def passenger_from_dict(d: dict) -> PassengerRecord:
    return PassengerRecord(**d)
