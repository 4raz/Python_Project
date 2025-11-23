# Hotel Management System (CSV + Python)

## High-Level Outline

1. **Core Domain Objects (OOP layer)**
   - `Guest`, `Room`, and `Reservation` classes capture hotel data.
   - Validation and serialization helpers keep CSV interactions simple.
2. **Persistence Layer (CSV storage)**
   - Repositories abstract the CSV read/write logic for each domain object.
   - Uses headers-first CSV files in `data/` so entries stay human readable.
3. **Service Layer (business workflows)**
   - `HotelService` coordinates bookings, check-ins, availability queries, and cancellations.
   - Keeps orchestration logic separate from UI.
4. **Interface Layer (CLI)**
   - `main.py` provides a menu-driven CLI with separate Admin and Guest flows.
   - Admin password defaults to `admin123`; adjust `ADMIN_PASSWORD` in `main.py` if needed.

## Work Breakdown (Three Parallel Tracks)

1. **Domain & Validation**
   - Flesh out models, add richer validation, capacity rules, and helpers for CSV serialization.
   - Extend unit tests for model behaviors.
2. **Persistence & Data Management**
   - Implement CRUD operations in repositories, add locking/concurrency handling, and reporting exports.
   - Populate sample CSV data and data-migration utilities.
3. **Service Layer & Interface**
   - Expand `HotelService` flows (search, booking lifecycle, billing hooks).
   - Build CLI menus or a minimal FastAPI/Flask interface.

Each part can be owned independently with well-defined interfaces between layers.

## Getting Started

```bash
python -m hotel_management.main
```

- Admin options: view/add rooms, inspect reservations, cancel or complete stays.
- Guest options: self-register, view availability, book rooms, review or cancel reservations.
- Update the CSV paths in `hotel_management/settings.py` if you relocate the `data/` folder.
- Add tests under `tests/` when you begin feature work.
