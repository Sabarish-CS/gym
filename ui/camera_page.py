"""
Camera and Angle Detection Page - FULL SCREEN WITH VISUAL FEEDBACK
Live webcam feed with posture monitoring and angle visualization
"""
# =========== IMPORTS ===========
import tkinter as tk
from tkinter import ttk
import cv2
import numpy as np
import mediapipe as mp
import threading
import time
import sys
import os
import config
from PIL import Image, ImageTk

# =========== FIXED IMPORTS ===========
# Add project root to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)  # Goes up from ui/ to project root
sys.path.insert(0, parent_dir)

# Try to import exercise functions, with fallback
try:
    from exercises.exercise_config import get_exercise_config, validate_angle
    HAS_EXERCISE_CONFIG = True
except ImportError:
    HAS_EXERCISE_CONFIG = False
    
    # Fallback functions
    def get_exercise_config(exercise_name):
        # Default configuration for Chest Press
        default_config = {
            "Chest Press": {
                "description": "Push handles forward while seated",
                "joints_to_track": ["shoulder", "elbow", "wrist"],
                "landmarks": {"left": [11, 13, 15], "right": [12, 14, 16]},
                "primary_side": "both",
                "target_angle_range": (160, 175),
                "tolerance": 5,
                "direction": "forward",
                "feedback_messages": {
                    "correct": "Perfect! Maintain this angle",
                    "too_small": "Elbow angle too small - don't lock elbows",
                    "too_large": "Elbow angle too large - extend more"
                }
            }
        }
        return default_config.get(exercise_name, default_config["Chest Press"])
    
    def validate_angle(exercise_name, angle):
        config = get_exercise_config(exercise_name)
        min_angle, max_angle = config["target_angle_range"]
        
        if min_angle <= angle <= max_angle:
            return True, config["feedback_messages"]["correct"]
        elif angle < min_angle:
            return False, config["feedback_messages"]["too_small"]
        else:
            return False, config["feedback_messages"]["too_large"]
# =========== END FIX ===========

