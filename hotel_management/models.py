"""Domain models for the hotel management system."""

from datetime import date


class Guest:
    def __init__(self, guest_id, full_name, email):
        self.guest_id = guest_id
        self.full_name = full_name
        self.email = email

    def to_dict(self):
        return {
            "guest_id": self.guest_id,
            "full_name": self.full_name,
            "email": self.email,
        }

    @classmethod
    def from_dict(cls, row):
        return cls(
            row["guest_id"],
            row.get("full_name", ""),
            row.get("email", ""),
        )


def _to_bool(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in ("1", "true", "yes", "available")
    return bool(value)


def _to_date(value):
    if isinstance(value, date):
        return value
    return date.fromisoformat(str(value))


class Room:
    def __init__(self, room_id, room_type, rate, is_available=True):
        self.room_id = room_id
        self.room_type = room_type
        self.rate = float(rate)
        self.is_available = _to_bool(is_available)

    def to_dict(self):
        return {
            "room_id": self.room_id,
            "room_type": self.room_type,
            "rate": f"{self.rate:.2f}",
            "is_available": "1" if self.is_available else "0",
        }

    @classmethod
    def from_dict(cls, row):
        return cls(
            row["room_id"],
            row.get("room_type", ""),
            row.get("rate", 0),
            row.get("is_available", "1") == "1",
        )


class Reservation:
    def __init__(
        self, reservation_id, guest_id, room_id, check_in, check_out, status="BOOKED"
    ):
        self.reservation_id = reservation_id
        self.guest_id = guest_id
        self.room_id = room_id
        self.check_in = _to_date(check_in)
        self.check_out = _to_date(check_out)
        self.status = status

    def to_dict(self):
        return {
            "reservation_id": self.reservation_id,
            "guest_id": self.guest_id,
            "room_id": self.room_id,
            "check_in": self.check_in.isoformat(),
            "check_out": self.check_out.isoformat(),
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, row):
        return cls(
            row["reservation_id"],
            row["guest_id"],
            row["room_id"],
            date.fromisoformat(row["check_in"]),
            date.fromisoformat(row["check_out"]),
            row.get("status", "BOOKED"),
        )
