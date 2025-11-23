"""Centralized settings for CSV persistence."""

import os

PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(PACKAGE_DIR)
DATA_DIR = os.path.join(BASE_DIR, "data")

GUESTS_CSV = os.path.join(DATA_DIR, "guests.csv")
ROOMS_CSV = os.path.join(DATA_DIR, "rooms.csv")
RESERVATIONS_CSV = os.path.join(DATA_DIR, "reservations.csv")
