import os
import logging
from typing import Self
from pydantic import BaseModel

# !!!Temporary test config, replace with environment variables or config files in production!!!

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class DatabaseConfig(BaseModel):
    host: str = "localhost"
    port: int = 5432
    user: str = "postgres"
    password: str = "admin123"  # Use the password you just set
    dbname: str = "cinema_db"

class UIConfig(BaseModel):
    ui_dir: str = os.path.join(BASE_DIR, "ui")
    styles_path: str = os.path.join(BASE_DIR, "ui", "styles.qss")
    icons_dir: str = os.path.join(BASE_DIR, "resources", "icons")
    
    login_ui_file: str = "login_window.ui"
    user_main_ui_file: str = "user_main_window.ui"
    admin_main_ui_file: str = "admin_main_window.ui"

    window_title: str = "Cinema Booking System"
    window_width: int = 800
    window_height: int = 600

class AppConfig(BaseModel):
    log_level: int = logging.DEBUG
    app_name: str = "CinemaBooker"
    version: str = "1.0.0"
    
    db: DatabaseConfig
    ui: UIConfig

    @classmethod
    def create(cls) -> Self:
        return cls(
            db=DatabaseConfig(),
            ui=UIConfig()
        )

settings = AppConfig.create()