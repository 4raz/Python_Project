"""Centralized settings for CSV persistence."""

import os

PACKAGE_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
BASE_DIRECTORY = os.path.dirname(PACKAGE_DIRECTORY)
DATA_DIRECTORY = os.path.join(BASE_DIRECTORY, "data")

GUESTS_CSV = os.path.join(DATA_DIRECTORY, "guests.csv")
ROOMS_CSV = os.path.join(DATA_DIRECTORY, "rooms.csv")
RESERVATIONS_CSV = os.path.join(DATA_DIRECTORY, "reservations.csv")
