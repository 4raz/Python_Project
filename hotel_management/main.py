import os
from datetime import date

from .models import Guest, Reservation, Room
from .service import HotelService

ADMIN_PASSWORD = "admin123"
BANNER = """
░█░█░█▀█░▀█▀░█▀▀░█░░░░░█▄█░█▀█░█▀█░█▀█░█▀▀░█▀▀░█▄█░█▀▀░█▀█░▀█▀░░░█▀▀░█░█░█▀▀░▀█▀░█▀▀░█▄█
░█▀█░█░█░░█░░█▀▀░█░░░░░█░█░█▀█░█░█░█▀█░█░█░█▀▀░█░█░█▀▀░█░█░░█░░░░▀▀█░░█░░▀▀█░░█░░█▀▀░█░█
░▀░▀░▀▀▀░░▀░░▀▀▀░▀▀▀░░░▀░▀░▀░▀░▀░▀░▀░▀░▀▀▀░▀▀▀░▀░▀░▀▀▀░▀░▀░░▀░░░░▀▀▀░░▀░░▀▀▀░░▀░░▀▀▀░▀░▀
"""


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def pause():
    input("\nPress Enter to continue...")


def main():
    service = HotelService()
    while True:
        clear_screen()
        print(BANNER)
        print("\n==== Hotel Management ====")
        print("1. Admin")
        print("2. Guest")
        print("0. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            if authenticate_admin():
                admin_menu(service)
        elif choice == "2":
            guest_menu(service)
        elif choice == "0":
            clear_screen()
            print("Goodbye!")
            break
        else:
            print("Invalid option. Try again.")
            pause()


def authenticate_admin():
    clear_screen()
    password = input("Enter admin password: ").strip()
    if password == ADMIN_PASSWORD:
        return True
    print("Incorrect password.")
    pause()
    return False


def admin_menu(service):
    while True:
        clear_screen()
        print("---- Admin Menu ----")
        print("1. View rooms")
        print("2. Add room")
        print("3. View reservations")
        print("4. Complete reservation (check-out)")
        print("5. Cancel reservation")
        print("0. Back")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            clear_screen()
            show_rooms(service.list_rooms())
            pause()
        elif choice == "2":
            clear_screen()
            add_room_flow(service)
            pause()
        elif choice == "3":
            clear_screen()
            show_reservations(service.list_reservations())
            pause()
        elif choice == "4":
            clear_screen()
            update_reservation_status(service, "complete")
            pause()
        elif choice == "5":
            clear_screen()
            update_reservation_status(service, "cancel")
            pause()
        elif choice == "0":
            break
        else:
            print("Invalid option.")
            pause()


def guest_menu(service):
    while True:
        clear_screen()
        print("---- Guest Menu ----")
        print("1. Register")
        print("2. View available rooms")
        print("3. Book room")
        print("4. View my reservations")
        print("5. Cancel reservation")
        print("0. Back")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            clear_screen()
            register_guest_flow(service)
            pause()
        elif choice == "2":
            clear_screen()
            show_rooms(service.list_available_rooms())
            pause()
        elif choice == "3":
            clear_screen()
            book_room_flow(service)
            pause()
        elif choice == "4":
            clear_screen()
            show_guest_reservations(service)
            pause()
        elif choice == "5":
            clear_screen()
            cancel_guest_reservation(service)
            pause()
        elif choice == "0":
            break
        else:
            print("Invalid option.")
            pause()


def add_room_flow(service):
    room_type = input("Room type: ").strip()
    rate_input = input("Nightly rate: ").strip()
    try:
        rate = float(rate_input)
    except ValueError:
        print("Invalid rate.")
        return

    room_id = generate_id("R", [room.room_id for room in service.list_rooms()])
    room = Room(room_id, room_type, rate, True)
    try:
        service.add_room(room)
        print(f"Room {room_id} added.")
    except ValueError as exc:
        print(exc)


def register_guest_flow(service):
    full_name = input("Full name: ").strip()
    email = input("Email: ").strip()
    guest_id = generate_id("G", [guest.guest_id for guest in service.list_guests()])
    guest = Guest(guest_id, full_name, email)
    try:
        service.register_guest(guest)
        print(f"Your guest ID is {guest_id}. Keep it for future bookings.")
    except ValueError as exc:
        print(exc)


def book_room_flow(service):
    guest_id = input("Guest ID: ").strip()
    guest = service.find_guest(guest_id)
    if not guest:
        print("Guest not found. Register first.")
        return

    available = service.list_available_rooms()
    if not available:
        print("No rooms available right now.")
        return
    show_rooms(available)

    room_id = input("Choose room ID: ").strip()
    room = service.find_room(room_id)
    if not room or not room.is_available:
        print("Room unavailable.")
        return

    check_in = prompt_date("Check-in date (YYYY-MM-DD): ")
    check_out = prompt_date("Check-out date (YYYY-MM-DD): ")
    if check_out <= check_in:
        print("Check-out must be after check-in.")
        return

    reservation_id = generate_id(
        "RES", [res.reservation_id for res in service.list_reservations()]
    )
    reservation = Reservation(reservation_id, guest_id, room_id, check_in, check_out)
    try:
        service.create_reservation(reservation)
        print(f"Reservation confirmed with ID {reservation_id}.")
    except ValueError as exc:
        print(f"Could not book room: {exc}")


def show_guest_reservations(service):
    guest_id = input("Guest ID: ").strip()
    reservations = service.get_guest_reservations(guest_id)
    if not reservations:
        print("No reservations found.")
        return
    show_reservations(reservations)


def cancel_guest_reservation(service):
    guest_id = input("Guest ID: ").strip()
    reservation_id = input("Reservation ID: ").strip()
    reservations = service.get_guest_reservations(guest_id)
    if not any(res.reservation_id == reservation_id for res in reservations):
        print("Reservation not found for this guest.")
        return
    try:
        service.cancel_reservation(reservation_id)
        print("Reservation cancelled.")
    except ValueError as exc:
        print(exc)


def update_reservation_status(service, action):
    reservation_id = input("Reservation ID: ").strip()
    try:
        if action == "complete":
            service.complete_reservation(reservation_id)
            print("Reservation marked completed.")
        else:
            service.cancel_reservation(reservation_id)
            print("Reservation cancelled.")
    except ValueError as exc:
        print(exc)


def prompt_date(message):
    while True:
        value = input(message).strip()
        try:
            return date.fromisoformat(value)
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD.")


def show_rooms(rooms):
    if not rooms:
        print("No rooms to show.")
        return
    print("\nRoom ID | Type    | Rate | Available")
    for room in rooms:
        status = "Yes" if room.is_available else "No"
        print(f"{room.room_id:>6} | {room.room_type:<7} | {room.rate:>5.2f} | {status}")


def show_reservations(reservations):
    if not reservations:
        print("No reservations to show.")
        return
    print("\nRes ID   | Guest | Room | Check-in  | Check-out | Status")
    for res in reservations:
        print(
            f"{res.reservation_id:>7} | {res.guest_id:>5} | {res.room_id:>4} | "
            f"{res.check_in} | {res.check_out} | {res.status}"
        )


def generate_id(prefix, existing_ids):
    highest = 0
    for value in existing_ids:
        if value.startswith(prefix):
            digits = "".join(ch for ch in value if ch.isdigit())
            if digits:
                highest = max(highest, int(digits))
    return f"{prefix}{highest + 1:03}"


if __name__ == "__main__":
    main()
