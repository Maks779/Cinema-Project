import sys
import os
import traceback  # Required for the error report

# Ensure the project root is in the path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from PySide6.QtWidgets import QApplication
from views.main_view import MainView
from config import settings
from db.connection import verify_database_schema

def main():
    # 1. Check DB first
    verify_database_schema()

    app = QApplication(sys.argv)
    app.setApplicationName(settings.app_name)

    # 2. Launch MainView in Guest Mode
    # If this line crashes, the 'except' block below will catch it!
    window = MainView(username=None, role="guest")
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    # THIS IS THE SAFETY NET (Step 1)
    try:
        main()
    except Exception as e:
        print("\n" + "!"*60)
        print("❌ CRASH DETECTED! Here is the reason:")
        traceback.print_exc()
        print("!"*60)
        # This is the most important line: it keeps the terminal open!
        input("\nPress ENTER to close this window...")