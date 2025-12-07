# main.py

import sys
import os
import logging
import io

# ----------------- PATH FIX -----------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# ----------------- LOGGING -----------------
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "app.log")

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.handlers = []

file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)

stream_handler = logging.StreamHandler(stream=io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8'))
stream_handler.setFormatter(file_formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

# ----------------- IMPORTS -----------------
from src.db.sqlite_connection import SqliteConnection
from src.models.aircraft import Aircraft
from src.models.flight import Flight
from src.models.passenger import Passenger
from src.models.ticket import Ticket
from src.repositories.aircraft_repository import AircraftRepository
from src.repositories.flight_repository import FlightRepository
from src.repositories.passenger_repository import PassengerRepository
from src.repositories.ticket_repository import TicketRepository
from src.services.flight_service import FlightService
from src.services.booking_service import BookingService
from src.utils.exceptions import NotFoundError, AlreadyExistsError

# ----------------- MENÜLƏR -----------------
def aircraft_menu(aircraft_repo):
    while True:
        logger.info("--- Aircraft Management ---")
        print("1. Add Aircraft\n2. View Aircraft\n3. Delete Aircraft\n4. Add Passenger\n5. Remove Passenger\n6. Back")
        choice = input("Select: ").strip()
        try:
            if choice == "1":
                aircraft_id = input("Aircraft ID: ")
                if aircraft_repo.read_by_id(aircraft_id):
                    raise AlreadyExistsError(f"Aircraft ID {aircraft_id} already exists!")
                model = input("Model: ")
                capacity = int(input("Capacity: "))
                aircraft = Aircraft(aircraft_id, model, capacity)
                aircraft_repo.create_aircraft(aircraft)
                logger.info(f"Aircraft added: {aircraft.info()}")
            
            elif choice == "2":
                aircrafts = aircraft_repo.read_all()
                if not aircrafts:
                    logger.info("No aircraft found.")
                for a in aircrafts:
                    logger.info(a.info() + f", Current passengers: {a.passengers_count}")

            elif choice == "3":
                aircraft_id = input("Aircraft ID to delete: ")
                aircraft_repo.delete_aircraft(aircraft_id)
                logger.info(f"Aircraft {aircraft_id} deleted")

            elif choice == "4":
                aircraft_id = input("Aircraft ID to add passenger: ")
                aircraft = aircraft_repo.read_by_id(aircraft_id)
                if not aircraft:
                    raise NotFoundError(f"Aircraft ID {aircraft_id} not found!")
                aircraft.add_passenger()
                logger.info(f"Passenger added. Current passengers: {aircraft.passengers_count}")

            elif choice == "5":
                aircraft_id = input("Aircraft ID to remove passenger: ")
                aircraft = aircraft_repo.read_by_id(aircraft_id)
                if not aircraft:
                    raise NotFoundError(f"Aircraft ID {aircraft_id} not found!")
                aircraft.remove_passenger()
                logger.info(f"Passenger removed. Current passengers: {aircraft.passengers_count}")

            elif choice == "6":
                break
            else:
                logger.warning("Invalid option!")

        except ValueError:
            logger.error("Invalid input type!")
        except (NotFoundError, AlreadyExistsError) as e:
            logger.error(e)

def flight_menu(flight_service):
    while True:
        logger.info("--- Flight Management ---")
        print("1. Add Flight\n2. View Flights\n3. Delete Flight\n4. Back")
        choice = input("Select: ").strip()
        try:
            if choice == "1":
                origin = input("Origin: ")
                destination = input("Destination: ")
                dep = input("Departure (YYYY-MM-DD HH:MM): ")
                arr = input("Arrival (YYYY-MM-DD HH:MM): ")
                aircraft_id = input("Aircraft ID: ")
                flight = Flight(None, origin, destination, dep, arr, aircraft_id)
                fid = flight_service.add_flight(flight)
                logger.info(f"Flight added with ID {fid}")
            
            elif choice == "2":
                flights = flight_service.get_all_flights()
                if not flights:
                    logger.info("No flights found.")
                for f in flights:
                    logger.info(f"ID: {f.flight_id}, {f.origin}->{f.destination}, Aircraft: {f.aircraft_id}")
            
            elif choice == "3":
                fid = int(input("Flight ID to delete: "))
                flight_service.delete_flight(fid)
                logger.info(f"Flight {fid} deleted")
            
            elif choice == "4":
                break
            else:
                logger.warning("Invalid option!")

        except ValueError:
            logger.error("Invalid input type!")
        except (NotFoundError, AlreadyExistsError) as e:
            logger.error(e)

def passenger_menu(passenger_repo):
    while True:
        logger.info("--- Passenger Management ---")
        print("1. Add Passenger\n2. View Passengers\n3. Delete Passenger\n4. Back")
        choice = input("Select: ").strip()
        try:
            if choice == "1":
                name = input("Name: ")
                email = input("Email: ")
                phone = input("Phone: ")
                passenger = Passenger(None, name, email, phone)
                pid = passenger_repo.create_passenger(passenger)
                logger.info(f"Passenger added with ID {pid}")
            
            elif choice == "2":
                passengers = passenger_repo.read_all()
                for p in passengers:
                    logger.info(f"ID: {p.passenger_id}, Name: {p.name}, Email: {p.email}, Phone: {p.phone}")

            elif choice == "3":
                pid = int(input("Passenger ID to delete: "))
                passenger_repo.delete_passenger(pid)
                logger.info(f"Passenger {pid} deleted")

            elif choice == "4":
                break
            else:
                logger.warning("Invalid option!")

        except ValueError:
            logger.error("Invalid input type!")
        except (NotFoundError, AlreadyExistsError) as e:
            logger.error(e)

def ticket_menu(booking_service):
    while True:
        logger.info("--- Ticket Management ---")
        print("1. Add Ticket\n2. View Tickets\n3. Delete Ticket\n4. Back")
        choice = input("Select: ").strip()
        try:
            if choice == "1":
                flight_id = int(input("Flight ID: "))
                passenger_id = int(input("Passenger ID: "))
                seat_number = input("Seat Number: ")
                price = float(input("Price: "))
                ticket = Ticket(None, flight_id, passenger_id, seat_number, price)
                tid = booking_service.create_ticket(ticket)
                logger.info(f"Ticket added with ID {tid}")

            elif choice == "2":
                tickets = booking_service.get_all_tickets()
                for t in tickets:
                    logger.info(f"ID: {t.ticket_id}, Flight: {t.flight_id}, Passenger: {t.passenger_id}, Seat: {t.seat_number}")

            elif choice == "3":
                tid = int(input("Ticket ID to delete: "))
                booking_service.cancel_ticket(tid)
                logger.info(f"Ticket {tid} deleted")

            elif choice == "4":
                break
            else:
                logger.warning("Invalid option!")

        except ValueError:
            logger.error("Invalid input type!")
        except (NotFoundError, AlreadyExistsError) as e:
            logger.error(e)

# ----------------- MAIN -----------------
def main():
    conn = SqliteConnection.get_instance()
    conn.init_db()

    aircraft_repo = AircraftRepository()
    flight_repo = FlightRepository()
    passenger_repo = PassengerRepository()
    ticket_repo = TicketRepository()

    flight_service = FlightService(flight_repo, aircraft_repo)
    booking_service = BookingService(ticket_repo, passenger_repo, flight_repo)

    while True:
        logger.info("--- Airline Management ---")
        print("1. Aircraft\n2. Flight\n3. Passenger\n4. Ticket\n5. Exit")
        choice = input("Select: ").strip()

        if choice == "1":
            aircraft_menu(aircraft_repo)
        elif choice == "2":
            flight_menu(flight_service)
        elif choice == "3":
            passenger_menu(passenger_repo)
        elif choice == "4":
            ticket_menu(booking_service)
        elif choice == "5":
            logger.info("Exiting...")
            break
        else:
            logger.warning("Invalid option!")

if __name__ == "__main__":
    main()
