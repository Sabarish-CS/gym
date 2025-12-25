"""
Equipment Selection Dashboard
Grid layout of hydraulic equipment with clickable cards
"""
import tkinter as tk
from tkinter import ttk
import config
from PIL import Image, ImageTk
import os

class EquipmentDashboard(tk.Frame):
    """Equipment selection interface with grid layout"""
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg=config.COLORS["secondary"])
        
        # Header with back button
        self.create_header()
        
        # Main content area
        self.create_equipment_grid()
        
        # Bind escape key to go back
        self.bind_all('<Escape>', lambda e: self.controller.quit_app())
    
    def create_header(self):
        """Create header with back button"""
        header_frame = tk.Frame(self, bg=config.COLORS["primary"], height=60)
        header_frame.pack(fill="x", side="top")
        header_frame.pack_propagate(False)
        
        # Back button
        back_btn = tk.Button(
            header_frame,
            text="← Back",
            font=config.FONTS["button"],
            bg=config.COLORS["primary"],
            fg=config.COLORS["text"],
            bd=0,
            cursor="hand2",
            command=lambda: self.controller.quit_app()  # Would go to previous screen
        )
        back_btn.pack(side="left", padx=20, pady=10)
        
        # Title
        title_label = tk.Label(
            header_frame,
            text="Select Equipment",
            font=config.FONTS["heading"],
            fg=config.COLORS["text"],
            bg=config.COLORS["primary"]
        )
        title_label.pack(side="left", padx=20, pady=10)
    
    def create_equipment_grid(self):
        """Create scrollable grid of equipment cards"""
        # Main container
        main_container = tk.Frame(self, bg=config.COLORS["secondary"])
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Canvas for scrolling
        canvas = tk.Canvas(main_container, bg=config.COLORS["secondary"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=config.COLORS["secondary"])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Create equipment cards
        self.create_equipment_cards(scrollable_frame)
        
        # Pack scrollable area
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Mouse wheel scrolling
        canvas.bind_all("<MouseWheel>", 
                       lambda event: canvas.yview_scroll(int(-1*(event.delta/120)), "units"))
    
    def create_equipment_cards(self, parent_frame):
        """Create individual equipment cards"""
        # Calculate grid layout (3 columns)
        columns = 3
        for i, equipment in enumerate(config.HYDRAULIC_EQUIPMENT):
            row = i // columns
            col = i % columns
            
            # Equipment card frame
            card_frame = tk.Frame(
                parent_frame,
                bg=config.COLORS["primary"],
                width=250,
                height=200,
                relief="raised",
                borderwidth=2
            )
            card_frame.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
            card_frame.grid_propagate(False)
            card_frame.bind("<Button-1>", 
                           lambda e, eq=equipment: self.select_equipment(eq))
            
            # Card content
            # Icon placeholder (would load actual image in production)
            icon_label = tk.Label(
                card_frame,
                text="🏋️",  # Placeholder emoji - replace with actual icon
                font=("Arial", 48),
                bg=config.COLORS["primary"],
                fg=config.COLORS["accent"]
            )
            icon_label.pack(pady=(20, 10))
            
            # Equipment name
            name_label = tk.Label(
                card_frame,
                text=equipment,
                font=config.FONTS["subheading"],
                bg=config.COLORS["primary"],
                fg=config.COLORS["text"],
                wraplength=200
            )
            name_label.pack(pady=(0, 20))
            
            # Hover effects
            card_frame.bind("<Enter>", lambda e, f=card_frame: self.on_card_hover(e, f))
            card_frame.bind("<Leave>", lambda e, f=card_frame: self.on_card_leave(e, f))
            
            # Make card and all children clickable
            for child in card_frame.winfo_children():
                child.bind("<Button-1>", 
                          lambda e, eq=equipment: self.select_equipment(eq))
    
    def on_card_hover(self, event, frame):
        """Visual feedback on card hover"""
        frame.config(bg=config.COLORS["accent"], relief="sunken")
        for child in frame.winfo_children():
            child.config(bg=config.COLORS["accent"])
    
    def on_card_leave(self, event, frame):
        """Reset card on mouse leave"""
        frame.config(bg=config.COLORS["primary"], relief="raised")
        for child in frame.winfo_children():
            child.config(bg=config.COLORS["primary"])
    
    def select_equipment(self, equipment_name):
        """Handle equipment selection"""
        # Store selected equipment
        self.controller.selected_equipment = equipment_name
        
        # Navigate to procedure page
        procedure_page = self.controller.get_frame("ProcedurePage")
        if procedure_page:
            procedure_page.set_equipment(equipment_name)
            self.controller.show_frame("ProcedurePage")