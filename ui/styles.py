COLORS = {
    "bg_dark": "#0a0a0a",
    "bg_darker": "#050505",
    "bg_card": "rgba(20, 20, 20, 0.95)",
    "overlay": "rgba(0, 0, 0, 0.75)",
    "primary": "#ffa500",
    "secondary": "#ffcc00",
    "accent": "#ff8800",
    "text_primary": "#ffffff",
    "text_secondary": "#e0e0e0",
    "text_muted": "#999999",
    "success": "#27ae60",
    "error": "#e74c3c",
    "warning": "#f39c12",
    "border": "rgba(255, 165, 0, 0.4)",
    "border_hover": "rgba(255, 136, 0, 0.7)",
}

# Базовий стиль з шрифтом Inter
BASE_STYLE = f"""
    QWidget {{
        background-color: {COLORS['bg_dark']};
        color: {COLORS['text_primary']};
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        font-size: 14px;
        font-weight: 400;
    }}
    
    QMainWindow {{
        background-color: {COLORS['bg_dark']};
    }}
"""

# Start Window
START_WINDOW_STYLE = (
    BASE_STYLE
    + f"""
    #bgLabel {{
        background-color: {COLORS['bg_dark']};
    }}
    
    #overlay {{
        background: {COLORS['overlay']};
    }}
    
    #logoImage {{
        background: transparent;
        padding: 0px;
    }}
    
    #appTitle {{
        font-size: 42px;
        font-weight: 700;
        letter-spacing: 4px;
        color: {COLORS['primary']};
        margin-bottom: 0px;
        background: transparent;
    }}
    
    #subtitle {{
        font-size: 18px;
        color: {COLORS['text_secondary']};
        font-weight: 300;
        margin-bottom: 0px;
        letter-spacing: 0.5px;
        background: transparent;
    }}
    
    #centerCard {{
        background: {COLORS['bg_card']};
        border-radius: 16px;
        border: 2px solid {COLORS['border']};
    }}
    
    QPushButton {{
        border-radius: 10px;
        padding: 14px 28px;
        font-size: 15px;
        font-weight: 500;
        border: none;
        min-height: 45px;
        letter-spacing: 0.5px;
    }}
    
    QPushButton#primaryButton {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                    stop:0 {COLORS['primary']}, 
                                    stop:1 {COLORS['secondary']});
        color: {COLORS['bg_dark']};
        font-weight: 600;
    }}
    
    QPushButton#primaryButton:hover {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                    stop:0 {COLORS['accent']}, 
                                    stop:1 {COLORS['primary']});
    }}
    
    QPushButton#secondaryButton {{
        background: transparent;
        border: 2px solid {COLORS['primary']};
        color: {COLORS['primary']};
        font-weight: 500;
    }}
    
    QPushButton#secondaryButton:hover {{
        background: {COLORS['primary']};
        color: {COLORS['bg_dark']};
    }}
    
    QPushButton#ghostButton {{
        background: transparent;
        color: {COLORS['text_muted']};
        text-decoration: underline;
        padding: 10px;
        font-weight: 400;
    }}
    
    QPushButton#ghostButton:hover {{
        color: {COLORS['text_primary']};
    }}
"""
)

# Auth Windows (Login/Signup)
AUTH_WINDOW_STYLE = (
    BASE_STYLE
    + f"""
    #authCard {{
        background: {COLORS['bg_card']};
        border-radius: 16px;
        border: 2px solid {COLORS['border']};
    }}
    
    #logoInCard {{
        background: transparent;
    }}
    
    #authTitle {{
        font-size: 32px;
        font-weight: 600;
        color: {COLORS['primary']};
        margin: 0px;
        padding: 0px;
        letter-spacing: 1px;
        background: transparent;
    }}
    
    #authSubtitle {{
        color: {COLORS['text_secondary']};
        font-size: 14px;
        margin: 0px;
        padding: 0px;
        font-weight: 400;
        background: transparent;
    }}
    
    #fieldLabel {{
        color: {COLORS['text_secondary']};
        font-size: 13px;
        margin: 0px;
        padding: 0px;
        font-weight: 400;
        background: transparent;
    }}
    
    #errorLabel {{
        color: {COLORS['error']};
        font-size: 12px;
        font-weight: 400;
        background: transparent;
        padding: 4px 0px;
        margin: 0px;
    }}
    
    #passwordHint {{
        color: {COLORS['text_muted']};
        font-size: 11px;
        font-weight: 400;
        background: transparent;
        padding: 4px 0px;
        margin: 0px;
        font-style: italic;
    }}
    
    
    QLineEdit {{
        background: {COLORS['bg_darker']};
        border: 2px solid transparent;
        border-radius: 8px;
        padding: 12px 16px;
        color: {COLORS['text_primary']};
        font-size: 14px;
        min-height: 20px;
        font-weight: 400;
    }}
    
    QLineEdit:focus {{
        border: 2px solid {COLORS['primary']};
    }}
    
    QPushButton#submitButton {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                    stop:0 {COLORS['primary']}, 
                                    stop:1 {COLORS['secondary']});
        color: {COLORS['bg_dark']};
        border-radius: 10px;
        padding: 14px;
        font-size: 15px;
        font-weight: 600;
        border: none;
        min-height: 45px;
        letter-spacing: 0.5px;
    }}
    
    QPushButton#submitButton:hover {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                    stop:0 {COLORS['accent']}, 
                                    stop:1 {COLORS['primary']});
    }}
    
    QPushButton#backButton {{
        background: transparent;
        color: {COLORS['text_muted']};
        border: none;
        padding: 12px;
        font-weight: 400;
        font-size: 14px;
        min-height: 35px;
    }}
    
    QPushButton#backButton:hover {{
        color: {COLORS['text_primary']};
    }}
"""
)

MAIN_VIEW_STYLE = (
    BASE_STYLE
    + f"""
    /* Буде додано далі */
"""
)


def apply_style(widget, style_name):
    styles = {
        "start": START_WINDOW_STYLE,
        "auth": AUTH_WINDOW_STYLE,
        "main": MAIN_VIEW_STYLE,
    }

    if style_name in styles:
        widget.setStyleSheet(styles[style_name])
    else:
        widget.setStyleSheet(BASE_STYLE)
