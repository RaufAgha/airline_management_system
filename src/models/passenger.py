class Passenger:
    def __init__(self, passenger_id, name, email, phone):
        self.passenger_id = passenger_id
        self.name = name
        self.email = email
        self.phone = phone

    def __str__(self):
        return f"{self.name} ({self.email})"


import logging
logger = logging.getLogger(__name__)