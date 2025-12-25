"""
Angle Calculation Utility
Mathematical functions for angle calculation and smoothing
"""
import numpy as np
from collections import deque

class AngleCalculator:
    """Utility class for angle calculations with smoothing"""
    
    def __init__(self, window_size=5):
        self.window_size = window_size
        self.angle_history = deque(maxlen=window_size)
    
    @staticmethod
    def calculate_angle(a, b, c):
        """
        Calculate angle between points A, B, C
        where B is the vertex
        
        Args:
            a, b, c: Points with x, y, z attributes
            
        Returns:
            float: Angle in degrees
        """
        # Convert to vectors
        ba = np.array([a.x - b.x, a.y - b.y])
        bc = np.array([c.x - b.x, c.y - b.y])
        
        # Calculate cosine of angle
        cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
        
        # Ensure value is within valid range for arccos
        cosine_angle = np.clip(cosine_angle, -1.0, 1.0)
        
        # Calculate angle in radians and convert to degrees
        angle = np.degrees(np.arccos(cosine_angle))
        
        return angle
    
    def add_angle(self, angle):
        """Add new angle to history for smoothing"""
        self.angle_history.append(angle)
        return self.get_smoothed_angle()
    
    def get_smoothed_angle(self):
        """Get smoothed angle using moving average"""
        if len(self.angle_history) == 0:
            return 0
        
        return np.mean(self.angle_history)
    
    def reset(self):
        """Reset angle history"""
        self.angle_history.clear()