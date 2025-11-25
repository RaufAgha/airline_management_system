class Ticket:
    def __init__(self, ticket_id, flight_id, passenger_id, seat_number, price=0):
        self.ticket_id = ticket_id
        self.flight_id = flight_id
        self.passenger_id = passenger_id
        self.seat_number = seat_number
        self.price = price
    def __str__(self):
        return f"Ticket {self.ticket_id}: Passenger {self.passenger_id}, Flight {self.flight_id}, Seat {self.seat_number}"


import logging
logger = logging.getLogger(__name__)