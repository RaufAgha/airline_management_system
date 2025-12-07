# src/repositories/passenger_repository.py
from src.models.passenger import Passenger
from src.models.passenger import PassengerRecord, passenger_from_dict
from src.utils.exceptions import NotFoundError
from src.repositories.base_repository import BaseRepository
from src.utils.exceptions import AlreadyExistsError

import logging
logger = logging.getLogger(__name__)

class PassengerRepository(BaseRepository):
	def __init__(self):
		super().__init__("passengers", Passenger, id_column="passenger_id")

	def create_passenger(self, passenger: Passenger):
		# Email-ə görə təkrar yoxlama
		cur = self.conn.cursor()
		cur.execute("SELECT * FROM passengers WHERE email = ?", (passenger.email,))
		if cur.fetchone():
			raise AlreadyExistsError(f"Passenger with email {passenger.email} already exists")
		name = getattr(passenger, "name")
		email = getattr(passenger, "email")
		phone = getattr(passenger, "phone")
		cur.execute("INSERT INTO passengers (name, email, phone) VALUES (?, ?, ?)",
			    (name, email, phone))
		self.conn.commit()
		return cur.lastrowid

	def update_passenger(self, passenger: Passenger):
		if not passenger.passenger_id:
			raise ValueError("passenger_id is required for update")
		cur = self.conn.cursor()
		cur.execute("UPDATE passengers SET name = ?, email = ?, phone = ? WHERE passenger_id = ?",
					(passenger.name, passenger.email, passenger.phone, passenger.passenger_id))
		if cur.rowcount == 0:
			raise NotFoundError(f"Passenger with ID {passenger.passenger_id} not found")
		self.conn.commit()
		return passenger.passenger_id

	def delete_passenger(self, passenger_id: int):
		# wrapper to keep API consistent with CLI
		self.delete(passenger_id)

	# Record helpers
	def read_by_id_record(self, id_value) -> PassengerRecord | None:
		cur = self.conn.cursor()
		cur.execute(f"SELECT * FROM {self.table_name} WHERE {self.id_column} = ?", (id_value,))
		row = cur.fetchone()
		if not row:
			return None
		return passenger_from_dict(dict(row))

	def read_all_records(self) -> list[PassengerRecord]:
		cur = self.conn.cursor()
		cur.execute(f"SELECT * FROM {self.table_name}")
		rows = cur.fetchall()
		return [passenger_from_dict(dict(r)) for r in rows]

