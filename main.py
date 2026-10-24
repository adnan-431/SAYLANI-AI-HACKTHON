# Smart Bus Ticket Booking System (simple version)

import json
import os

DATA_FILE = "bus_data.json"

routes = [
    {"route_id": "R101", "from": "Karachi", "to": "Hyderabad",
     "time": "08:00 AM", "price": 1200, "total_seats": 40, "available_seats": 40},
    {"route_id": "R102", "from": "Karachi", "to": "Sukkur",
     "time": "09:30 AM", "price": 2000, "total_seats": 36, "available_seats": 36},
    {"route_id": "R103", "from": "Hyderabad", "to": "Mirpur Khas",
     "time": "11:00 AM", "price": 800, "total_seats": 32, "available_seats": 32},
    {"route_id": "R104", "from": "Karachi", "to": "Lahore",
     "time": "07:00 PM", "price": 5000, "total_seats": 45, "available_seats": 45},
    {"route_id": "R105", "from": "Sukkur", "to": "Hyderabad",
     "time": "02:00 PM", "price": 1500, "total_seats": 30, "available_seats": 30},
]

bookings = []


# ---------- Saving and loading (one JSON file) ----------

def save_data():
    with open(DATA_FILE, "w") as file:
        json.dump({"routes": routes, "bookings": bookings}, file, indent=4)


def load_data():
    global routes, bookings
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as file:
            data = json.load(file)
        routes = data["routes"]
        bookings = data["bookings"]
        print("Previous data loaded.")


# ---------- Helper functions ----------

def find_route(route_id):
    for route in routes:
        if route["route_id"].lower() == route_id.lower():
            return route
    return None


def seat_status(route):
    if route["available_seats"] == 0:
        return "Fully Booked"
    if route["available_seats"] == route["total_seats"]:
        return "Available"
    return "Partially Booked"


def read_number(prompt):
    while True:
        text = input(prompt).strip()
        if text.isdigit() and int(text) > 0:
            return int(text)
        print("Please enter a whole number greater than zero.")


def print_route(route):
    print(f"{route['route_id']} | {route['from']} -> {route['to']} | "
          f"{route['time']} | Rs. {route['price']} | "
          f"{route['available_seats']}/{route['total_seats']} seats "
          f"({seat_status(route)})")


# ---------- Menu options ----------

def view_routes(only_available=False):
    print("\nAVAILABLE BUS ROUTES")
    print("-" * 90)
    print(f"{'No.':<5}{'Route':<9}{'Journey':<36}{'Departure':<13}{'Fare':<12}{'Seats'}")
    print("-" * 90)

    shown = 0
    for number, route in enumerate(routes, start=1):
        if only_available and route["available_seats"] == 0:
            continue

        shown += 1
        journey = route["from"] + " -> " + route["to"]
        print(
            f"{number:<5}{route['route_id']:<9}{journey:<36}"
            f"{route['time']:<13}Rs.{route['price']:<9}"
            f"{route['available_seats']}/{route['total_seats']} ({seat_status(route)})"
        )

    if shown == 0:
        print("No routes with available seats found.")


def search_route():
    term = input("Enter route ID or city: ").strip().lower()
    found = False
    for route in routes:
        if term and (term == route["route_id"].lower()
                     or term in route["from"].lower()
                     or term in route["to"].lower()):
            print_route(route)
            found = True
    if not found:
        print("No matching route found.")


def book_ticket():
    print("\nBOOK A TICKET")
    name = input("Passenger name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return

    age = read_number("Passenger age: ")
    route = find_route(input("Route ID: ").strip())
    if route is None:
        print("Route not found.")
        return

    seats = read_number("Number of seats: ")
    if seats > route["available_seats"]:
        print(f"Only {route['available_seats']} seats are available.")
        return

    booking = {
        "booking_id": "B" + str(1001 + len(bookings)),
        "passenger_name": name,
        "passenger_age": age,
        "route_id": route["route_id"],
        "seats": seats,
        "total_fare": route["price"] * seats,
        "status": "Confirmed",
    }
    bookings.append(booking)
    route["available_seats"] -= seats
    save_data()

    print("\nBooking confirmed!")
    print(f"Booking ID: {booking['booking_id']}")
    print(f"Route: {route['from']} -> {route['to']}")
    print(f"Seats: {seats}")
    print(f"Total fare: Rs. {booking['total_fare']}")


def view_bookings():
    print("\nBOOKING HISTORY")
    if not bookings:
        print("No bookings found.")
        return
    for b in bookings:
        print(f"{b['booking_id']} | {b['passenger_name']} (age {b['passenger_age']}) | "
              f"{b['route_id']} | {b['seats']} seats | "
              f"Rs. {b['total_fare']} | {b['status']}")


def cancel_booking():
    booking_id = input("Booking ID to cancel: ").strip().upper()
    for booking in bookings:
        if booking["booking_id"] == booking_id:
            if booking["status"] == "Cancelled":
                print("This booking is already cancelled.")
                return
            route = find_route(booking["route_id"])
            route["available_seats"] += booking["seats"]
            booking["status"] = "Cancelled"
            save_data()
            print(f"Booking {booking_id} cancelled. {booking['seats']} seats restored.")
            return
    print("Booking ID not found.")


def generate_report():
    confirmed = [b for b in bookings if b["status"] == "Confirmed"]
    cancelled = [b for b in bookings if b["status"] == "Cancelled"]

    print("\nBOOKING REPORT")
    print(f"Total bookings: {len(bookings)}")
    print(f"Confirmed: {len(confirmed)}")
    print(f"Cancelled: {len(cancelled)}")
    print(f"Seats reserved: {sum(b['seats'] for b in confirmed)}")
    print(f"Revenue: Rs. {sum(b['total_fare'] for b in confirmed)}")

    print("\nCONFIRMED BOOKINGS BY ROUTE")
    for route in routes:
        route_bookings = [b for b in confirmed if b["route_id"] == route["route_id"]]
        seats = sum(b["seats"] for b in route_bookings)
        revenue = sum(b["total_fare"] for b in route_bookings)
        print(f"{route['route_id']} ({route['from']} -> {route['to']}): "
              f"{seats} seats, Rs. {revenue}")


def show_schedule():
    print("\nSCHEDULE BY DEPARTURE CITY")
    cities = sorted(set(route["from"] for route in routes))
    for city in cities:
        print(f"\n{city}")
        for route in routes:
            if route["from"] == city:
                print(f"  {route['route_id']} -> {route['to']} at {route['time']}")


# ---------- Main program ----------

def main():
    load_data()

    while True:
        print("\n=== SMART BUS TICKET BOOKING SYSTEM ===")
        print("1. View Routes")
        print("2. Search for a Route")
        print("3. Book a Ticket")
        print("4. View Bookings")
        print("5. Cancel a Booking")
        print("6. View Routes With Free Seats")
        print("7. Booking Report")
        print("8. Route Schedule")
        print("9. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            view_routes()
        elif choice == "2":
            search_route()
        elif choice == "3":
            book_ticket()
        elif choice == "4":
            view_bookings()
        elif choice == "5":
            cancel_booking()
        elif choice == "6":
            view_routes(only_available=True)
        elif choice == "7":
            generate_report()
        elif choice == "8":
            show_schedule()
        elif choice == "9":
            save_data()
            print("Data saved. Goodbye!")
            break
        else:
            print("Invalid choice. Enter a number from 1 to 9.")


main()
