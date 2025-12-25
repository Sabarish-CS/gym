"""
FitPose - Main Application File
Entry point for the Real-Time Exercise Posture Monitoring System
"""
import tkinter as tk
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from ui.splash_screen import SplashScreen
    from ui.gym_layout_page import GymLayoutPage
    from ui.procedure_page import ProcedurePage
    from ui.camera_page import CameraPage
    import config
    
    print("✓ All modules imported successfully")
    
except ImportError as e:
    print(f"✗ Import Error: {e}")
    print("\n📦 Required packages:")
    print("   pip install opencv-python mediapipe numpy Pillow")
    
    # Create error window
    root = tk.Tk()
    root.title("FitPose - Installation Error")
    root.geometry("600x400")
    
    error_frame = tk.Frame(root, bg="#2E3B4E")
    error_frame.pack(fill="both", expand=True)
    
    tk.Label(error_frame, 
             text="❌ INSTALLATION ERROR",
             font=("Arial", 24, "bold"),
             fg="#F44336",
             bg="#2E3B4E").pack(pady=50)
    
    tk.Label(error_frame,
             text=f"Error: {str(e)}",
             font=("Arial", 12),
             fg="white",
             bg="#2E3B4E",
             wraplength=500).pack(pady=20)
    
    tk.Label(error_frame,
             text="Please install required packages:",
             font=("Arial", 14, "bold"),
             fg="#4CAF50",
             bg="#2E3B4E").pack(pady=20)
    
    tk.Label(error_frame,
             text="pip install opencv-python mediapipe numpy Pillow",
             font=("Arial", 12, "bold"),
             fg="#2196F3",
             bg="#2E3B4E").pack()
    
    tk.Button(error_frame,
              text="Exit",
              font=("Arial", 14, "bold"),
              bg="#F44336",
              fg="white",
              command=root.quit,
              padx=30,
              pady=10).pack(pady=30)
    
    root.mainloop()
    sys.exit(1)

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
          # ADD THESE TWO LINES HERE:
        self.root.minsize(1200, 700)  # Minimum window size to ensure proper layout
        self.root.state('zoomed')     # Start maximized
        
        
        # Container for all pages
        self.container = tk.Frame(self.root)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        # Dictionary to hold all frames/pages
        self.frames = {}
        
        # Initialize all pages
        pages = [
            ("SplashScreen", SplashScreen),
            ("GymLayoutPage", GymLayoutPage),
            ("ProcedurePage", ProcedurePage),
            ("CameraPage", CameraPage)
        ]
        
        for name, PageClass in pages:
            try:
                print(f"Creating {name}...")
                frame = PageClass(parent=self.container, controller=self)
                self.frames[name] = frame
                frame.grid(row=0, column=0, sticky="nsew")
                print(f"✓ {name} created successfully")
            except Exception as e:
                print(f"✗ Error creating {name}: {e}")
                import traceback
                traceback.print_exc()
        
        # Start with splash screen
        self.show_frame("SplashScreen")
        
        # Bind escape key
        self.root.bind('<Escape>', lambda e: self.quit_app())
        
        # Store selected exercise
        self.selected_exercise = None
    
    def show_frame(self, page_name):
        """Raise a frame to the top"""
        if page_name in self.frames:
            frame = self.frames[page_name]
            frame.tkraise()
            
            # If showing splash screen, schedule transition
            if page_name == "SplashScreen":
                self.root.after(config.SPLASH_DURATION, 
                              lambda: self.show_frame("GymLayoutPage"))
        else:
            print(f"✗ Frame {page_name} not found in frames!")
            print(f"   Available frames: {list(self.frames.keys())}")
    
    def get_frame(self, page_name):
        """Get reference to a specific frame"""
        return self.frames.get(page_name)
    
    def set_exercise(self, exercise_name):
        """Store selected exercise and navigate to procedure page"""
        self.selected_exercise = exercise_name
        procedure_page = self.get_frame("ProcedurePage")
        if procedure_page:
            procedure_page.set_exercise(exercise_name)
            self.show_frame("ProcedurePage")
        else:
            print("✗ ProcedurePage not found!")
    
    def start_camera(self):
        """Navigate to camera page with selected exercise"""
        camera_page = self.get_frame("CameraPage")
        if camera_page and self.selected_exercise:
            camera_page.set_exercise(self.selected_exercise)
            self.show_frame("CameraPage")
        else:
            print("✗ CameraPage not found or no exercise selected!")
    
    def run(self):
        """Start the application"""
        print("✓ Starting FitPose application...")
        self.root.mainloop()
    
    def quit_app(self):
        """Clean shutdown of the application"""
        print("✓ Shutting down FitPose...")
        # Clean up camera resources if active
        camera_page = self.get_frame("CameraPage")
        if camera_page and hasattr(camera_page, 'stop_camera'):
            camera_page.stop_camera()
        self.root.quit()

if __name__ == "__main__":
    print("=" * 60)
    print("FitPose - Real-Time Exercise Posture Monitoring System")
    print("=" * 60)
    
    app = FitPoseApp()
    app.run()