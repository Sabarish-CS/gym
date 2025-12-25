#!/usr/bin/env python3
"""
FitPose Launcher Script - UPDATED
Run this to start the real-time monitoring application
"""
import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Now run the main application
if __name__ == "__main__":
    print("=" * 60)
    print("FitPose - Real-Time Exercise Posture Monitoring System")
    print("Version 2.0.0")
    print("=" * 60)
    
    # Check for required packages
    required_packages = ['opencv-python', 'mediapipe', 'numpy', 'Pillow']
    
    try:
        from main import FitPoseApp
        app = FitPoseApp()
        app.run()
    except ImportError as e:
        print(f"\n❌ Error: {e}")
        print("\n📦 Required packages:")
        print("   pip install opencv-python mediapipe numpy Pillow")
        print("\n🔧 Troubleshooting steps:")
        print("1. Install packages: pip install -r requirements.txt")
        print("2. Ensure webcam is connected and working")
        print("3. Run from the project root directory")
        print("\nPress Enter to exit...")
        input()