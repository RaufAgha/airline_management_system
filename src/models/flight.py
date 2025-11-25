from datetime import datetime

class Flight:
    def __init__(self, flight_id, origin, destination, departure_time, arrival_time, aircraft_id):
        self.flight_id = flight_id
        self.origin = origin
        self.destination = destination
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.aircraft_id = aircraft_id

    def flight_duration(self):
        dep = datetime.fromisoformat(self.departure_time)
        arr = datetime.fromisoformat(self.arrival_time)
        return (arr - dep).total_seconds() / 3600

    def __str__(self):
        return f"Flight {self.flight_id}: {self.origin} → {self.destination}"

import logging
logger = logging.getLogger(__name__)