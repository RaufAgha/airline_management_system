import sys
import os
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.db.sqlite_connection import SqliteConnection
from src.models.flight import Flight
from src.models.passenger import Passenger
from src.models.ticket import Ticket
from src.models.aircraft import Aircraft
from src.repositories.flight_repository import FlightRepository
from src.repositories.passenger_repository import PassengerRepository
from src.repositories.ticket_repository import TicketRepository
from src.repositories.aircraft_repository import AircraftRepository
from src.services.flight_service import FlightService
from src.services.booking_service import BookingService
from src.utils.exceptions import NotFoundError, AlreadyExistsError

# ---------------- Logging Setup ----------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# ---------------- Flight Menu ----------------
def flight_menu(flight_service):
    while True:
        logger.info("--- Flight Management ---")
        print("1. Add Flight")
        print("2. View Flights")
        print("3. Delete Flight")
        print("4. Back")
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
                    logger.info(f"ID: {f.flight_id}, {f.origin}->{f.destination}, {f.departure_time}-{f.arrival_time}, Aircraft: {f.aircraft_id}")
            elif choice == "3":
                fid = int(input("Flight ID to delete: "))
                flight_service.delete_flight(fid)
                logger.info(f"Flight {fid} deleted")
            elif choice == "4":
                break
            else:
                logger.warning("Invalid option!")
        except ValueError:
            logger.error("Invalid input type.")
        except NotFoundError as e:
            logger.error(e)

# ---------------- Passenger Menu ----------------
def passenger_menu(passenger_repo):
    while True:
        logger.info("--- Passenger Management ---")
        print("1. Add Passenger")
        print("2. View Passengers")
        print("3. Delete Passenger")
        print("4. Back")
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
                if not passengers:
                    logger.info("No passengers found.")
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
            logger.error("Invalid input type.")
        except NotFoundError as e:
            logger.error(e)
        except AlreadyExistsError as e:
            logger.error(e)

# ---------------- Ticket Menu ----------------
def ticket_menu(booking_service):
    while True:
        logger.info("--- Ticket Management ---")
        print("1. Add Ticket")
        print("2. View Tickets")
        print("3. Delete Ticket")
        print("4. Back")
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
                if not tickets:
                    logger.info("No tickets found.")
                for t in tickets:
                    logger.info(f"ID: {t.ticket_id}, Flight ID: {t.flight_id}, Passenger ID: {t.passenger_id}, Seat: {t.seat_number}, Price: {t.price}")
            elif choice == "3":
                tid = int(input("Ticket ID to delete: "))
                booking_service.cancel_ticket(tid)
                logger.info(f"Ticket {tid} deleted")
            elif choice == "4":
                break
            else:
                logger.warning("Invalid option!")
        except ValueError:
            logger.error("Invalid input type.")
        except NotFoundError as e:
            logger.error(e)
        except AlreadyExistsError as e:
            logger.error(e)

# ---------------- Aircraft Menu ----------------
def aircraft_menu(aircraft_repo):
    while True:
        logger.info("--- Aircraft Management ---")
        print("1. Add Aircraft")
        print("2. View Aircraft")
        print("3. Delete Aircraft")
        print("4. Back")
        choice = input("Select: ").strip()
        try:
            if choice == "1":
                aircraft_id = input("Aircraft ID: ")
                model = input("Model: ")
                capacity = int(input("Capacity: "))
                aircraft = Aircraft(aircraft_id, model, capacity)
                aircraft_repo.create_aircraft(aircraft)
                logger.info(f"Aircraft added with ID {aircraft_id}")
            elif choice == "2":
                aircrafts = aircraft_repo.read_all()
                if not aircrafts:
                    logger.info("No aircraft found.")
                for a in aircrafts:
                    logger.info(f"ID: {a.aircraft_id}, Model: {a.model}, Capacity: {a.capacity}")
            elif choice == "3":
                aircraft_id = input("Aircraft ID to delete: ")
                aircraft_repo.delete_aircraft(aircraft_id)
                logger.info(f"Aircraft {aircraft_id} deleted")
            elif choice == "4":
                break
            else:
                logger.warning("Invalid option!")
        except ValueError:
            logger.error("Invalid input type.")
        except NotFoundError as e:
            logger.error(e)
        except AlreadyExistsError as e:
            logger.error(e)

# ---------------- Main ----------------
def main():
    conn = SqliteConnection.get_instance()
    conn.init_db()  # bütün table-lar yaradılır

    # Repositories
    flight_repo = FlightRepository()
    passenger_repo = PassengerRepository()
    ticket_repo = TicketRepository()
    aircraft_repo = AircraftRepository()

    # Services
    flight_service = FlightService(flight_repo, aircraft_repo)
    booking_service = BookingService(ticket_repo, passenger_repo, flight_repo)

    while True:
        logger.info("--- Airline Ticket Management ---")
        print("1. Flight Management")
        print("2. Passenger Management")
        print("3. Ticket Management")
        print("4. Aircraft Management")
        print("5. Exit")
        choice = input("Select: ").strip()
        if choice == "1":
            flight_menu(flight_service)
        elif choice == "2":
            passenger_menu(passenger_repo)
        elif choice == "3":
            ticket_menu(booking_service)
        elif choice == "4":
            aircraft_menu(aircraft_repo)
        elif choice == "5":
            logger.info("Exiting...")
            break
        else:
            logger.warning("Invalid option!")

if __name__ == "__main__":
    main()
