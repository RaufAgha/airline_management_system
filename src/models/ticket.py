from dataclasses import dataclass, replace, asdict
from typing import Optional


# src/models/ticket.py
class Ticket:
    """Mutable OO model kept for compatibility."""
    def __init__(self, ticket_id: int, flight_id: int, passenger_id: int, seat_number: str, price: float):
        self.ticket_id = ticket_id
        self.flight_id = flight_id
        self.passenger_id = passenger_id
        self.seat_number = seat_number
        self.price = price

    def info(self):
        return f"ID: {self.ticket_id}, Flight: {self.flight_id}, Passenger: {self.passenger_id}, Seat: {self.seat_number}, Price: {self.price}"


@dataclass(frozen=True)
class TicketRecord:
    ticket_id: Optional[int]
    flight_id: int
    passenger_id: int
    seat_number: str
    price: float


def make_ticket_record(ticket_id: Optional[int], flight_id: int, passenger_id: int, seat_number: str, price: float) -> TicketRecord:
    return TicketRecord(ticket_id, flight_id, passenger_id, seat_number, price)


def update_ticket_record(t: TicketRecord, **changes) -> TicketRecord:
    return replace(t, **changes)


def ticket_to_dict(t: TicketRecord) -> dict:
    return asdict(t)


def ticket_from_dict(d: dict) -> TicketRecord:
    return TicketRecord(**d)
