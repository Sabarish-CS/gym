#!/usr/bin/env python3
"""
FitPose Launcher Script
Run this to start the application
"""
import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Now run the main application
if __name__ == "__main__":
    try:
        from main import FitPoseApp
        app = FitPoseApp()
        app.run()
    except ImportError as e:
        print(f"Error: {e}")
        print("\nTroubleshooting steps:")
        print("1. Make sure your project structure is correct:")
        print("   - exercises/ directory exists with exercise_config.py")
        print("   - ui/ directory exists with all UI files")
        print("2. Install required packages: pip install -r requirements.txt")
        print("3. Run from the project root directory")
        input("\nPress Enter to exit...")