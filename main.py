import sys
import os
import traceback

# Ensure the project root is in the path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from views.start_window import StartWindow
from config import settings
from db.connection import verify_database_schema
from ui.fonts import load_custom_fonts


def main():
    verify_database_schema()

    app = QApplication(sys.argv)
    app.setApplicationName(settings.app_name)

    app.setStyle("Fusion")

    try:
        load_custom_fonts()
    except Exception as e:
        print(f"⚠️ Font loading failed: {e}")
        print("Continuing with system fonts...")

    window = StartWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("\n" + "!" * 60)
        print("❌ CRASH DETECTED! Here is the reason:")
        traceback.print_exc()
        print("!" * 60)
        input("\nPress ENTER to close this window...")
