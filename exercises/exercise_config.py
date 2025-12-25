"""
FitPose Exercise Configuration Module
Contains all exercise-specific configurations, angle rules, and procedures
"""

# MediaPipe Pose landmark indices (full list for reference)
MEDIAPIPE_LANDMARKS = {
    # Face (not used in our system)
    "nose": 0,
    "left_eye_inner": 1,
    "left_eye": 2,
    "left_eye_outer": 3,
    "right_eye_inner": 4,
    "right_eye": 5,
    "right_eye_outer": 6,
    "left_ear": 7,
    "right_ear": 8,
    "mouth_left": 9,
    "mouth_right": 10,
    
    # Upper body (important for most exercises)
    "left_shoulder": 11,
    "right_shoulder": 12,
    "left_elbow": 13,
    "right_elbow": 14,
    "left_wrist": 15,
    "right_wrist": 16,
    "left_pinky": 17,
    "right_pinky": 18,
    "left_index": 19,
    "right_index": 20,
    "left_thumb": 21,
    "right_thumb": 22,
    
    # Lower body (important for leg exercises)
    "left_hip": 23,
    "right_hip": 24,
    "left_knee": 25,
    "right_knee": 26,
    "left_ankle": 27,
    "right_ankle": 28,
    "left_heel": 29,
    "right_heel": 30,
    "left_foot_index": 31,
    "right_foot_index": 32
}

# ============================================================================
# EXERCISE ANGLE CONFIGURATIONS
# Each machine has its own angle measurement rules
# ============================================================================

