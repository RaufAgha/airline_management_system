# src/models/flight.py
from dataclasses import dataclass, replace, asdict
from typing import Optional


class Flight:
    """Mutable OO model kept for compatibility with existing code."""
    def __init__(self, flight_id: int, origin: str, destination: str, departure_time: str, arrival_time: str, aircraft_id: str):
        self.flight_id = flight_id
        self.origin = origin
        self.destination = destination
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.aircraft_id = aircraft_id
        self.tickets_sold = 0  # satılmış biletlərin sayı

    def info(self):
        return f"ID: {self.flight_id}, {self.origin}->{self.destination}, {self.departure_time}-{self.arrival_time}, Aircraft: {self.aircraft_id}, Tickets sold: {self.tickets_sold}"

    def sell_ticket(self):
        self.tickets_sold += 1

    def cancel_ticket(self):
        if self.tickets_sold > 0:
            self.tickets_sold -= 1


@dataclass(frozen=True)
class FlightRecord:
    """Immutable, functional dataclass variant of Flight.

    Use `make_flight_record` and `update_flight_record` helper functions to work
    in a functional style (returning new instances instead of mutating).
    """
    flight_id: Optional[int]
    origin: str
    destination: str
    departure_time: str
    arrival_time: str
    aircraft_id: str
    tickets_sold: int = 0


def make_flight_record(flight_id: Optional[int], origin: str, destination: str, departure_time: str, arrival_time: str, aircraft_id: str) -> FlightRecord:
    return FlightRecord(flight_id, origin, destination, departure_time, arrival_time, aircraft_id, 0)


def update_flight_record(f: FlightRecord, **changes) -> FlightRecord:
    """Return a new FlightRecord with the provided field changes."""
    return replace(f, **changes)


def flight_to_dict(f: FlightRecord) -> dict:
    return asdict(f)


def flight_from_dict(d: dict) -> FlightRecord:
    return FlightRecord(**d)
