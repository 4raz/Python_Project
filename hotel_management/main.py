import os
import sys
from datetime import date


from .models import Guest, Reservation, Room
from .service import HotelService
password = "admin123"


def clear():
    os.system("cls" if os.name == "nt" else "clear")
def pause():
    input("\nPress Enter to continue...")

hms = """
░█░█░█▀█░▀█▀░█▀▀░█░░░░░█▄█░█▀█░█▀█░█▀█░█▀▀░█▀▀░█▄█░█▀▀░█▀█░▀█▀░░░█▀▀░█░█░█▀▀░▀█▀░█▀▀░█▄█
░█▀█░█░█░░█░░█▀▀░█░░░░░█░█░█▀█░█░█░█▀█░█░█░█▀▀░█░█░█▀▀░█░█░░█░░░░▀▀█░░█░░▀▀█░░█░░█▀▀░█░█
░▀░▀░▀▀▀░░▀░░▀▀▀░▀▀▀░░░▀░▀░▀░▀░▀░▀░▀░▀░▀▀▀░▀▀▀░▀░▀░▀▀▀░▀░▀░░▀░░░░▀▀▀░░▀░░▀▀▀░░▀░░▀▀▀░▀░▀
"""

def main():
    service = HotelService()

    while 1:
        clear()
        print(hms)
        print("1. Login as Admin")
        print("2. Login as Guest")
        print("0. Exit")
        
        choice = input("\nSelect Option >>> ").strip()

        if choice == "1":
            if login():amenu(service)

        elif choice == "2":gmenu(service)
            
        elif choice == "0":break
            
        else:
            print("Invalid input")
            pause()

def login():
    clear()
    print("=== Admin login === ")
    pwd = input("Enter password>>> ").strip()
    
    if (pwd == password):
        return True
    else:
        print("Incorrect password")
        pause()
        return False

def amenu(service):
    while True:
        clear()
        print("="*10 + " ADMIN " + "="*10)
        print("1.View all rooms")
        print("2.Add new room")
        print("3.View all reservations")
        print("4.Check-out guest")
        print("5.Cancel reservation")
        print("0.Main menu")
        opt = input(">>> ").strip()
        if opt == "1":
            clear()
            display_rooms(service.list_rooms())
            pause()
        elif opt == "2":
            clear()
            addroom(service)
            pause()
        elif opt == "3":
            clear()
            display_reserv(service.list_reservations())
            pause()
            
        elif opt == "4":
            procees_reserv(service, "complete")
            pause()
            

        elif opt == "5":
            procees_reserv(service, "cancel")
            pause()
            
        elif opt == "0":
            break
        else:
            print("Invalid option.")
            pause()
def gmenu(service):
    while True:
        clear()
        print("\n" + "="*10 + " GUEST MENU " + "="*10)
        print("1.Register/Signup")
        print("2.Check availability")
        print("3.Book room")
        print("4.Show bookings")
        print("5.Cancel my booking")
        print("0.Main menu")
        
        opt = input(">>> ").strip()



        if opt == "1":
            clear()
            guest_register(service)
            pause()
        elif opt == "2":
            clear()
            display_rooms(service.list_available_rooms())
            pause()

        elif opt == "3":
            clear()
            bookroom(service)
            pause()
        elif opt == "4":
            clear()
            view_reserv(service)
            pause()

        elif opt == "5":
            cancel_reserv(service)
            pause()
        elif opt == "0":
            break
        else:
            print("Invalid option.")
            pause()
def addroom(service):
    print("="*10 + "Add Room"+ "="*10)
    r_type = input("Enter room category >>> ").strip()
    price = input("Enter room cost >>> ").strip()
    try:
        rate = float(price)
    except ValueError:
        print("cost should be a number")
        return
    existing_ids = [r.room_id for r in service.list_rooms()]
    new_id = next_id("R", existing_ids)
    new_room = Room(new_id, r_type, rate, True)
    
    try:
        service.add_room(new_room)
        print(f"Room {new_id} added")
    except Exception as e:
        print(e)

