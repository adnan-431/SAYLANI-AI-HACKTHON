# SAYLANI-AI-HACKTHON
# Smart Bus Ticket Booking System

## Purpose

A simple terminal program for managing bus ticket reservations. It lets a user view bus routes, search for a route, book tickets, cancel bookings, check seat availability, and generate a booking report. All data is saved automatically so it is still there the next time the program runs.

## Python Requirement

- Python 3.6 or higher (Python 3.8+ recommended)
- No extra packages needed. The program only uses the built-in `json` and `os` modules.

Check your version with:

```
python --version
```

## How to Run

1. Save `bus_booking_simple.py` in a folder of your choice.
2. Open a terminal in that folder.
3. Run:

```
python bus_booking_simple.py
```

On some systems you may need to use `python3` instead of `python`.

## Menu Guide

| Option | Name | What it does |
|--------|------|--------------|
| 1 | View Routes | Shows a table of all routes with departure time, fare, and seats left |
| 2 | Search for a Route | Finds routes by route ID (e.g. `R101`) or by departure/destination city (partial names work) |
| 3 | Book a Ticket | Asks for passenger name, age, route ID, and number of seats, then confirms the booking and shows the total fare |
| 4 | View Bookings | Lists every booking made, including cancelled ones |
| 5 | Cancel a Booking | Cancels a booking by its ID and returns the seats to the route |
| 6 | View Routes With Free Seats | Same table as option 1, but hides fully booked routes |
| 7 | Booking Report | Shows total, confirmed, and cancelled bookings, seats reserved, revenue, number of fully booked routes, and a per-route breakdown |
| 8 | Route Schedule | Lists departures grouped by departure city |
| 9 | Exit | Saves data and closes the program |

## Sample Workflow

1. Start the program and choose **1** to see the available routes.
2. Choose **3** to book a ticket:
   - Passenger name: `Ali`
   - Passenger age: `25`
   - Route ID: `R101`
   - Number of seats: `2`
3. The program confirms the booking, for example: Booking ID `B1001`, total fare `Rs. 2400`.
4. Choose **4** to see the booking in the history.
5. Choose **5** and enter `B1001` to cancel it. The 2 seats go back to route R101.
6. Choose **7** to view the report (the booking now counts as cancelled and is not included in revenue).
7. Choose **9** to save and exit.

## Storage Limitation

- Data is saved to a single file called `bus_data.json`, created in the folder where you run the program.
- The file is updated after every booking, every cancellation, and when you exit with option 9.
- Because it saves after every change, closing the terminal without choosing option 9 does not lose any bookings or cancellations.
- Once `bus_data.json` exists, the routes stored in it are used instead of the routes written in the code. If you edit the route list in the Python file, delete `bus_data.json` to make the changes take effect (this also erases all bookings).
- If `bus_data.json` is damaged or unreadable, the program shows a message and starts with the default routes and no bookings. The damaged file is replaced the next time data is saved.
- Running the program from a different folder creates a separate `bus_data.json` and starts with fresh data.
- The file is plain text and is not encrypted. Anyone with access to it can read or edit it.
- Only one copy of the program should be run at a time. Two copies running together can overwrite each other's changes.

## Constraints

- Single-user, terminal-only program with no login or passenger accounts.
- Routes are fixed in the code. There is no menu option to add, edit, or remove routes.
- Bookings cannot be edited. To change one, cancel it and make a new booking.
- Seats are counted, not assigned. There are no individual seat numbers.
- There is no travel date. Each route is treated as a single departure.
- No payment is processed. The fare is only calculated and displayed.
- Passenger name cannot be empty, and age and seat count must be whole numbers greater than zero.
- A booking cannot ask for more seats than are currently available on the route.
- Cancelled bookings stay in the history with the status "Cancelled" and cannot be restored.
- Booking IDs are sequential (`B1001`, `B1002`, ...) and are never reused.
