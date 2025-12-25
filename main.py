"""
FitPose - Main Application File - FIXED IMPORTS
Entry point for the Intelligent Angle & Posture Monitoring System
"""
import tkinter as tk
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Now import your modules
try:
    from ui.splash_screen import SplashScreen
    from ui.dashboard import EquipmentDashboard
    from ui.procedure_page import ProcedurePage
    from ui.camera_page import CameraPage
    import config
    
    # Import from exercises package
    from exercises.exercise_config import get_all_exercises
    config.HYDRAULIC_EQUIPMENT = get_all_exercises()
    
except ImportError as e:
    print(f"Import Error: {e}")
    print("Current Python path:", sys.path)
    print("Current directory:", os.getcwd())
    raise

class FitPoseApp:
    """Main application controller managing all pages"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(config.APP_NAME)
        
        # Set window size
        if config.FULLSCREEN:
            self.root.attributes('-fullscreen', True)
            self.root.bind('<Escape>', lambda e: self.root.attributes('-fullscreen', False))
        else:
            self.root.geometry(config.WINDOW_SIZE)
        
        # Container for all pages
        self.container = tk.Frame(self.root)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        # Dictionary to hold all frames/pages
        self.frames = {}
        
        # Initialize all pages
        pages = {
            "SplashScreen": SplashScreen,
            "EquipmentDashboard": EquipmentDashboard,
            "ProcedurePage": ProcedurePage,
            "CameraPage": CameraPage
        }
        
        for name, PageClass in pages.items():
            try:
                frame = PageClass(parent=self.container, controller=self)
                self.frames[name] = frame
                frame.grid(row=0, column=0, sticky="nsew")
            except Exception as e:
                print(f"Error creating {name}: {e}")
        
        # Start with splash screen
        self.show_frame("SplashScreen")
    
    def show_frame(self, page_name):
        """Raise a frame to the top"""
        if page_name in self.frames:
            frame = self.frames[page_name]
            frame.tkraise()
            
            # If showing splash screen, schedule transition
            if page_name == "SplashScreen":
                self.root.after(config.SPLASH_DURATION, 
                              lambda: self.show_frame("EquipmentDashboard"))
        else:
            print(f"Frame {page_name} not found!")
    
    def get_frame(self, page_name):
        """Get reference to a specific frame"""
        return self.frames.get(page_name)
    
    def run(self):
        """Start the application"""
        self.root.mainloop()
    
    def quit_app(self):
        """Clean shutdown of the application"""
        # Clean up camera resources if active
        camera_page = self.get_frame("CameraPage")
        if camera_page and hasattr(camera_page, 'stop_camera'):
            camera_page.stop_camera()
        self.root.quit()

if __name__ == "__main__":
    print("Starting FitPose Application...")
    print(f"Working directory: {os.getcwd()}")
    print(f"Python path: {sys.path}")
    
    app = FitPoseApp()
    app.run()