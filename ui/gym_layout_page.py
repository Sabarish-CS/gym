"""
Gym Layout Selection Page
Grid layout of exercise machines with clickable cards (3 rows of 4)
WITHOUT SCROLLBARS - fills screen completely
"""
import tkinter as tk
from tkinter import ttk
import config

class GymLayoutPage(tk.Frame):
    """Exercise selection interface with 3×4 grid layout"""
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg=config.COLORS["dark"])
        
        # Exercise data - 12 exercises total (3 rows of 4)
        self.exercises = [
            {
                "name": "Chest Press",
                "icon": "💪",
                "joints": "Shoulders, Elbows",
                "description": "Push handles forward",
                "color": "#4CAF50"
            },
            {
                "name": "Shoulder Press",
                "icon": "🏋️",
                "joints": "Shoulders, Elbows",
                "description": "Press upward",
                "color": "#2196F3"
            },
            {
                "name": "Lat Pulldown",
                "icon": "⬇️",
                "joints": "Shoulders, Elbows",
                "description": "Pull bar down",
                "color": "#FF9800"
            },
            {
                "name": "Seated Row",
                "icon": "🚣",
                "joints": "Shoulders, Elbows",
                "description": "Pull toward torso",
                "color": "#9C27B0"
            },
            {
                "name": "Leg Press",
                "icon": "🦵",
                "joints": "Hips, Knees",
                "description": "Press platform",
                "color": "#4CAF50"
            },
            {
                "name": "Leg Extension",
                "icon": "🦿",
                "joints": "Hips, Knees",
                "description": "Extend legs",
                "color": "#2196F3"
            },
            {
                "name": "Leg Curl",
                "icon": "🏃",
                "joints": "Hips, Knees",
                "description": "Curl legs",
                "color": "#FF9800"
            },
            {
                "name": "Pec Deck",
                "icon": "🤗",
                "joints": "Shoulders, Elbows",
                "description": "Bring arms together",
                "color": "#9C27B0"
            },
            {
                "name": "Biceps Curl",
                "icon": "💪",
                "joints": "Elbows, Wrists",
                "description": "Curl handles up",
                "color": "#4CAF50"
            },
            {
                "name": "Triceps Pushdown",
                "icon": "👇",
                "joints": "Elbows, Wrists",
                "description": "Push bar down",
                "color": "#2196F3"
            },
            {
                "name": "Ab Crunch Machine",
                "icon": "🤸",
                "joints": "Hips, Shoulders",
                "description": "Crunch forward",
                "color": "#FF9800"
            },
            {
                "name": "Back Extension",
                "icon": "🙆",
                "joints": "Hips, Shoulders",
                "description": "Extend back",
                "color": "#9C27B0"
            }
        ]
        
        # Header
        self.create_header()
        
        # Main content area with 3×4 grid - FIXED
        self.create_exercise_grid_fixed()
    
    def create_header(self):
        """Create header with title"""
        header_frame = tk.Frame(self, bg=config.COLORS["primary"], height=100)
        header_frame.pack(fill="x", side="top")
        header_frame.pack_propagate(False)
        
        # Title
        title_label = tk.Label(
            header_frame,
            text="🏋️‍♂️ GYM EXERCISE LAYOUT",
            font=("Arial", 28, "bold"),
            fg=config.COLORS["accent"],
            bg=config.COLORS["primary"]
        )
        title_label.pack(pady=(20, 5))
        
        # Subtitle
        subtitle_label = tk.Label(
            header_frame,
            text="Select an exercise to view procedure and start monitoring",
            font=("Arial", 14),
            fg=config.COLORS["text_secondary"],
            bg=config.COLORS["primary"]
        )
        subtitle_label.pack(pady=(0, 10))
    
    def create_exercise_grid_fixed(self):
        """FIXED: Create 3×4 grid that fills entire screen without scrollbars"""
        # Main container that fills remaining space
        main_container = tk.Frame(self, bg=config.COLORS["dark"])
        main_container.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Use grid for better control over spacing
        rows = 3
        cols = 4
        
        # Configure grid weights for equal spacing
        for i in range(rows):
            main_container.grid_rowconfigure(i, weight=1, uniform="row")
        for j in range(cols):
            main_container.grid_columnconfigure(j, weight=1, uniform="col")
        
        # Create cards in grid layout
        for row in range(rows):
            for col in range(cols):
                index = row * cols + col
                if index < len(self.exercises):
                    exercise = self.exercises[index]
                    self.create_exercise_card_fixed(main_container, exercise, row, col)
                else:
                    # Empty cell
                    empty_frame = tk.Frame(
                        main_container,
                        bg=config.COLORS["dark"]
                    )
                    empty_frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        
        # Footer at bottom
        footer_frame = tk.Frame(self, bg=config.COLORS["dark"], height=40)
        footer_frame.pack(side="bottom", fill="x")
        
        footer_label = tk.Label(
            footer_frame,
            text="Total: 12 Exercises Available • Click any card to continue →",
            font=("Arial", 11, "italic"),
            fg=config.COLORS["text_secondary"],
            bg=config.COLORS["dark"]
        )
        footer_label.pack(pady=10)
    
    def create_exercise_card_fixed(self, parent_frame, exercise, row, col):
        """Create individual exercise card that expands to fill grid cell"""
        # Card frame with proper expansion
        card_frame = tk.Frame(
            parent_frame,
            bg=config.COLORS["primary"],
            relief="raised",
            borderwidth=2,
            cursor="hand2"
        )
        card_frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        card_frame.grid_propagate(False)
        
        # Configure grid inside card
        card_frame.grid_rowconfigure(0, weight=1)  # Top spacer
        card_frame.grid_rowconfigure(1, weight=0)  # Content (fixed height)
        card_frame.grid_rowconfigure(2, weight=1)  # Bottom spacer
        card_frame.grid_columnconfigure(0, weight=1)
        
        # Store exercise name for callback
        card_frame.exercise_name = exercise["name"]
        card_frame.bind("<Button-1>", 
                       lambda e, ex=exercise["name"]: self.select_exercise(ex))
        
        # ======= CARD CONTENT =======
        # Top color bar
        color_bar = tk.Frame(
            card_frame,
            bg=exercise["color"],
            height=4
        )
        color_bar.grid(row=0, column=0, sticky="ew")
        
        # Content frame (centered)
        content_frame = tk.Frame(card_frame, bg=config.COLORS["primary"])
        content_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=15)
        content_frame.grid_propagate(False)
        
        # Icon
        icon_label = tk.Label(
            content_frame,
            text=exercise["icon"],
            font=("Arial", 36),
            bg=config.COLORS["primary"],
            fg="white"
        )
        icon_label.pack(anchor="center", pady=(0, 15))
        
        # Exercise name
        name_label = tk.Label(
            content_frame,
            text=exercise["name"],
            font=("Arial", 16, "bold"),
            bg=config.COLORS["primary"],
            fg="white",
            anchor="center"
        )
        name_label.pack(fill="x", pady=(0, 5))
        
        # Joints
        joints_label = tk.Label(
            content_frame,
            text=f"Joints: {exercise['joints']}",
            font=("Arial", 11),
            bg=config.COLORS["primary"],
            fg=config.COLORS["text_secondary"],
            anchor="center"
        )
        joints_label.pack(fill="x", pady=(0, 10))
        
        # Divider
        divider = tk.Frame(
            content_frame,
            bg="#37474F",
            height=1
        )
        divider.pack(fill="x", pady=(0, 10))
        
        # Description
        desc_label = tk.Label(
            content_frame,
            text=exercise["description"],
            font=("Arial", 12),
            bg=config.COLORS["primary"],
            fg="#E0E0E0",
            anchor="center"
        )
        desc_label.pack(fill="x", pady=(0, 15))
        
        # Click indicator
        click_label = tk.Label(
            content_frame,
            text="CLICK TO VIEW PROCEDURE →",
            font=("Arial", 10, "bold"),
            bg=config.COLORS["primary"],
            fg=exercise["color"],
            anchor="center"
        )
        click_label.pack()
        
        # Hover effects
        card_frame.bind("<Enter>", 
                       lambda e, f=card_frame, c=exercise["color"]: self.on_card_hover(e, f, c))
        card_frame.bind("<Leave>", 
                       lambda e, f=card_frame: self.on_card_leave(e, f))
        
        # Make all children clickable
        for child in card_frame.winfo_children():
            child.bind("<Button-1>", 
                      lambda e, ex=exercise["name"]: self.select_exercise(ex))
    
    def on_card_hover(self, event, frame, color):
        """Visual feedback on card hover"""
        frame.config(relief="sunken", bg=color)
        for child in frame.winfo_children():
            if isinstance(child, tk.Frame):
                child.config(bg=color)
    
    def on_card_leave(self, event, frame):
        """Reset card on mouse leave"""
        frame.config(bg=config.COLORS["primary"], relief="raised")
        for child in frame.winfo_children():
            if isinstance(child, tk.Frame):
                child.config(bg=config.COLORS["primary"])
    
    def select_exercise(self, exercise_name):
        """Handle exercise selection - SMOOTH NAVIGATION"""
        try:
            print(f"✓ Selected: {exercise_name}")
            self.controller.set_exercise(exercise_name)  # This goes to ProcedurePage
        except Exception as e:
            print(f"✗ Error selecting {exercise_name}: {e}")