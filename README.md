# Cinema-Project
# Cinema Booking System 🎬
A Python-based desktop application for managing cinema tickets, built with **PySide6** and **PostgreSQL**.

## 🚀 Project Status: Phases 1-6 Complete
This project followed a structured development roadmap:
- **Phase 1 & 2**: Requirements defined and environment setup (Python 3.13 + PySide6).
- **Phase 3**: Database schema implemented in PostgreSQL with 6 relational tables.
- **Phase 4**: User Authentication system with Role-Based Access Control (Admin/User).
- **Phase 5**: Complete User Booking Flow (Movie list -> Showtimes -> Seat Selection).
- **Phase 6**: Admin Management Panel with database maintenance features.

## 🛠️ Tech Stack
- **Frontend**: PySide6 (Qt for Python)
- **Backend**: Python 3.13
- **Database**: PostgreSQL 18
- **Libraries**: `psycopg2` for database connectivity

## 📖 How to Run
1. Configure your database credentials in `config.py`.
2. Run `python -m db.init_db` to create tables.
3. Run `python -m db.seed_db` to add sample movies.
4. Run `python main.py` to start the application.