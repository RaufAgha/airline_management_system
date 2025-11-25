from src.models.ticket import Ticket
from src.repositories.ticket_repository import TicketRepository
from src.repositories.passenger_repository import PassengerRepository
from src.repositories.flight_repository import FlightRepository
from src.utils.exceptions import NotFoundError, AlreadyExistsError

class BookingService:
    def __init__(self, ticket_repo: TicketRepository, passenger_repo: PassengerRepository, flight_repo: FlightRepository):
        self.ticket_repo = ticket_repo
        self.passenger_repo = passenger_repo
        self.flight_repo = flight_repo

    def create_ticket(self, ticket: Ticket):
        # Passenger mövcudluğunu yoxla
        passengers = self.passenger_repo.read_all()
        if not any(p.passenger_id == ticket.passenger_id for p in passengers):
            raise NotFoundError(f"Passenger ID {ticket.passenger_id} not found!")

        # Flight mövcudluğunu yoxla
        flights = self.flight_repo.read_all()
        if not any(f.flight_id == ticket.flight_id for f in flights):
            raise NotFoundError(f"Flight ID {ticket.flight_id} not found!")

        # Duplicate seat yoxla
        tickets = self.ticket_repo.read_all()
        if any(t.flight_id == ticket.flight_id and t.seat_number == ticket.seat_number for t in tickets):
            raise AlreadyExistsError(f"Seat {ticket.seat_number} is already booked for this flight!")

        return self.ticket_repo.create_ticket(ticket)

    def get_all_tickets(self):
        return self.ticket_repo.read_all()

    def cancel_ticket(self, ticket_id: int):
        self.ticket_repo.delete_ticket(ticket_id)


import logging
logger = logging.getLogger(__name__)
