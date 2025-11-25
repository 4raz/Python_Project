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

## Work Breakdown

- Bhaskar Kumar Arya: Modeled the core `Guest`, `Room`, and `Reservation` classes and kept the CSV serialization helpers simple.
- Muhammad Raza Khan: Set up the CSV files and the small repository helper that reads/writes them, filled in the sample data, and kept the service layer hooked up so bookings, cancellations, and room availability always reflect what’s stored on disk.
- Surya Kiran Basava: Implemented the menu-driven CLI, covering both admin and guest flows plus booking/cancellation interactions. Also added ASCII art.

## Getting Started

```bash
python -m hotel_management.main
```

- Admin options: view/add rooms, inspect reservations, cancel or complete stays.
- Guest options: self-register, view availability, book rooms, review or cancel reservations.
- Update the CSV paths in `hotel_management/settings.py` if you relocate the `data/` folder.
