from dataclasses import dataclass, replace, asdict
from typing import Optional


# src/models/aircraft.py
class Aircraft:
    """Mutable OO model kept for compatibility."""
    def __init__(self, aircraft_id: int, model: str, capacity: int):
        self.aircraft_id = aircraft_id
        self.model = model
        self.capacity = capacity
        self.passengers_count = 0  # hazırda təyyarədəki sərnişin sayı

    def info(self):
        return f"ID: {self.aircraft_id}, Model: {self.model}, Capacity: {self.capacity}, Passengers: {self.passengers_count}"

    def is_full(self):
        return self.passengers_count >= self.capacity

    def add_passenger(self):
        if self.is_full():
            raise ValueError(f"Aircraft {self.aircraft_id} is full!")
        self.passengers_count += 1

    def remove_passenger(self):
        if self.passengers_count > 0:
            self.passengers_count -= 1


@dataclass(frozen=True)
class AircraftRecord:
    aircraft_id: int
    model: str
    capacity: int
    passengers_count: int = 0


def make_aircraft_record(aircraft_id: int, model: str, capacity: int) -> AircraftRecord:
    return AircraftRecord(aircraft_id, model, capacity, 0)


def update_aircraft_record(a: AircraftRecord, **changes) -> AircraftRecord:
    return replace(a, **changes)


def aircraft_to_dict(a: AircraftRecord) -> dict:
    return asdict(a)


def aircraft_from_dict(d: dict) -> AircraftRecord:
    return AircraftRecord(**d)
