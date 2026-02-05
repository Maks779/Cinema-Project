from PySide6.QtGui import QFontDatabase, QFont
import os


def load_custom_fonts():
    font_dir = "assets/fonts"

    if not os.path.exists(font_dir):
        print(f"⚠️ Folder {font_dir} not found. Using system fonts.")
        return

    for filename in os.listdir(font_dir):
        if filename.endswith((".ttf", ".otf")):
            font_path = os.path.join(font_dir, filename)
            font_id = QFontDatabase.addApplicationFont(font_path)

            if font_id != -1:
                font_families = QFontDatabase.applicationFontFamilies(font_id)
                print(f"✅ Loaded font: {font_families}")
            else:
                print(f"❌ Failed to load: {filename}")


def get_app_font(size=14, weight=QFont.Normal):
    font = QFont("Inter", size, weight)
    font.setStyleHint(QFont.SansSerif)
    return font
