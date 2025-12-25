"""
Splash Screen Module
Displays initial loading screen with animation
"""
import tkinter as tk
from tkinter import font as tkfont
import config

class SplashScreen(tk.Frame):
    """Fullscreen splash screen with fade animation"""
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        # Configure fullscreen background
        self.configure(bg=config.COLORS["dark"])
        
        # Center content
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Create title label with animation
        self.title_label = tk.Label(
            self,
            text="FitPose",
            font=config.FONTS["title"],
            fg=config.COLORS["accent"],
            bg=config.COLORS["dark"]
        )
        self.title_label.grid(row=0, column=0, sticky="nsew")
        
        # Subtitle
        self.subtitle_label = tk.Label(
            self,
            text="Intelligent Angle & Posture Monitoring System",
            font=config.FONTS["subheading"],
            fg=config.COLORS["text_secondary"],
            bg=config.COLORS["dark"]
        )
        self.subtitle_label.grid(row=1, column=0, pady=(0, 50))
        
        # Loading animation
        self.loading_label = tk.Label(
            self,
            text="Initializing...",
            font=config.FONTS["body"],
            fg=config.COLORS["text_secondary"],
            bg=config.COLORS["dark"]
        )
        self.loading_label.grid(row=2, column=0, pady=20)
        
        # Animation dots
        self.dots = 0
        self.animate_loading()
    
    def animate_loading(self):
        """Animate loading dots"""
        dots_text = "Initializing" + "." * (self.dots % 4)
        self.loading_label.config(text=dots_text)
        self.dots += 1
        self.after(500, self.animate_loading)
    
    def fade_out(self):
        """Fade out animation before transition"""
        current_alpha = self.title_label.cget("fg")
        # Implement fade logic here
        pass