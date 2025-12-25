"""
Exercise Procedure Page
Displays equipment-specific instructions
"""
import tkinter as tk
import random
import config

class ProcedurePage(tk.Frame):
    """Page showing exercise procedure before starting camera"""
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg=config.COLORS["secondary"])
        self.selected_equipment = None
        self.procedure_steps = []
        
        self.create_ui()
    
    def create_ui(self):
        """Create user interface elements"""
        # Header
        self.create_header()
        
        # Content area
        content_frame = tk.Frame(self, bg=config.COLORS["secondary"])
        content_frame.pack(fill="both", expand=True, padx=40, pady=20)
        
        # Left side - Equipment image placeholder
        self.image_frame = tk.Frame(
            content_frame,
            bg=config.COLORS["primary"],
            width=400,
            height=400,
            relief="solid",
            borderwidth=2
        )
        self.image_frame.pack(side="left", fill="both", expand=True, padx=(0, 20))
        self.image_frame.pack_propagate(False)
        
        # Image placeholder label
        self.image_label = tk.Label(
            self.image_frame,
            text="Equipment Image\nWill Appear Here",
            font=config.FONTS["subheading"],
            bg=config.COLORS["primary"],
            fg=config.COLORS["text_secondary"]
        )
        self.image_label.pack(expand=True)
        
        # Right side - Procedure steps
        procedure_frame = tk.Frame(content_frame, bg=config.COLORS["secondary"])
        procedure_frame.pack(side="right", fill="both", expand=True)
        
        # Title
        self.equipment_title = tk.Label(
            procedure_frame,
            text="",
            font=config.FONTS["heading"],
            bg=config.COLORS["secondary"],
            fg=config.COLORS["text"],
            wraplength=400
        )
        self.equipment_title.pack(anchor="w", pady=(0, 30))
        
        # Procedure steps container
        steps_container = tk.Frame(procedure_frame, bg=config.COLORS["secondary"])
        steps_container.pack(fill="both", expand=True)
        
        # Step 1
        self.step1_frame = tk.Frame(
            steps_container,
            bg=config.COLORS["primary"],
            relief="raised",
            borderwidth=1
        )
        self.step1_frame.pack(fill="x", pady=(0, 20))
        
        step1_label = tk.Label(
            self.step1_frame,
            text="Step 1:",
            font=config.FONTS["button"],
            bg=config.COLORS["primary"],
            fg=config.COLORS["accent"],
            anchor="w"
        )
        step1_label.pack(side="left", padx=10, pady=10)
        
        self.step1_text = tk.Label(
            self.step1_frame,
            text="",
            font=config.FONTS["body"],
            bg=config.COLORS["primary"],
            fg=config.COLORS["text"],
            wraplength=350,
            justify="left"
        )
        self.step1_text.pack(side="left", padx=(0, 10), pady=10, fill="x", expand=True)
        
        # Step 2
        self.step2_frame = tk.Frame(
            steps_container,
            bg=config.COLORS["primary"],
            relief="raised",
            borderwidth=1
        )
        self.step2_frame.pack(fill="x")
        
        step2_label = tk.Label(
            self.step2_frame,
            text="Step 2:",
            font=config.FONTS["button"],
            bg=config.COLORS["primary"],
            fg=config.COLORS["accent"],
            anchor="w"
        )
        step2_label.pack(side="left", padx=10, pady=10)
        
        self.step2_text = tk.Label(
            self.step2_frame,
            text="",
            font=config.FONTS["body"],
            bg=config.COLORS["primary"],
            fg=config.COLORS["text"],
            wraplength=350,
            justify="left"
        )
        self.step2_text.pack(side="left", padx=(0, 10), pady=10, fill="x", expand=True)
        
        # Start button at bottom
        button_frame = tk.Frame(self, bg=config.COLORS["secondary"])
        button_frame.pack(side="bottom", pady=30)
        
        self.start_button = tk.Button(
            button_frame,
            text="START EXERCISE",
            font=config.FONTS["button"],
            bg=config.COLORS["accent"],
            fg=config.COLORS["text"],
            padx=40,
            pady=15,
            cursor="hand2",
            command=self.start_exercise
        )
        self.start_button.pack()
    
    def create_header(self):
        """Create page header with back button"""
        header_frame = tk.Frame(self, bg=config.COLORS["primary"], height=60)
        header_frame.pack(fill="x", side="top")
        header_frame.pack_propagate(False)
        
        back_btn = tk.Button(
            header_frame,
            text="← Back",
            font=config.FONTS["button"],
            bg=config.COLORS["primary"],
            fg=config.COLORS["text"],
            bd=0,
            cursor="hand2",
            command=lambda: self.controller.show_frame("EquipmentDashboard")
        )
        back_btn.pack(side="left", padx=20, pady=10)
    
    def set_equipment(self, equipment_name):
        """Set the selected equipment and update UI"""
        self.selected_equipment = equipment_name
        
        # Update title
        self.equipment_title.config(text=f"{equipment_name} - Exercise Procedure")
        
        # Get random procedure steps
        procedures = config.EXERCISE_PROCEDURES.get(
            equipment_name, 
            ["Adjust seat for proper alignment", "Maintain controlled movement throughout"]
        )
        # To:
        # First check if EXERCISE_PROCEDURES exists
        if hasattr(config, 'EXERCISE_PROCEDURES') and equipment_name in config.EXERCISE_PROCEDURES:
            procedures = config.EXERCISE_PROCEDURES[equipment_name]
        else:
            # Fallback procedures
            procedures = [
                f"Step 1: Adjust {equipment_name} for proper alignment",
                f"Step 2: Perform {equipment_name} with controlled movement",
                f"Step 3: Maintain good posture throughout",
                f"Step 4: Breathe properly during exercise"
           ]
        
        if len(procedures) >= 2:
            # Select two random unique steps
            if len(procedures) > 2:
                self.procedure_steps = random.sample(procedures, 2)
            else:
                self.procedure_steps = procedures[:2]
            
            self.step1_text.config(text=self.procedure_steps[0])
            self.step2_text.config(text=self.procedure_steps[1])
        
        # Update image placeholder (in production, load actual image)
        self.image_label.config(text=f"{equipment_name}\nImage Preview")
    
    def start_exercise(self):
        """Navigate to camera page to start exercise monitoring"""
        if self.selected_equipment:
            camera_page = self.controller.get_frame("CameraPage")
            if camera_page:
                camera_page.set_equipment(self.selected_equipment)
                self.controller.show_frame("CameraPage")