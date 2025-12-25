"""
Exercises package for FitPose
Contains exercise configurations and utilities
"""

from .exercise_config import (
    EXERCISE_ANGLES,
    EXERCISE_PROCEDURES,
    MEDIAPIPE_LANDMARKS,
    get_exercise_config,
    validate_angle,
    get_exercise_procedures,
    get_all_exercises,
    get_landmark_indices
)

__all__ = [
    'EXERCISE_ANGLES',
    'EXERCISE_PROCEDURES', 
    'MEDIAPIPE_LANDMARKS',
    'get_exercise_config',
    'validate_angle',
    'get_exercise_procedures',
    'get_all_exercises',
    'get_landmark_indices'
]