class CameraPage(tk.Frame):
    """Full screen camera feed with angle detection and visual feedback"""
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        # Make this frame expand to fill parent
        self.configure(bg=config.COLORS["dark"])
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Camera and MediaPipe setup
        self.cap = None
        
        # Initialize MediaPipe with compatibility
        self.initialize_mediapipe()
        
        self.running = False
        
        # Angle tracking
        self.current_angle = 0
        self.angle_history = []
        self.posture_correct = False
        self.posture_feedback = ""
        self.blink_state = False
        self.blink_interval = 300  # Faster blinking for better feedback
        self.last_blink_time = 0
        
        # Selected equipment
        self.selected_equipment = None
        self.angle_config = None
        
        # UI setup - FULL SCREEN
        self.create_fullscreen_ui()
        
        # Start camera thread
        self.start_camera()
    
    def initialize_mediapipe(self):
        """Initialize MediaPipe with version compatibility"""
        try:
            # Check MediaPipe version
            mp_version = getattr(mp, '__version__', 'unknown')
            print(f"MediaPipe version: {mp_version}")
            
            # Different initialization for different versions
            if hasattr(mp, 'solutions'):
                self.mp_pose = mp.solutions.pose
                self.mp_drawing = mp.solutions.drawing_utils
                
                # Try different initialization methods
                try:
                    # Method 1: With all parameters (newest versions)
                    self.pose = self.mp_pose.Pose(
                        static_image_mode=False,
                        model_complexity=1,
                        smooth_landmarks=True,
                        min_detection_confidence=0.5,
                        min_tracking_confidence=0.5
                    )
                    print("✓ MediaPipe Pose initialized with parameters")
                except TypeError as e1:
                    try:
                        # Method 2: With fewer parameters
                        self.pose = self.mp_pose.Pose(
                            min_detection_confidence=0.5,
                            min_tracking_confidence=0.5
                        )
                        print("✓ MediaPipe Pose initialized with basic parameters")
                    except TypeError as e2:
                        try:
                            # Method 3: Without any parameters (oldest versions)
                            self.pose = self.mp_pose.Pose()
                            print("✓ MediaPipe Pose initialized without parameters")
                        except Exception as e3:
                            print(f"✗ All Pose initializations failed: {e3}")
                            self.create_mock_pose()
                    except Exception as e:
                        print(f"✗ Pose initialization error: {e}")
                        self.create_mock_pose()
            else:
                print("✗ mp.solutions not found")
                self.create_mock_pose()
                
        except ImportError as e:
            print(f"✗ MediaPipe not installed: {e}")
            self.create_mock_pose()
    
    def create_mock_pose(self):
        """Create mock pose detection for when MediaPipe fails"""
        print("Creating mock pose detector...")
        
        class MockPose:
            def __init__(self, **kwargs):
                pass
            def process(self, image):
                class Result:
                    pose_landmarks = None
                return Result()
            def close(self):
                pass
        
        class MockDrawingUtils:
            @staticmethod
            def draw_landmarks(image, landmarks, connections, **kwargs):
                # Draw mock landmarks for testing
                height, width = image.shape[:2]
                cv2.putText(image, "MOCK POSE DETECTION", (50, 50), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                cv2.putText(image, "Install mediapipe for real detection", (50, 100), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        
        # Create mock modules
        self.mp_pose = type('pose', (), {
            'Pose': MockPose,
            'POSE_CONNECTIONS': []
        })()
        self.mp_drawing = MockDrawingUtils()
        self.pose = self.mp_pose.Pose()
    
    def create_fullscreen_ui(self):
        """Create full screen camera interface with large angle display"""
        # Main container that fills entire screen
        main_container = tk.Frame(self, bg=config.COLORS["dark"])
        main_container.grid(row=0, column=0, sticky="nsew")
        main_container.grid_rowconfigure(1, weight=1)
        main_container.grid_columnconfigure(0, weight=1)
        
        # =========== HEADER ===========
        header_frame = tk.Frame(main_container, bg=config.COLORS["primary"], height=70)
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 5))
        header_frame.grid_propagate(False)
        
        # Back button (left)
        back_btn = tk.Button(
            header_frame,
            text="← BACK TO PROCEDURE",
            font=("Arial", 16, "bold"),
            bg=config.COLORS["primary"],
            fg=config.COLORS["text"],
            bd=0,
            cursor="hand2",
            padx=20,
            pady=10,
            command=self.stop_and_go_back
        )
        back_btn.pack(side="left", padx=20)
        
        # Equipment title (center)
        self.equipment_label = tk.Label(
            header_frame,
            text="LIVE POSTURE MONITORING",
            font=("Arial", 24, "bold"),
            bg=config.COLORS["primary"],
            fg=config.COLORS["accent"]
        )
        self.equipment_label.pack(side="left", expand=True)
        
        # =========== MAIN CONTENT ===========
        content_frame = tk.Frame(main_container, bg=config.COLORS["dark"])
        content_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        content_frame.grid_rowconfigure(0, weight=1)
        content_frame.grid_columnconfigure(0, weight=3)  # Camera gets 3/4 width
        content_frame.grid_columnconfigure(1, weight=1)  # Info gets 1/4 width
        
        # =========== LEFT PANEL: CAMERA FEED ===========
        left_panel = tk.Frame(content_frame, bg=config.COLORS["dark"])
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        left_panel.grid_rowconfigure(0, weight=1)
        left_panel.grid_columnconfigure(0, weight=1)
        
        # Camera feed with thick blinking border
        self.camera_border = tk.Frame(
            left_panel,
            bg=config.COLORS["accent"],  # Start with green
            padx=10,  # Thicker border
            pady=10
        )
        self.camera_border.grid(row=0, column=0, sticky="nsew")
        self.camera_border.grid_rowconfigure(0, weight=1)
        self.camera_border.grid_columnconfigure(0, weight=1)
        
        self.camera_label = tk.Label(
            self.camera_border,
            text="INITIALIZING CAMERA...\n\nPlease wait...",
            font=("Arial", 18),
            bg=config.COLORS["dark"],
            fg=config.COLORS["text"],
            relief="solid",
            borderwidth=2
        )
        self.camera_label.grid(row=0, column=0, sticky="nsew")
        
        # =========== RIGHT PANEL: ANGLE & INFO ===========
        right_panel = tk.Frame(content_frame, bg=config.COLORS["secondary"])
        right_panel.grid(row=0, column=1, sticky="nsew")
        right_panel.grid_rowconfigure(0, weight=1)
        right_panel.grid_columnconfigure(0, weight=1)
        
        # Create a canvas for scrollable content
        canvas = tk.Canvas(right_panel, bg=config.COLORS["secondary"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(right_panel, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=config.COLORS["secondary"])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=350)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # =========== ANGLE DISPLAY ===========
        angle_container = tk.Frame(
            scrollable_frame,
            bg=config.COLORS["primary"],
            relief="raised",
            borderwidth=3,
            padx=30,
            pady=30
        )
        angle_container.pack(fill="x", pady=(0, 15))
        
        angle_title = tk.Label(
            angle_container,
            text="CURRENT ANGLE",
            font=("Arial", 20, "bold"),
            bg=config.COLORS["primary"],
            fg=config.COLORS["text_secondary"]
        )
        angle_title.pack(pady=(0, 10))
        
        # Large angle display that changes color
        self.angle_value = tk.Label(
            angle_container,
            text="--°",
            font=("Arial", 72, "bold"),
            bg=config.COLORS["primary"],
            fg=config.COLORS["accent"]
        )
        self.angle_value.pack()
        
        # Angle status
        self.angle_status = tk.Label(
            angle_container,
            text="No angle detected",
            font=("Arial", 16),
            bg=config.COLORS["primary"],
            fg=config.COLORS["text_secondary"]
        )
        self.angle_status.pack(pady=(10, 0))
        
        # =========== TARGET RANGE ===========
        range_container = tk.Frame(
            scrollable_frame,
            bg=config.COLORS["primary"],
            relief="raised",
            borderwidth=2,
            padx=20,
            pady=20
        )
        range_container.pack(fill="x", pady=(0, 15))
        
        range_title = tk.Label(
            range_container,
            text="TARGET RANGE",
            font=("Arial", 18, "bold"),
            bg=config.COLORS["primary"],
            fg=config.COLORS["text_secondary"]
        )
        range_title.pack()
        
        self.range_value = tk.Label(
            range_container,
            text="160° - 175°",
            font=("Arial", 32, "bold"),
            bg=config.COLORS["primary"],
            fg=config.COLORS["text"]
        )
        self.range_value.pack()
        
        # =========== POSTURE STATUS ===========
        status_container = tk.Frame(
            scrollable_frame,
            bg=config.COLORS["primary"],
            relief="raised",
            borderwidth=2,
            padx=20,
            pady=20
        )
        status_container.pack(fill="x", pady=(0, 15))
        
        status_title = tk.Label(
            status_container,
            text="POSTURE STATUS",
            font=("Arial", 18, "bold"),
            bg=config.COLORS["primary"],
            fg=config.COLORS["text_secondary"]
        )
        status_title.pack()
        
        self.status_indicator = tk.Label(
            status_container,
            text="WAITING FOR DETECTION",
            font=("Arial", 24, "bold"),
            bg=config.COLORS["dark"],
            fg=config.COLORS["text_secondary"],
            padx=30,
            pady=15
        )
        self.status_indicator.pack()
        
        # =========== REAL-TIME FEEDBACK ===========
        feedback_container = tk.Frame(
            scrollable_frame,
            bg=config.COLORS["primary"],
            relief="raised",
            borderwidth=2,
            padx=20,
            pady=20
        )
        feedback_container.pack(fill="x")
        
        feedback_title = tk.Label(
            feedback_container,
            text="REAL-TIME FEEDBACK",
            font=("Arial", 18, "bold"),
            bg=config.COLORS["primary"],
            fg=config.COLORS["text_secondary"]
        )
        feedback_title.pack(pady=(0, 10))
        
        self.feedback_text = tk.Text(
            feedback_container,
            font=("Arial", 14),
            bg=config.COLORS["primary"],
            fg=config.COLORS["text"],
            wrap="word",
            height=6,
            width=30,
            relief="flat",
            borderwidth=0,
            padx=10,
            pady=10
        )
        self.feedback_text.pack(fill="both", expand=True)
        self.feedback_text.insert("1.0", "Stand in front of the camera and perform the exercise.\n\nAngle feedback will appear here.")
        self.feedback_text.config(state="disabled")  # Make it read-only
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mouse wheel for scrolling
        canvas.bind_all("<MouseWheel>", 
                       lambda event: canvas.yview_scroll(int(-1*(event.delta/120)), "units"))
    
    def set_equipment(self, equipment_name):
        """Set the equipment for angle detection"""
        self.selected_equipment = equipment_name
        self.angle_config = get_exercise_config(equipment_name)
        
        # Update UI
        self.equipment_label.config(text=f"{equipment_name.upper()} - LIVE MONITORING")
        
        if self.angle_config:
            min_angle, max_angle = self.angle_config["target_angle_range"]
            self.range_value.config(text=f"{min_angle}° - {max_angle}°")
            
            # Update feedback text
            self.feedback_text.config(state="normal")
            self.feedback_text.delete("1.0", "end")
            self.feedback_text.insert("1.0", 
                f"Exercise: {equipment_name}\n"
                f"Target Angle: {min_angle}° - {max_angle}°\n\n"
                f"Perform the exercise in front of the camera.\n"
                f"Keep your elbow angle within the target range.\n\n"
                f"Green border = Correct posture\n"
                f"Red blinking border = Needs adjustment"
            )
            self.feedback_text.config(state="disabled")
    
    def start_camera(self):
        """Initialize and start camera capture"""
        self.running = True
        
        # Start camera thread
        self.camera_thread = threading.Thread(target=self.update_camera, daemon=True)
        self.camera_thread.start()
        
        # Start border blinking in main thread using after()
        self.update_border_animation()
    
    def update_camera(self):
        """Thread function to update camera feed"""
        self.cap = cv2.VideoCapture(0)
        
        # Set higher resolution for better quality
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        
        while self.running and self.cap.isOpened():
            ret, frame = self.cap.read()
            
            if ret:
                # Process frame
                processed_frame, angle = self.process_frame(frame)
                
                # Update angle display
                if angle is not None:
                    self.current_angle = angle
                    self.after(0, self.update_angle_display, angle)
                
                # Convert to PhotoImage
                rgb_image = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
                
                # Resize for display
                height, width = rgb_image.shape[:2]
                max_size = (800, 600)
                if width > max_size[0] or height > max_size[1]:
                    scale = min(max_size[0]/width, max_size[1]/height)
                    new_width = int(width * scale)
                    new_height = int(height * scale)
                    rgb_image = cv2.resize(rgb_image, (new_width, new_height))
                
                pil_image = Image.fromarray(rgb_image)
                imgtk = ImageTk.PhotoImage(image=pil_image)
                
                # Update camera label
                self.after(0, self.update_camera_label, imgtk)
            
            time.sleep(0.03)
        
        # Release camera
        if self.cap:
            self.cap.release()
    
    def process_frame(self, frame):
        """Process frame with MediaPipe"""
        frame = cv2.flip(frame, 1)  # Mirror effect
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(rgb_frame)
        
        if results.pose_landmarks:
            # Draw landmarks
            self.mp_drawing.draw_landmarks(
                frame, 
                results.pose_landmarks, 
                self.mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp.solutions.drawing_utils.DrawingSpec(
                    color=(0, 255, 0), thickness=3, circle_radius=4
                ),
                connection_drawing_spec=mp.solutions.drawing_utils.DrawingSpec(
                    color=(255, 255, 255), thickness=2
                )
            )
            
            if self.selected_equipment and results.pose_landmarks.landmark:
                angle = self.calculate_angle(results.pose_landmarks.landmark)
                
                if angle is not None:
                    # Validate angle
                    is_valid, feedback = validate_angle(self.selected_equipment, angle)
                    self.posture_correct = is_valid
                    self.posture_feedback = feedback
                    
                    # Draw on frame with larger text
                    color = (0, 255, 0) if is_valid else (0, 0, 255)
                    
                    # Add background for better text visibility
                    cv2.rectangle(frame, (40, 30), (350, 120), (0, 0, 0), -1)
                    
                    cv2.putText(frame, f"ANGLE: {angle:.1f}°", (50, 70), 
                               cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)
                    
                    status = "CORRECT" if is_valid else "NEEDS ADJUSTMENT"
                    cv2.putText(frame, f"STATUS: {status}", (50, 110), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
                    
                    return frame, angle
        
        # If no pose detected
        cv2.rectangle(frame, (40, 30), (600, 80), (0, 0, 0), -1)
        cv2.putText(frame, "ADJUST POSITION - ENSURE FULL BODY IS VISIBLE", (50, 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        return frame, None
    
    def calculate_angle(self, landmarks):
        """Calculate angle between three points"""
        if not self.angle_config:
            return None
        
        try:
            # Use left side by default
            indices = self.angle_config["landmarks"]["left"]
            idx_a, idx_b, idx_c = indices
            
            # Get coordinates
            a = landmarks[idx_a]
            b = landmarks[idx_b]
            c = landmarks[idx_c]
            
            # Skip if landmark visibility is low
            if hasattr(a, 'visibility') and a.visibility < 0.5:
                return None
            if hasattr(b, 'visibility') and b.visibility < 0.5:
                return None
            if hasattr(c, 'visibility') and c.visibility < 0.5:
                return None
            
            # Calculate angle
            ba = np.array([a.x - b.x, a.y - b.y])
            bc = np.array([c.x - b.x, c.y - b.y])
            
            cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
            cosine_angle = np.clip(cosine_angle, -1.0, 1.0)
            angle = np.degrees(np.arccos(cosine_angle))
            
            # Smooth angle
            self.angle_history.append(angle)
            if len(self.angle_history) > 5:
                self.angle_history.pop(0)
            
            return np.mean(self.angle_history)
            
        except Exception:
            return None
    
    def update_camera_label(self, image):
        """Update camera label"""
        self.camera_label.config(image=image)
        self.camera_label.image = image  # Keep reference
    
    def update_angle_display(self, angle):
        """Update angle display with color coding"""
        self.angle_value.config(text=f"{angle:.0f}°")
        
        if self.posture_correct:
            # Green for correct angle
            self.angle_value.config(fg=config.COLORS["accent"])
            self.angle_status.config(
                text="✓ WITHIN TARGET RANGE",
                fg=config.COLORS["accent"]
            )
            self.status_indicator.config(
                text="CORRECT POSTURE",
                bg=config.COLORS["accent"],
                fg=config.COLORS["text"]
            )
        else:
            # Red for incorrect angle
            self.angle_value.config(fg=config.COLORS["danger"])
            self.angle_status.config(
                text="✗ OUTSIDE TARGET RANGE",
                fg=config.COLORS["danger"]
            )
            self.status_indicator.config(
                text="NEEDS ADJUSTMENT",
                bg=config.COLORS["danger"],
                fg=config.COLORS["text"]
            )
        
        # Update feedback text
        self.feedback_text.config(state="normal")
        self.feedback_text.delete("1.0", "end")
        self.feedback_text.insert("1.0", 
            f"Current Angle: {angle:.1f}°\n\n"
            f"{self.posture_feedback}\n\n"
            f"Target Range: {self.angle_config['target_angle_range'][0]}° - {self.angle_config['target_angle_range'][1]}°"
        )
        self.feedback_text.config(state="disabled")
    
    def update_border_animation(self):
        """Update border color with blinking effect (runs in main thread)"""
        if not self.running:
            return
        
        current_time = time.time()
        
        if self.posture_correct:
            # Solid green for correct posture
            self.camera_border.config(bg=config.COLORS["accent"])
            self.blink_state = False
        else:
            # Blinking red for incorrect posture
            if current_time - self.last_blink_time > self.blink_interval / 1000:
                if self.blink_state:
                    self.camera_border.config(bg=config.COLORS["danger"])
                else:
                    self.camera_border.config(bg=config.COLORS["dark"])
                self.blink_state = not self.blink_state
                self.last_blink_time = current_time
        
        # Schedule next update
        self.after(50, self.update_border_animation)
    
    def stop_and_go_back(self):
        """Stop camera and go back"""
        self.stop_camera()
        self.controller.show_frame("ProcedurePage")
    
    def stop_camera(self):
        """Stop camera"""
        self.running = False
        if self.cap:
            self.cap.release()
        if hasattr(self, 'pose') and self.pose:
            self.pose.close()

# For testing
if __name__ == "__main__":
    root = tk.Tk()
    root.title("FitPose Camera Test")
    root.geometry("1400x800")
    app = CameraPage(root, None)
    app.pack(fill="both", expand=True)
    root.mainloop()