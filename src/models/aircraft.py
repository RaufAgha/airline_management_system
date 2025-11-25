class Aircraft:
    def __init__(self, aircraft_id, model, capacity):
        self.aircraft_id = aircraft_id
        self.model = model
        self.capacity = capacity

    def __str__(self):
        return f"{self.model} (Capacity: {self.capacity})"
