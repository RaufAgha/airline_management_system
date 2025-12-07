# src/services/booking_service.py
from src.models.ticket import Ticket
from src.repositories.ticket_repository import TicketRepository
from src.repositories.passenger_repository import PassengerRepository
from src.repositories.flight_repository import FlightRepository
from src.utils.exceptions import NotFoundError, AlreadyExistsError, InvalidInputError
import logging

logger = logging.getLogger(__name__)

class BookingService:
    def __init__(self, ticket_repo: TicketRepository, passenger_repo: PassengerRepository, flight_repo: FlightRepository):
        self.ticket_repo = ticket_repo
        self.passenger_repo = passenger_repo
        self.flight_repo = flight_repo

    def create_ticket(self, ticket: Ticket):
        # Validate input IDs are integers (ticket.flight_id and ticket.passenger_id)
        try:
            flight_id = int(ticket.flight_id)
            passenger_id = int(ticket.passenger_id)
        except (TypeError, ValueError):
            raise InvalidInputError("flight_id and passenger_id must be integers")

        # Passenger mövcudluğunu yoxla (prefer record read)
        passenger = self.passenger_repo.read_by_id_record(passenger_id) if hasattr(self.passenger_repo, 'read_by_id_record') else self.passenger_repo.read_by_id(passenger_id)
        if not passenger:
            raise NotFoundError(f"Passenger ID {passenger_id} not found!")

        # Flight mövcudluğunu yoxla
        flight = self.flight_repo.read_by_id_record(flight_id) if hasattr(self.flight_repo, 'read_by_id_record') else self.flight_repo.read_by_id(flight_id)
        if not flight:
            raise NotFoundError(f"Flight ID {flight_id} not found!")

        # Duplicate seat yoxla and create
        return self.ticket_repo.create_ticket(ticket)

    def get_all_tickets(self):
        return self.ticket_repo.read_all()

    def cancel_ticket(self, ticket_id: int):
        if not self.ticket_repo.read_by_id(ticket_id):
            raise NotFoundError(f"Ticket ID {ticket_id} not found!")
        self.ticket_repo.delete(ticket_id)