def guest_register(service):
    print("="*10 + " Guest Registration " + "="*10)
    name = input("Enter name>>> ").strip()
    email = input("Enter email >>> ").strip()
    

    current_guests = [g.guest_id for g in service.list_guests()]
    g_id = next_id("G", current_guests)
    
    guest = Guest(g_id, name, email)
    
    try:
        service.register_guest(guest)
        print(f"Registered\n Guest ID is>>> {g_id}")
    except Exception as e:
        print(e)



def bookroom(service):
    print( "="*10 +  "Book a Room"+"="*10)
    gid = input("Enter Guest id>>> ").strip()
    guest = service.find_guest(gid)
    if not guest:
        print("Guest not registerd")
        return


    available_rooms = service.list_available_rooms()
    if not available_rooms:
        print("no rooms available.")
        return
        
    display_rooms(available_rooms)
    
    rid = input("\nEnter Room ID for booking>>> ").strip()
    room_obj = service.find_room(rid)
    
    if not room_obj or not room_obj.is_available:
        print("Room is unavailable")
        return
    d_in = get_date("Check-in Date (YYYY-MM-DD)>>> ")
    d_out = get_date("Check-out Date (YYYY-MM-DD)>>> ")
    
    if d_out <= d_in:
        print("Time travel not permitted")
        return

    all_res_ids = [r.reservation_id for r in service.list_reservations()]
    res_id = next_id("RES", all_res_ids)
    
    new_res = Reservation(res_id, gid, rid, d_in, d_out)
    
    try:
        service.create_reservation(new_res)
        print(f"Booking done\n Reservation ID>>> {res_id}")
    except ValueError as e:
        print(e)

def view_reserv(service):
    gid = input("Enter your Guest ID>>> ").strip()
    my_res = service.get_guest_reservations(gid)
    
    if not my_res:
        print("No reservations found for this guest.")
    else:
        display_reserv(my_res)

def cancel_reserv(service):
    gid = input("Enter Guest ID>>> ").strip()
    rid = input("Enter Reservation ID to cancel>>> ").strip()
    guest_res = service.get_guest_reservations(gid)
    is_valid = False
    for r in guest_res:
        if r.reservation_id == rid:
            is_valid = True
            break            
    if not is_valid:
        print("Not valid")
        return
        
    try:
        service.cancel_reservation(rid)
        print("Reservation canceled ")
    except Exception as e:
        print(e)

def procees_reserv(service, action):
    clear()
    print(f"--- {action.title()} Reservation ---")
    rid = input("Enter Reservation ID>>> ").strip()
    try:
        if action == "complete":
            service.complete_reservation(rid)
            print("Check-out done")
        elif action == "cancel":
            service.cancel_reservation(rid)
            print("Reservation canceeled")
    except ValueError as e:
        print(e)

def get_date(date_prompt_text):
    while True:
        val = input(date_prompt_text).strip()
        try:
            return date.fromisoformat(val)
        except ValueError:
            print("Wrong format. use YYYY-MM-DD.")

def display_rooms(room_list):
    if not room_list:
        print("No rooms to display")
        return
    print()
    print(f"{'ID':<10} | {'Type':<10} | {'Rate':<10} | {'Available':<10}")
    print("-" * 50)
    for room in room_list:
        print(f"{room.room_id:<10} | {room.room_type:<10} | ₹{room.rate:<9.2f} | {'yes' if room.is_available else 'no':<10}")

def display_reserv(res_list):
    if not res_list:
        print("no reservations")
        return
    
    print()
    print(f"{'Res ID':<10} | {'Guest ID':<8} | {'Room ID':<6} | {'Check-in':<12} | {'Status':<10}")
    print("-" * 60)
    for r in res_list:
        print(f"{r.reservation_id:<10} | {r.guest_id:<8} | {r.room_id:<6} | {str(r.check_in):<12} | {r.status}")

def next_id(prefix, id_list):
    max_val = 0
    for i in id_list:
        if i.startswith(prefix):
            num_part = i.replace(prefix, "")
            if num_part.isdigit():
                val = int(num_part)
                if val > max_val:
                    max_val = val
    
    return f"{prefix}{max_val + 1:03}"

if __name__ == "__main__":

    main()
