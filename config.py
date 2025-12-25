"""
FitPose Configuration File - SAFE IMPORTS
"""
import os
import sys
# Add this line to your existing config.py
EXERCISE_PROCEDURES = {}

# Application settings
APP_NAME = "FitPose - Intelligent Angle & Posture Monitoring System"
VERSION = "1.0.0"
WINDOW_SIZE = "1366x768"
FULLSCREEN = True
SPLASH_DURATION = 3000

# Path configurations
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
IMAGES_DIR = os.path.join(ASSETS_DIR, "images")
ICONS_DIR = os.path.join(ASSETS_DIR, "icons")

# Create directories if they don't exist
for directory in [ASSETS_DIR, IMAGES_DIR, ICONS_DIR]:
    os.makedirs(directory, exist_ok=True)

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
    "title": ("Arial", 48, "bold"),
    "heading": ("Arial", 32, "bold"),
    "subheading": ("Arial", 24, "bold"),
    "body": ("Arial", 14),
    "button": ("Arial", 16, "bold")
}
# Add this to your config.py file

# EXERCISE PROCEDURES DATABASE
EXERCISE_PROCEDURES = {
    "Chest Press": [
        "Sit upright with your back firmly against the pad",
        "Grip handles at chest level with palms facing forward",
        "Push handles forward smoothly without locking elbows",
        "Keep shoulders down and back during movement",
        "Return to starting position in controlled manner",
        "Maintain neutral spine position throughout",
        "Exhale while pushing, inhale while returning",
        "Focus on chest muscle contraction"
    ],
    
    "Shoulder Press": [
        "Adjust seat height so handles align with shoulders",
        "Sit with back straight against the pad",
        "Grip handles with palms facing forward",
        "Press upward without arching your back",
        "Avoid locking elbows at the top position",
        "Lower weights slowly to starting position",
        "Keep core engaged throughout movement",
        "Don't let shoulders shrug toward ears"
    ],
    
    "Lat Pulldown": [
        "Adjust thigh pad to secure your legs",
        "Grip bar wider than shoulder width",
        "Lean back slightly with chest up",
        "Pull bar down to upper chest level",
        "Squeeze shoulder blades together",
        "Return bar slowly to starting position",
        "Avoid using momentum or swinging",
        "Focus on latissimus dorsi muscles"
    ],
    
    "Seated Row": [
        "Sit with knees slightly bent, feet flat",
        "Grip handles with neutral grip",
        "Keep chest up and back straight",
        "Pull handles toward your abdomen",
        "Squeeze shoulder blades together",
        "Return slowly to starting position",
        "Avoid rounding your back forward",
        "Focus on mid-back muscles"
    ],
    
    "Leg Press": [
        "Sit with back and hips against pad",
        "Place feet shoulder-width on platform",
        "Lower safety bars before starting",
        "Press platform until legs are extended",
        "Don't lock knees at the top",
        "Lower platform in controlled manner",
        "Keep heels flat on platform",
        "Maintain natural arch in lower back"
    ],
    
    "Leg Extension": [
        "Sit with back against pad",
        "Adjust roller above ankles",
        "Grip side handles for stability",
        "Extend legs until they're straight",
        "Squeeze quadriceps at top position",
        "Lower weight slowly with control",
        "Avoid swinging or using momentum",
        "Don't lock knees completely"
    ],
    
    "Leg Curl": [
        "Lie face down on machine",
        "Position roller above ankles",
        "Grip handles for upper body stability",
        "Curl heels toward glutes",
        "Squeeze hamstrings at top position",
        "Lower weight slowly with control",
        "Keep hips pressed into pad",
        "Avoid lifting hips off pad"
    ],
    
    "Pec Deck": [
        "Sit with back against pad",
        "Adjust seat height so handles are chest level",
        "Grip handles with elbows bent",
        "Bring handles together in front of chest",
        "Squeeze pectoral muscles at midpoint",
        "Return slowly to starting position",
        "Keep shoulders relaxed",
        "Focus on chest contraction, not arms"
    ],
    
    "Biceps Curl Machine": [
        "Sit with chest against pad",
        "Adjust seat so armpits align with pad top",
        "Grip handles with underhand grip",
        "Curl handles upward toward shoulders",
        "Squeeze biceps at top position",
        "Lower weight slowly with control",
        "Keep elbows stationary",
        "Avoid swinging or using back muscles"
    ],
    
    "Triceps Pushdown": [
        "Stand facing cable machine",
        "Grip bar with palms down",
        "Keep elbows close to sides",
        "Push bar down until arms straight",
        "Squeeze triceps at bottom position",
        "Return slowly to starting position",
        "Keep upper arms stationary",
        "Avoid using shoulder momentum"
    ],
    
    "Ab Crunch Machine": [
        "Sit with back against pad",
        "Adjust seat so handles are shoulder level",
        "Grip handles lightly for support",
        "Crunch forward by contracting abs",
        "Exhale as you crunch forward",
        "Return slowly to starting position",
        "Don't pull with arms or neck",
        "Focus on abdominal contraction"
    ],
    
    "Back Extension Machine": [
        "Adjust machine so hips align with pivot point",
        "Position feet securely under foot pads",
        "Cross arms over chest or behind head",
        "Lower upper body toward floor",
        "Extend back until body is straight",
        "Squeeze glutes at top position",
        "Avoid hyperextending at the top",
        "Keep movement controlled"
    ]
}

