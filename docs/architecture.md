# Airline Ticket Management System Architecture

## Overview
The Airline Ticket Management System is designed using **Object-Oriented Programming (OOP) principles**. It allows managing flights, passengers, tickets, and aircrafts using a modular and maintainable architecture.

## Layers

### 1. Models
- **Flight**: flight_id, origin, destination, departure_time, arrival_time, aircraft_id  
- **Passenger**: passenger_id, name, email, phone  
- **Ticket**: ticket_id, flight_id, passenger_id, seat_number, price  
- **Aircraft**: aircraft_id, model, capacity  

### 2. Repositories
- **BaseRepository**: Provides generic CRUD methods (Create, Read, Delete).  
- **Specific Repositories**: FlightRepository, PassengerRepository, TicketRepository, AircraftRepository inherit from BaseRepository and implement domain-specific logic.  
- **Exceptions**: NotFoundError, AlreadyExistsError are used to handle invalid operations.

### 3. CLI
- `main.py` provides a **menu-driven interface** for CRUD operations.  
- Handles user input, exceptions, and displays results.  

### 4. Database
- Uses **SQLite** (`sqlite3`) for persistent data storage.  
- Tables:
  - `flights(flight_id, origin, destination, departure_time, arrival_time, aircraft_id)`
  - `passengers(passenger_id, name, email, phone)`
  - `tickets(ticket_id, flight_id, passenger_id, seat_number, price)`
  - `aircraft(aircraft_id, model, capacity)`

## Relationships
- **Flight → Aircraft** (each flight uses one aircraft)  
- **Ticket → Flight** (each ticket belongs to a flight)  
- **Ticket → Passenger** (each ticket belongs to a passenger)