EXERCISE_ANGLES = {
    "Chest Press": {
        "description": "Push handles forward while seated",
        "joints_to_track": ["shoulder", "elbow", "wrist"],
        "landmarks": {
            "left": [11, 13, 15],   # left_shoulder, left_elbow, left_wrist
            "right": [12, 14, 16]   # right_shoulder, right_elbow, right_wrist
        },
        "primary_side": "both",  # Track both sides, use worst-case
        "target_angle_range": (160, 175),  # Optimal pushing angle
        "tolerance": 5,  # ±5 degrees tolerance
        "direction": "forward",
        "feedback_messages": {
            "correct": "Perfect! Maintain this angle",
            "too_small": "Elbow angle too small - don't lock elbows",
            "too_large": "Elbow angle too large - extend more"
        }
    },
    
    "Shoulder Press": {
        "description": "Press handles upward from shoulders",
        "joints_to_track": ["shoulder", "elbow", "wrist"],
        "landmarks": {
            "left": [11, 13, 15],
            "right": [12, 14, 16]
        },
        "primary_side": "both",
        "target_angle_range": (165, 180),
        "tolerance": 5,
        "direction": "upward",
        "feedback_messages": {
            "correct": "Good shoulder press form",
            "too_small": "Don't lock elbows at the top",
            "too_large": "Press higher without arching back"
        }
    },
    
    "Lat Pulldown": {
        "description": "Pull bar down to chest",
        "joints_to_track": ["shoulder", "elbow", "wrist"],
        "landmarks": {
            "left": [11, 13, 15],
            "right": [12, 14, 16]
        },
        "primary_side": "both",
        "target_angle_range": (90, 120),  # During the pull phase
        "tolerance": 8,
        "direction": "downward",
        "feedback_messages": {
            "correct": "Good lat engagement",
            "too_small": "Pull bar lower to chest",
            "too_large": "Control the eccentric phase"
        }
    },
    
    "Seated Row": {
        "description": "Pull handles toward torso",
        "joints_to_track": ["shoulder", "elbow", "wrist"],
        "landmarks": {
            "left": [11, 13, 15],
            "right": [12, 14, 16]
        },
        "primary_side": "both",
        "target_angle_range": (80, 100),  # At maximum contraction
        "tolerance": 5,
        "direction": "backward",
        "feedback_messages": {
            "correct": "Excellent rowing form",
            "too_small": "Squeeze shoulder blades together",
            "too_large": "Don't overextend at the finish"
        }
    },
    
    "Leg Press": {
        "description": "Press platform with legs",
        "joints_to_track": ["hip", "knee", "ankle"],
        "landmarks": {
            "left": [23, 25, 27],   # left_hip, left_knee, left_ankle
            "right": [24, 26, 28]   # right_hip, right_knee, right_ankle
        },
        "primary_side": "both",
        "target_angle_range": (140, 160),  # Knee angle at extension
        "tolerance": 8,
        "direction": "forward",
        "feedback_messages": {
            "correct": "Good leg press depth",
            "too_small": "Don't lock knees",
            "too_large": "Press more completely"
        }
    },
    
    "Leg Extension": {
        "description": "Extend legs against resistance",
        "joints_to_track": ["hip", "knee", "ankle"],
        "landmarks": {
            "left": [23, 25, 27],
            "right": [24, 26, 28]
        },
        "primary_side": "both",
        "target_angle_range": (150, 170),  # Near full extension
        "tolerance": 5,
        "direction": "forward",
        "feedback_messages": {
            "correct": "Smooth quad extension",
            "too_small": "Avoid hyperextension",
            "too_large": "Extend more completely"
        }
    },
    
    "Leg Curl": {
        "description": "Curl legs against resistance",
        "joints_to_track": ["hip", "knee", "ankle"],
        "landmarks": {
            "left": [23, 25, 27],
            "right": [24, 26, 28]
        },
        "primary_side": "both",
        "target_angle_range": (50, 70),  # At maximum curl
        "tolerance": 8,
        "direction": "backward",
        "feedback_messages": {
            "correct": "Good hamstring contraction",
            "too_small": "Curl heels closer to glutes",
            "too_large": "Focus on full range of motion"
        }
    },
    
    "Pec Deck": {
        "description": "Bring arms together in front",
        "joints_to_track": ["shoulder", "elbow", "wrist"],
        "landmarks": {
            "left": [11, 13, 15],
            "right": [12, 14, 16]
        },
        "primary_side": "both",
        "target_angle_range": (100, 130),  # At maximum contraction
        "tolerance": 10,
        "direction": "forward",
        "feedback_messages": {
            "correct": "Good chest squeeze",
            "too_small": "Bring hands closer together",
            "too_large": "Focus on squeezing pecs"
        }
    },
    
    "Biceps Curl Machine": {
        "description": "Curl handles upward",
        "joints_to_track": ["shoulder", "elbow", "wrist"],
        "landmarks": {
            "left": [11, 13, 15],
            "right": [12, 14, 16]
        },
        "primary_side": "both",
        "target_angle_range": (30, 60),  # At maximum curl
        "tolerance": 5,
        "direction": "upward",
        "feedback_messages": {
            "correct": "Perfect biceps peak contraction",
            "too_small": "Curl weight higher",
            "too_large": "Focus on biceps isolation"
        }
    },
    
    "Triceps Pushdown": {
        "description": "Push bar downward",
        "joints_to_track": ["shoulder", "elbow", "wrist"],
        "landmarks": {
            "left": [11, 13, 15],
            "right": [12, 14, 16]
        },
        "primary_side": "both",
        "target_angle_range": (150, 170),  # Near full extension
        "tolerance": 5,
        "direction": "downward",
        "feedback_messages": {
            "correct": "Good triceps lockout",
            "too_small": "Don't lock elbows completely",
            "too_large": "Push more completely"
        }
    },
    
    "Ab Crunch Machine": {
        "description": "Crunch forward against resistance",
        "joints_to_track": ["hip", "shoulder", "elbow"],
        "landmarks": {
            "left": [23, 11, 13],   # hip, shoulder, elbow
            "right": [24, 12, 14]
        },
        "primary_side": "both",
        "target_angle_range": (70, 90),  # At maximum crunch
        "tolerance": 10,
        "direction": "forward",
        "feedback_messages": {
            "correct": "Good abdominal contraction",
            "too_small": "Crunch more completely",
            "too_large": "Focus on core engagement"
        }
    },
    
    "Back Extension Machine": {
        "description": "Extend back against resistance",
        "joints_to_track": ["hip", "shoulder", "ear"],
        "landmarks": {
            "left": [23, 11, 7],   # hip, shoulder, ear
            "right": [24, 12, 8]
        },
        "primary_side": "both",
        "target_angle_range": (150, 170),  # At full extension
        "tolerance": 10,
        "direction": "backward",
        "feedback_messages": {
            "correct": "Good spinal extension",
            "too_small": "Don't hyperextend",
            "too_large": "Extend more completely"
        }
    }
}

