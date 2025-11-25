from src.models.ticket import Ticket
from src.repositories.base_repository import BaseRepository

class TicketRepository(BaseRepository):
    def __init__(self):
        super().__init__("tickets", Ticket)

    def create_ticket(self, ticket: Ticket):
        return self.create(
            flight_id=ticket.flight_id,
            passenger_id=ticket.passenger_id,
            seat_number=ticket.seat_number,
            price=ticket.price
        )

    def delete_ticket(self, ticket_id):
        return self.delete("ticket_id", ticket_id)


import logging
logger = logging.getLogger(__name__)
