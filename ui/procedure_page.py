"""
Procedure Page - Shows exercise instructions before starting camera
BACK BUTTON ABOVE IMAGE AREA
"""
import tkinter as tk
import config

class ProcedurePage(tk.Frame):
    """Page showing exercise procedure before starting monitoring"""
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg=config.COLORS["dark"])
        
        # Current exercise
        self.current_exercise = None
        
        # UI setup with back button above image
        self.create_ui_with_back_above()
    
    def create_ui_with_back_above(self):
        """Create layout with back button above the image area"""
        # MAIN CONTAINER
        main_container = tk.Frame(self, bg=config.COLORS["dark"])
        main_container.pack(fill="both", expand=True)
        
        # Configure 50/50 columns
        main_container.grid_columnconfigure(0, weight=1, uniform="half")  # Left - 50%
        main_container.grid_columnconfigure(1, weight=1, uniform="half")  # Right - 50%
        main_container.grid_rowconfigure(0, weight=1)
        
        # =========== LEFT SIDE: BACK BUTTON + IMAGE (50%) ===========
        left_frame = tk.Frame(main_container, bg="#000000")
        left_frame.grid(row=0, column=0, sticky="nsew")
        
        # Configure 2 rows: back button (fixed) and image (expands)
        left_frame.grid_rowconfigure(0, weight=0)   # Back button (fixed height)
        left_frame.grid_rowconfigure(1, weight=1)   # Image (takes remaining space)
        left_frame.grid_columnconfigure(0, weight=1)
        
        # BACK BUTTON ABOVE IMAGE AREA
        back_frame = tk.Frame(left_frame, bg="#000000", height=60)
        back_frame.grid(row=0, column=0, sticky="ew")
        back_frame.grid_propagate(False)
        back_frame.grid_columnconfigure(0, weight=1)
        
        back_btn = tk.Button(
            back_frame,
            text="← BACK TO EXERCISES",
            font=("Arial", 14, "bold"),
            bg="#4CAF50",
            fg="white",
            bd=0,
            cursor="hand2",
            padx=20,
            pady=10,
            command=lambda: self.controller.show_frame("GymLayoutPage")
        )
        back_btn.grid(row=0, column=0, sticky="w", padx=30)
        
        # IMAGE AREA (BELOW BACK BUTTON)
        image_container = tk.Frame(
            left_frame,
            bg="#000000"
        )
        image_container.grid(row=1, column=0, sticky="nsew")
        image_container.grid_rowconfigure(0, weight=1)
        image_container.grid_columnconfigure(0, weight=1)
        
        # Image label - CENTERED
        self.image_label = tk.Label(
            image_container,
            text="EXERCISE\nIMAGE",
            font=("Arial", 36, "bold"),
            bg="#000000",
            fg="white",
            justify="center"
        )
        self.image_label.grid(row=0, column=0, sticky="nsew")
        
        # =========== RIGHT SIDE: CONTENT (50%) ===========
        right_frame = tk.Frame(main_container, bg=config.COLORS["secondary"])
        right_frame.grid(row=0, column=1, sticky="nsew")
        
        # Configure grid for right side
        right_frame.grid_rowconfigure(0, weight=0)  # Exercise name
        right_frame.grid_rowconfigure(1, weight=0)  # Divider line
        right_frame.grid_rowconfigure(2, weight=0)  # Joints
        right_frame.grid_rowconfigure(3, weight=1)  # Steps
        right_frame.grid_rowconfigure(4, weight=0)  # Button
        right_frame.grid_columnconfigure(0, weight=1)
        
        # =========== EXERCISE NAME AT TOP ===========
        title_frame = tk.Frame(right_frame, bg=config.COLORS["secondary"])
        title_frame.grid(row=0, column=0, sticky="ew", padx=30, pady=(40, 20))
        
        self.exercise_title = tk.Label(
            title_frame,
            text="SELECT EXERCISE",
            font=("Arial", 32, "bold"),
            bg=config.COLORS["secondary"],
            fg=config.COLORS["accent"],
            anchor="w"
        )
        self.exercise_title.pack(anchor="w")
        
        # =========== DIVIDER LINE - EXTENDS FULL WIDTH ===========
        divider_frame = tk.Frame(right_frame, bg=config.COLORS["secondary"])
        divider_frame.grid(row=1, column=0, sticky="ew", padx=30, pady=(0, 20))
        tk.Frame(divider_frame, bg="#4CAF50", height=3).pack(fill="x")
        
        # =========== JOINTS ===========
        joints_frame = tk.Frame(right_frame, bg=config.COLORS["secondary"])
        joints_frame.grid(row=2, column=0, sticky="ew", padx=30, pady=(0, 20))
        
        joints_title = tk.Label(
            joints_frame,
            text="JOINTS INVOLVED",
            font=("Arial", 18, "bold"),
            bg=config.COLORS["secondary"],
            fg=config.COLORS["text_secondary"],
            anchor="w"
        )
        joints_title.pack(anchor="w", pady=(0, 10))
        
        self.joints_label = tk.Label(
            joints_frame,
            text="--",
            font=("Arial", 16),
            bg=config.COLORS["primary"],
            fg="white",
            anchor="w",
            justify="left",
            padx=20,
            pady=15
        )
        self.joints_label.pack(fill="x")
        
        # =========== PROCEDURE STEPS ===========
        steps_container = tk.Frame(right_frame, bg=config.COLORS["secondary"])
        steps_container.grid(row=3, column=0, sticky="nsew", padx=30, pady=(0, 20))
        steps_container.grid_rowconfigure(0, weight=1)
        steps_container.grid_columnconfigure(0, weight=1)
        
        # Steps frame
        steps_frame = tk.Frame(
            steps_container,
            bg=config.COLORS["primary"],
            relief="flat"
        )
        steps_frame.grid(row=0, column=0, sticky="nsew")
        steps_frame.grid_rowconfigure(1, weight=1)
        steps_frame.grid_columnconfigure(0, weight=1)
        
        # Steps title
        steps_title = tk.Label(
            steps_frame,
            text="PROCEDURE STEPS",
            font=("Arial", 18, "bold"),
            bg=config.COLORS["primary"],
            fg=config.COLORS["text_secondary"],
            anchor="w"
        )
        steps_title.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        
        # Steps text
        self.steps_text = tk.Text(
            steps_frame,
            font=("Arial", 13),
            bg=config.COLORS["primary"],
            fg="white",
            wrap="word",
            relief="flat",
            borderwidth=0,
            padx=20,
            pady=10,
            spacing1=8,
            spacing3=4,
            height=8
        )
        self.steps_text.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        
        # Default text
        self.steps_text.insert("1.0", "1. Select an exercise\n\n")
        self.steps_text.insert("end", "2. View procedure\n\n")
        self.steps_text.insert("end", "3. Start monitoring")
        self.steps_text.config(state="disabled")
        
        # =========== START BUTTON ===========
        button_frame = tk.Frame(right_frame, bg=config.COLORS["secondary"])
        button_frame.grid(row=4, column=0, sticky="ew", padx=30, pady=(0, 40))
        
        self.start_btn = tk.Button(
            button_frame,
            text="START MONITORING →",
            font=("Arial", 18, "bold"),
            bg="#4CAF50",
            fg="white",
            padx=40,
            pady=20,
            cursor="hand2",
            command=self.start_monitoring,
            state="disabled"
        )
        self.start_btn.pack(fill="x")
    
    def set_exercise(self, exercise_name):
        """Set exercise and update UI"""
        self.current_exercise = exercise_name
        
        # Get exercise configuration
        exercise_config = self.get_exercise_config(exercise_name)
        
        # Update exercise title
        self.exercise_title.config(text=exercise_name.upper())
        
        # Update joints
        joints = exercise_config.get("joints", "Shoulders, Elbows")
        self.joints_label.config(text=joints)
        
        # Update image
        self.image_label.config(
            text=f"{exercise_name.upper()}\n\n🖼️\nExercise Image",
            font=("Arial", 28, "bold")
        )
        
        # Update steps
        steps = exercise_config.get("steps", [])
        self.steps_text.config(state="normal")
        self.steps_text.delete("1.0", "end")
        
        for i, step in enumerate(steps[:5], 1):
            self.steps_text.insert("end", f"{i}. {step}\n\n")
        
        self.steps_text.config(state="disabled")
        
        # Enable start button
        self.start_btn.config(
            state="normal", 
            text=f"START {exercise_name.upper()} →"
        )
    
    def get_exercise_config(self, exercise_name):
        """Get configuration for specific exercise"""
        configs = {
            "Chest Press": {
                "joints": "Shoulders, Elbows",
                "steps": [
                    "Sit upright with back against pad",
                    "Grip handles at chest level",
                    "Push handles forward until arms extend",
                    "Keep elbows slightly bent at extension",
                    "Slowly return to starting position"
                ]
            },
            "Shoulder Press": {
                "joints": "Shoulders, Elbows",
                "steps": [
                    "Sit with back straight against pad",
                    "Adjust seat so handles at shoulder height",
                    "Grip handles with palms facing forward",
                    "Press upward in controlled motion",
                    "Extend arms fully without locking elbows"
                ]
            },
            "Lat Pulldown": {
                "joints": "Shoulders, Elbows",
                "steps": [
                    "Sit with thighs under knee pads",
                    "Grip bar wider than shoulder width",
                    "Lean back slightly (about 30 degrees)",
                    "Pull bar down to upper chest level",
                    "Squeeze shoulder blades together"
                ]
            },
            "Seated Row": {
                "joints": "Shoulders, Elbows",
                "steps": [
                    "Sit with feet braced against platform",
                    "Grip handles with neutral grip",
                    "Keep back straight, chest up",
                    "Pull handles toward torso",
                    "Squeeze shoulder blades together"
                ]
            },
            "Leg Press": {
                "joints": "Hips, Knees",
                "steps": [
                    "Sit with back firmly against seat",
                    "Place feet shoulder-width apart",
                    "Release safety handles or latches",
                    "Press through heels to extend legs",
                    "Do not lock knees at full extension"
                ]
            },
            "Leg Extension": {
                "joints": "Hips, Knees",
                "steps": [
                    "Sit with back against padded seat",
                    "Position ankles behind roller pads",
                    "Extend legs fully against resistance",
                    "Squeeze quadriceps at full extension",
                    "Lower weight slowly with control"
                ]
            },
            "Leg Curl": {
                "joints": "Hips, Knees",
                "steps": [
                    "Lie face down on the machine",
                    "Position heels under roller pads",
                    "Curl legs upward toward glutes",
                    "Squeeze hamstrings at peak",
                    "Lower weight slowly with control"
                ]
            },
            "Biceps Curl": {
                "joints": "Elbows, Wrists",
                "steps": [
                    "Sit with chest against the pad",
                    "Grip handles with underhand grip",
                    "Position elbows on the pad",
                    "Curl handles upward toward shoulders",
                    "Squeeze biceps at peak contraction"
                ]
            },
            "Triceps Pushdown": {
                "joints": "Elbows, Wrists",
                "steps": [
                    "Stand facing the cable machine",
                    "Grip bar with palms facing down",
                    "Keep elbows close to sides",
                    "Push bar down until arms extend",
                    "Squeeze triceps at bottom position"
                ]
            },
            "Pec Deck": {
                "joints": "Shoulders, Elbows",
                "steps": [
                    "Sit with back against pad",
                    "Place forearms on pads",
                    "Adjust height for elbow alignment",
                    "Bring arms together in front",
                    "Squeeze chest muscles at peak"
                ]
            },
            "Ab Crunch Machine": {
                "joints": "Hips, Shoulders",
                "steps": [
                    "Sit with back against pad",
                    "Position chest under pads",
                    "Place hands on handles",
                    "Crunch forward using abs",
                    "Exhale during contraction"
                ]
            },
            "Back Extension": {
                "joints": "Hips, Shoulders",
                "steps": [
                    "Position hips against pad",
                    "Place heels under roller",
                    "Cross arms over chest",
                    "Lower torso toward floor",
                    "Extend back to neutral position"
                ]
            }
        }
        
        default_config = {
            "joints": "Multiple Joints",
            "steps": [
                "Adjust machine to fit your body",
                "Maintain proper posture throughout",
                "Perform controlled movements",
                "Use appropriate weight",
                "Complete full range of motion"
            ]
        }
        
        return configs.get(exercise_name, default_config)
    
    def start_monitoring(self):
        """Navigate to camera page"""
        if self.current_exercise:
            self.controller.start_camera()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Procedure Page - Back Button Above Image")
    root.state('zoomed')
    
    class TestController:
        def show_frame(self, frame_name):
            print(f"Would show: {frame_name}")
        def start_camera(self):
            print("Would start camera")
    
    app = ProcedurePage(root, TestController())
    app.pack(fill="both", expand=True)
    app.set_exercise("Lat Pulldown")
    
    root.mainloop()