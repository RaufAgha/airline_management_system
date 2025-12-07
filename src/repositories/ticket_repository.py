# src/repositories/ticket_repository.py
from src.models.ticket import Ticket
from src.models.ticket import TicketRecord, ticket_from_dict
from src.utils.exceptions import NotFoundError
from src.repositories.base_repository import BaseRepository
from src.utils.exceptions import AlreadyExistsError

import logging
logger = logging.getLogger(__name__)

class TicketRepository(BaseRepository):
    def __init__(self):
        super().__init__("tickets", Ticket, id_column="ticket_id")

    def create_ticket(self, ticket: Ticket):
        # Eyni flight və seat üçün yoxlama
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM tickets WHERE flight_id = ? AND seat_number = ?",
                    (ticket.flight_id, ticket.seat_number))
        if cur.fetchone():
            raise AlreadyExistsError(f"Seat {ticket.seat_number} already booked for flight {ticket.flight_id}")
        flight_id = getattr(ticket, "flight_id")
        passenger_id = getattr(ticket, "passenger_id")
        seat_number = getattr(ticket, "seat_number")
        price = getattr(ticket, "price")
        cur.execute("INSERT INTO tickets (flight_id, passenger_id, seat_number, price) VALUES (?, ?, ?, ?)",
                (flight_id, passenger_id, seat_number, price))
        self.conn.commit()
        return cur.lastrowid

    def update_ticket(self, ticket: Ticket):
        if not ticket.ticket_id:
            raise ValueError("ticket_id is required for update")
        cur = self.conn.cursor()
        cur.execute("UPDATE tickets SET flight_id = ?, passenger_id = ?, seat_number = ?, price = ? WHERE ticket_id = ?",
                    (ticket.flight_id, ticket.passenger_id, ticket.seat_number, ticket.price, ticket.ticket_id))
        if cur.rowcount == 0:
            raise NotFoundError(f"Ticket with ID {ticket.ticket_id} not found")
        self.conn.commit()
        return ticket.ticket_id

    def delete_ticket(self, ticket_id: int):
        # wrapper for CLI consistency
        self.delete(ticket_id)

    # Record reads
    def read_by_id_record(self, id_value) -> TicketRecord | None:
        cur = self.conn.cursor()
        cur.execute(f"SELECT * FROM {self.table_name} WHERE {self.id_column} = ?", (id_value,))
        row = cur.fetchone()
        if not row:
            return None
        return ticket_from_dict(dict(row))

    def read_all_records(self) -> list[TicketRecord]:
        cur = self.conn.cursor()
        cur.execute(f"SELECT * FROM {self.table_name}")
        rows = cur.fetchall()
        return [ticket_from_dict(dict(r)) for r in rows]
