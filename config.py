# config.py - Add these configurations
"""
FitPose Configuration File - UPDATED FOR REAL-TIME MONITORING
"""

# Application settings
APP_NAME = "FitPose - Real-Time Exercise Posture Monitor"
VERSION = "2.0.0"
WINDOW_SIZE = "1400x800"
FULLSCREEN = False  # Set to True for kiosk mode
SPLASH_DURATION = 2000

# Color scheme
COLORS = {
    "primary": "#2E3B4E",
    "secondary": "#1E2A38",
    "accent": "#4CAF50",
    "danger": "#F44336",
    "warning": "#FF9800",
    "dark": "#121826",
    "light": "#F5F5F5",
    "text": "#FFFFFF",
    "text_secondary": "#B0BEC5"
}

# Font settings
FONTS = {
    "title": ("Arial", 36, "bold"),
    "heading": ("Arial", 24, "bold"),
    "subheading": ("Arial", 18, "bold"),
    "body": ("Arial", 12),
    "button": ("Arial", 14, "bold")
}

# Available exercises
EXERCISES = [
    "Chest Press",
    "Shoulder Press",
    "Lat Pulldown",
    "Seated Row",
    "Leg Press",
    "Leg Extension",
    "Leg Curl",
    "Biceps Curl",
    "Triceps Pushdown"
]