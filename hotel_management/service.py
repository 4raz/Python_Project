"""Business workflows coordinating repositories."""

from . import settings
from .models import Guest, Reservation, Room
from .repository import CSVRepository


def _guest_repo():
    return CSVRepository(
        settings.GUESTS_CSV, ["guest_id", "full_name", "email"], Guest.from_dict
    )


def _room_repo():
    return CSVRepository(
        settings.ROOMS_CSV,
        ["room_id", "room_type", "rate", "is_available"],
        Room.from_dict,
    )


def _reservation_repo():
    return CSVRepository(
        settings.RESERVATIONS_CSV,
        ["reservation_id", "guest_id", "room_id", "check_in", "check_out", "status"],
        Reservation.from_dict,
    )


class HotelService:
    """High-level hotel operations."""

    def __init__(self):
        self.guests = _guest_repo()
        self.rooms = _room_repo()
        self.reservations = _reservation_repo()

    def list_rooms(self):
        return self.rooms.list_all()

    def list_guests(self):
        return self.guests.list_all()

    def list_reservations(self):
        return self.reservations.list_all()

    def list_available_rooms(self):
        return [room for room in self.rooms.list_all() if room.is_available]

    def find_guest(self, guest_id):
        return next(
            (guest for guest in self.guests.list_all() if guest.guest_id == guest_id),
            None,
        )

    def find_room(self, room_id):
        return next(
            (room for room in self.rooms.list_all() if room.room_id == room_id), None
        )

    def create_reservation(self, reservation):
        rooms = self.rooms.list_all()
        target = next(
            (room for room in rooms if room.room_id == reservation.room_id), None
        )
        if not target or not target.is_available:
            raise ValueError("Room unavailable")

        reservations = self.reservations.list_all()
        for existing in reservations:
            if existing.status != "BOOKED":
                continue
            overlaps = not (
                reservation.check_out <= existing.check_in
                or reservation.check_in >= existing.check_out
            )
            if existing.room_id == reservation.room_id and overlaps:
                raise ValueError("Room already booked within the requested range")

        reservations.append(reservation)
        self.reservations.save_all(reservations)
        target.is_available = False
        self.rooms.save_all(rooms)
        return reservation

    def cancel_reservation(self, reservation_id):
        reservations = self.reservations.list_all()
        rooms = self.rooms.list_all()
        found = False
        released_room_id = None
        for reservation in reservations:
            if reservation.reservation_id == reservation_id:
                reservation.status = "CANCELLED"
                found = True
                released_room_id = reservation.room_id
                break
        if found:
            self.reservations.save_all(reservations)
            self._release_room(rooms, released_room_id)
        else:
            raise ValueError("Reservation not found")

    def complete_reservation(self, reservation_id):
        reservations = self.reservations.list_all()
        rooms = self.rooms.list_all()
        found = False
        released_room_id = None
        for reservation in reservations:
            if reservation.reservation_id == reservation_id:
                reservation.status = "COMPLETED"
                found = True
                released_room_id = reservation.room_id
                break
        if found:
            self.reservations.save_all(reservations)
            self._release_room(rooms, released_room_id)
        else:
            raise ValueError("Reservation not found")

    def _release_room(self, rooms, room_id):
        if not room_id:
            return
        for room in rooms:
            if room.room_id == room_id:
                room.is_available = True
                break
        self.rooms.save_all(rooms)

    def register_guest(self, guest):
        guests = self.guests.list_all()
        if any(existing.guest_id == guest.guest_id for existing in guests):
            raise ValueError("Guest already exists")
        guests.append(guest)
        self.guests.save_all(guests)
        return guest

    def add_room(self, room):
        rooms = self.rooms.list_all()
        if any(existing.room_id == room.room_id for existing in rooms):
            raise ValueError("Room already exists")
        rooms.append(room)
        self.rooms.save_all(rooms)
        return room

    def set_room_availability(self, room_id, is_available):
        rooms = self.rooms.list_all()
        found = False
        normalized = str(is_available).strip().lower()
        flag = normalized in ("1", "true", "yes", "available")
        for room in rooms:
            if room.room_id == room_id:
                room.is_available = flag
                found = True
                break
        if not found:
            raise ValueError("Room not found")
        self.rooms.save_all(rooms)

    def get_guest_reservations(self, guest_id):
        return [res for res in self.reservations.list_all() if res.guest_id == guest_id]

    def seed_sample_data(self):
        if not self.guests.list_all():
            self.guests.save_all(
                [
                    Guest("G001", "Ariana Reed", "ariana@example.com"),
                    Guest("G002", "Bao Tran", "bao@example.com"),
                ]
            )
        if not self.rooms.list_all():
            self.rooms.save_all(
                [
                    Room("R101", "Deluxe", 120.0, True),
                    Room("R102", "Suite", 200.0, True),
                ]
            )
        if not self.reservations.list_all():
            self.reservations.save_all([])