# ============================================================================
# EXERCISE PROCEDURES DATABASE
# Two random steps will be selected from each list
# ============================================================================

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

# ============================================================================
# UTILITY FUNCTIONS FOR EXERCISE MANAGEMENT
# ============================================================================

def get_exercise_config(exercise_name):
    """
    Get configuration for a specific exercise
    
    Args:
        exercise_name (str): Name of the exercise
        
    Returns:
        dict: Exercise configuration or default if not found
    """
    return EXERCISE_ANGLES.get(exercise_name, EXERCISE_ANGLES["Chest Press"])

def get_exercise_procedures(exercise_name, num_steps=2):
    """
    Get random procedure steps for an exercise
    
    Args:
        exercise_name (str): Name of the exercise
        num_steps (int): Number of steps to return
        
    Returns:
        list: Random procedure steps
    """
    import random
    
    procedures = EXERCISE_PROCEDURES.get(exercise_name, [])
    if len(procedures) >= num_steps:
        return random.sample(procedures, num_steps)
    elif procedures:
        return procedures
    else:
        return ["Adjust machine for proper alignment", "Perform exercise with controlled movement"]

def get_all_exercises():
    """
    Get list of all available exercises
    
    Returns:
        list: All exercise names
    """
    return list(EXERCISE_ANGLES.keys())

def get_landmark_indices(exercise_name, side="left"):
    """
    Get MediaPipe landmark indices for specific exercise and side
    
    Args:
        exercise_name (str): Name of the exercise
        side (str): "left", "right", or "both"
        
    Returns:
        list: Landmark indices for angle calculation
    """
    config = get_exercise_config(exercise_name)
    
    if side == "both":
        # Return both sides, caller can decide which to use
        return config["landmarks"]["left"], config["landmarks"]["right"]
    else:
        return config["landmarks"].get(side, config["landmarks"]["left"])

def validate_angle(exercise_name, angle):
    """
    Check if an angle is within the target range for an exercise
    
    Args:
        exercise_name (str): Name of the exercise
        angle (float): Angle to validate
        
    Returns:
        tuple: (is_valid, feedback_message)
    """
    config = get_exercise_config(exercise_name)
    min_angle, max_angle = config["target_angle_range"]
    
    if min_angle <= angle <= max_angle:
        return True, config["feedback_messages"]["correct"]
    elif angle < min_angle:
        return False, config["feedback_messages"]["too_small"]
    else:
        return False, config["feedback_messages"]["too_large"]

# ============================================================================
# DEFAULT CONFIGURATION FOR UNKNOWN EXERCISES
# ============================================================================

DEFAULT_EXERCISE_CONFIG = {
    "description": "General exercise form monitoring",
    "joints_to_track": ["shoulder", "elbow", "wrist"],
    "landmarks": {
        "left": [11, 13, 15],
        "right": [12, 14, 16]
    },
    "primary_side": "both",
    "target_angle_range": (160, 175),
    "tolerance": 10,
    "direction": "forward",
    "feedback_messages": {
        "correct": "Good form, maintain this angle",
        "too_small": "Angle too small, extend more",
        "too_large": "Angle too large, reduce range"
    }
}