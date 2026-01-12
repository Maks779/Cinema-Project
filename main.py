import sys
import os

# Ensure the project root is in the path so imports work
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# Using PySide6 to avoid the Python 3.13 DLL errors
from PySide6.QtWidgets import QApplication
from views.start_window import StartWindow
from config import settings

def main():
    # Initialize the Application
    app = QApplication(sys.argv)
    app.setApplicationName(settings.app_name)

    # Apply Styles if the file exists
    try:
        if os.path.exists(settings.ui.styles_path):
            with open(settings.ui.styles_path, "r", encoding="utf-8") as f:
                app.setStyleSheet(f.read())
    except Exception as e:
        print(f"Error loading styles: {e}")

    # Launch the Start Window
    window = StartWindow()
    window.show()

    # PySide6 uses exec() instead of exec_()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()