# HYDRAULIC EQUIPMENT LIST
HYDRAULIC_EQUIPMENT = [
    "Chest Press",
    "Shoulder Press", 
    "Lat Pulldown",
    "Seated Row",
    "Leg Press",
    "Leg Extension",
    "Leg Curl",
    "Pec Deck",
    "Biceps Curl Machine",
    "Triceps Pushdown",
    "Ab Crunch Machine",
    "Back Extension Machine"
]

# Try to import exercise configurations, but have fallbacks
try:
    # Add exercises directory to path if not already there
    exercises_dir = os.path.join(BASE_DIR, "exercises")
    if exercises_dir not in sys.path:
        sys.path.append(exercises_dir)
    
    from exercise_config import get_all_exercises, get_exercise_config, get_exercise_procedures
    
    # Use imported functions
    HYDRAULIC_EQUIPMENT = get_all_exercises()
    
    # Define wrapper functions
    def get_exercise_config_wrapper(name):
        return get_exercise_config(name)
    
    def get_exercise_procedures_wrapper(name, num_steps=2):
        return get_exercise_procedures(name, num_steps)
    
except ImportError as e:
    print(f"Warning: Could not import exercise_config: {e}")
    print("Using fallback configurations...")
    
    # Fallback equipment list
    HYDRAULIC_EQUIPMENT = [
        "Chest Press", "Shoulder Press", "Lat Pulldown", "Seated Row",
        "Leg Press", "Leg Extension", "Leg Curl", "Pec Deck",
        "Biceps Curl Machine", "Triceps Pushdown", "Ab Crunch Machine",
        "Back Extension Machine"
    ]
    
    # Fallback functions
    def get_exercise_config_wrapper(exercise_name):
        return {
            "description": f"{exercise_name} exercise",
            "joints_to_track": ["shoulder", "elbow", "wrist"],
            "landmarks": {"left": [11, 13, 15], "right": [12, 14, 16]},
            "primary_side": "both",
            "target_angle_range": (160, 175),
            "tolerance": 5,
            "direction": "forward",
            "feedback_messages": {
                "correct": "Good form, maintain this angle",
                "too_small": "Angle too small, extend more",
                "too_large": "Angle too large, reduce range"
            }
        }
    
    def get_exercise_procedures_wrapper(exercise_name, num_steps=2):
        return [
            f"Step 1: Adjust {exercise_name} for proper alignment",
            f"Step 2: Perform {exercise_name} with controlled movement"
        ]
    
# Export the functions
get_exercise_config = get_exercise_config_wrapper
get_exercise_procedures = get_exercise_procedures_wrapper