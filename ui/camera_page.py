"""
FitPose Camera Page - Real-time Posture Monitoring
WITH STABILIZED ANGLE & PROPER REP COUNTING
"""
import tkinter as tk
from tkinter import ttk
import cv2
import numpy as np
import threading
import time
import config
from PIL import Image, ImageTk

# Try to import MediaPipe with proper error handling
try:
    import mediapipe as mp
    MEDIAPIPE_AVAILABLE = True
    print("✓ MediaPipe successfully imported")
except ImportError as e:
    MEDIAPIPE_AVAILABLE = False
    print(f"✗ MediaPipe not available: {e}")
    print("Please install: pip install mediapipe")

class CameraPage(tk.Frame):
    """Real-time camera feed with exercise monitoring - STABILIZED VERSION"""
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg="#1a1a1a")
        
        # Camera setup
        self.cap = None
        self.running = False
        
        # Exercise tracking
        self.current_exercise = "Chest Press"
        self.exercise_config = self.get_exercise_config("Chest Press")
        
        # Pose detection
        self.pose = None
        self.mp_pose = None
        self.mediapipe_available = MEDIAPIPE_AVAILABLE
        
        # Initialize MediaPipe if available
        if self.mediapipe_available:
            self.initialize_mediapipe()
        else:
            print("⚠ Running in mock mode - MediaPipe not available")
            self.create_mock_pose()
        
        # FIX 1: ANGLE STABILIZATION
        self.angle_buffer = []  # Moving average buffer
        self.angle_buffer_size = 8  # Smoothing window
        self.current_angle = None
        
        # FIX 2: CORRECT POSTURE HOLD TIMER
        self.correct_hold_start = None
        self.correct_hold_time = 0.8  # seconds to hold correct posture
        self.posture_correct = False
        
        # Rep counting
        self.rep_count = 0
        self.rep_state = "down"  # down, up, counting
        self.last_state_change = time.time()
        self.rep_debounce = 0.5  # seconds
        
        # Blinking border
        self.blink_state = False
        self.blink_interval = 500  # ms
        self.last_blink_time = 0
        
        # Mock data for testing
        self.mock_angle = 118  # Start at 118°
        self.mock_increment = 0.5  # Slower change
        
        # UI setup
        self.create_ui()
        
    def initialize_mediapipe(self):
        """Initialize MediaPipe Pose"""
        try:
            if hasattr(mp, 'solutions'):
                self.mp_pose = mp.solutions.pose
                
                try:
                    self.pose = self.mp_pose.Pose(
                        static_image_mode=False,
                        model_complexity=1,
                        smooth_landmarks=True,
                        min_detection_confidence=0.5,
                        min_tracking_confidence=0.5
                    )
                    print("✓ MediaPipe Pose initialized")
                except TypeError:
                    self.pose = self.mp_pose.Pose()
                    print("✓ MediaPipe Pose initialized (old version)")
                
                if hasattr(mp.solutions, 'drawing_utils'):
                    self.mp_drawing = mp.solutions.drawing_utils
                else:
                    self.create_mock_drawing()
            else:
                self.create_mock_pose()
                
        except Exception as e:
            print(f"✗ MediaPipe initialization failed: {e}")
            self.create_mock_pose()
    
    def create_mock_pose(self):
        """Create mock pose detection"""
        class MockPose:
            def __init__(self, **kwargs):
                self.kwargs = kwargs
            
            def process(self, image):
                class Result:
                    def __init__(self):
                        self.pose_landmarks = None
                return Result()
            
            def close(self):
                pass
        
        class MockDrawingUtils:
            @staticmethod
            def draw_landmarks(image, landmarks, connections, **kwargs):
                # Just draw text - NO DARK OVERLAY
                h, w, c = image.shape
                cv2.putText(image, "MOCK MODE", (w-150, 40),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        
        self.mp_pose = type('MockMPPose', (), {'Pose': MockPose})()
        self.mp_drawing = MockDrawingUtils()
        self.pose = self.mp_pose.Pose()
        self.mediapipe_available = False
    
    def create_mock_drawing(self):
        """Create mock drawing utilities"""
        class MockDrawingUtils:
            @staticmethod
            def draw_landmarks(image, landmarks, connections, **kwargs):
                pass
        
        self.mp_drawing = MockDrawingUtils()
    
    def create_ui(self):
        """Create the camera monitoring interface"""
        # Main container
        main_container = tk.Frame(self, bg="#1a1a1a")
        main_container.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Configure grid for 50-50 split
        main_container.grid_columnconfigure(0, weight=1)
        main_container.grid_columnconfigure(1, weight=1)
        main_container.grid_rowconfigure(1, weight=1)
        
        # =========== HEADER ===========
        header_frame = tk.Frame(main_container, bg="#2d2d2d", height=60)
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew")
        header_frame.grid_propagate(False)
        
        # Back button
        back_btn = tk.Button(
            header_frame,
            text="← BACK TO PROCEDURE",
            font=("Arial", 12, "bold"),
            bg="#2d2d2d",
            fg="#ffffff",
            bd=0,
            cursor="hand2",
            padx=20,
            pady=10,
            command=self.stop_and_go_back
        )
        back_btn.pack(side="left", padx=20)
        
        # Exercise title
        self.exercise_title = tk.Label(
            header_frame,
            text="CHEST PRESS – LIVE MONITORING",
            font=("Arial", 18, "bold"),
            bg="#2d2d2d",
            fg="#4CAF50"
        )
        self.exercise_title.pack(side="left", expand=True)
        
        # =========== LEFT PANEL: CAMERA FEED (50%) ===========
        left_panel = tk.Frame(main_container, bg="#000000")
        left_panel.grid(row=1, column=0, sticky="nsew")
        left_panel.grid_rowconfigure(0, weight=1)
        left_panel.grid_columnconfigure(0, weight=1)
        
        # Camera feed with border
        self.camera_border = tk.Frame(
            left_panel,
            bg="#2196F3",
            padx=0,
            pady=0
        )
        self.camera_border.pack(fill="both", expand=True)
        
        self.camera_label = tk.Label(
            self.camera_border,
            text="INITIALIZING CAMERA...",
            font=("Arial", 16),
            bg="#000000",
            fg="white",
            relief="flat"
        )
        self.camera_label.pack(fill="both", expand=True)
        
        # =========== RIGHT PANEL: MONITORING INFO (50%) ===========
        right_panel = tk.Frame(main_container, bg="#1a1a1a")
        right_panel.grid(row=1, column=1, sticky="nsew")
        right_panel.grid_rowconfigure(0, weight=1)
        right_panel.grid_columnconfigure(0, weight=1)
        
        # Canvas for scrolling
        canvas = tk.Canvas(right_panel, bg="#1a1a1a", highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)
        
        scrollable_frame = tk.Frame(canvas, bg="#1a1a1a")
        scrollable_frame.pack(fill="both", expand=True)
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=400)
        
        # =========== MONITORING PANELS ===========
        tk.Frame(scrollable_frame, bg="#1a1a1a", height=10).pack()
        
        # Current Angle Panel
        angle_panel = tk.Frame(
            scrollable_frame,
            bg="#2d2d2d",
            relief="flat",
            padx=30,
            pady=30
        )
        angle_panel.pack(fill="x", pady=(0, 20), padx=20)
        
        self.angle_display = tk.Label(
            angle_panel,
            text="118°",
            font=("Arial", 72, "bold"),
            bg="#2d2d2d",
            fg="#FF9800"
        )
        self.angle_display.pack()
        
        tk.Label(
            angle_panel,
            text="CURRENT ANGLE",
            font=("Arial", 14),
            bg="#2d2d2d",
            fg="#aaaaaa"
        ).pack(pady=(10, 0))
        
        # Target Range Panel
        target_panel = tk.Frame(
            scrollable_frame,
            bg="#2d2d2d",
            relief="flat",
            padx=30,
            pady=20
        )
        target_panel.pack(fill="x", pady=(0, 20), padx=20)
        
        tk.Label(
            target_panel,
            text="TARGET RANGE",
            font=("Arial", 16, "bold"),
            bg="#2d2d2d",
            fg="#ffffff"
        ).pack(anchor="w", pady=(0, 10))
        
        self.target_range_label = tk.Label(
            target_panel,
            text="160° – 175°",
            font=("Arial", 24, "bold"),
            bg="#2d2d2d",
            fg="#4CAF50"
        )
        self.target_range_label.pack(anchor="w")
        
        # Posture Status Panel
        status_panel = tk.Frame(
            scrollable_frame,
            bg="#2d2d2d",
            relief="flat",
            padx=30,
            pady=20
        )
        status_panel.pack(fill="x", pady=(0, 20), padx=20)
        
        tk.Label(
            status_panel,
            text="POSTURE STATUS",
            font=("Arial", 16, "bold"),
            bg="#2d2d2d",
            fg="#ffffff"
        ).pack(anchor="w", pady=(0, 10))
        
        self.status_display = tk.Label(
            status_panel,
            text="Incorrect posture",
            font=("Arial", 18, "bold"),
            bg="#2d2d2d",
            fg="#F44336",
            wraplength=350
        )
        self.status_display.pack(anchor="w")
        
        # Real-time Feedback Panel
        feedback_panel = tk.Frame(
            scrollable_frame,
            bg="#2d2d2d",
            relief="flat",
            padx=30,
            pady=20
        )
        feedback_panel.pack(fill="x", pady=(0, 20), padx=20)
        
        tk.Label(
            feedback_panel,
            text="REAL-TIME FEEDBACK",
            font=("Arial", 16, "bold"),
            bg="#2d2d2d",
            fg="#ffffff"
        ).pack(anchor="w", pady=(0, 10))
        
        self.feedback_text = tk.Text(
            feedback_panel,
            font=("Arial", 12),
            bg="#2d2d2d",
            fg="#ffffff",
            wrap="word",
            height=8,
            width=35,
            relief="flat",
            borderwidth=0
        )
        self.feedback_text.pack(fill="both", expand=True)
        
        self.feedback_text.insert("1.0", 
            "⚠ MOCK MODE\n\n"
            "Status: Incorrect posture\n"
            "Feedback: Adjust elbow angle\n\n"
            "Install MediaPipe for real detection:\n"
            "pip install mediapipe"
        )
        self.feedback_text.config(state="disabled")
        
        # Rep Counter Panel
        rep_panel = tk.Frame(
            scrollable_frame,
            bg="#2d2d2d",
            relief="flat",
            padx=30,
            pady=20
        )
        rep_panel.pack(fill="x", pady=(0, 20), padx=20)
        
        tk.Label(
            rep_panel,
            text="REPETITION COUNT",
            font=("Arial", 16, "bold"),
            bg="#2d2d2d",
            fg="#ffffff"
        ).pack(anchor="w", pady=(0, 10))
        
        self.rep_display = tk.Label(
            rep_panel,
            text="0",
            font=("Arial", 48, "bold"),
            bg="#2d2d2d",
            fg="#4CAF50"
        )
        self.rep_display.pack(anchor="w")
        
        tk.Button(
            rep_panel,
            text="Reset Counter",
            font=("Arial", 12),
            bg="#FF9800",
            fg="white",
            command=self.reset_counter,
            padx=20,
            pady=8
        ).pack(anchor="w", pady=(10, 0))
        
        tk.Frame(scrollable_frame, bg="#1a1a1a", height=20).pack()
    
    def get_exercise_config(self, exercise_name):
        """Get configuration for specific exercise"""
        if exercise_name == "Chest Press":
            return {
                "landmarks": {
                    "left": [11, 13, 15],
                    "right": [12, 14, 16]
                },
                "down_range": (80, 100),
                "up_range": (160, 175)
            }
        return None
    
    def set_exercise(self, exercise_name):
        """Set the exercise configuration"""
        self.current_exercise = exercise_name
        self.exercise_config = self.get_exercise_config(exercise_name)
        self.exercise_title.config(text=f"{exercise_name.upper()} – LIVE MONITORING")
        
        if not self.running:
            self.start_camera()
    
    def start_camera(self):
        """Start camera capture"""
        try:
            self.cap = cv2.VideoCapture(0)
            
            if not self.cap.isOpened():
                raise Exception("Cannot open camera")
            
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            
            self.running = True
            self.camera_thread = threading.Thread(target=self.update_camera, daemon=True)
            self.camera_thread.start()
            self.update_border_animation()
            
            print("✓ Camera started successfully")
            
        except Exception as e:
            print(f"✗ Camera initialization failed: {e}")
            self.show_camera_error(f"Camera Error: {str(e)}")
    
    def show_camera_error(self, message):
        """Display camera error message"""
        self.camera_label.config(
            text=f"❌ CAMERA ERROR\n\n{message}",
            font=("Arial", 14),
            fg="#FF6B6B"
        )
    
    def update_camera(self):
        """Thread function to update camera feed"""
        while self.running and self.cap and self.cap.isOpened():
            try:
                ret, frame = self.cap.read()
                
                if ret:
                    processed_frame = self.process_frame(frame)
                    rgb_image = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
                    
                    # Resize to fit
                    label_width = self.camera_label.winfo_width()
                    label_height = self.camera_label.winfo_height()
                    
                    if label_width > 1 and label_height > 1:
                        rgb_image = cv2.resize(rgb_image, (label_width, label_height))
                    else:
                        rgb_image = cv2.resize(rgb_image, (640, 480))
                    
                    pil_image = Image.fromarray(rgb_image)
                    imgtk = ImageTk.PhotoImage(image=pil_image)
                    
                    self.after(0, self.update_camera_label, imgtk)
                else:
                    self.show_camera_error("Cannot read from camera")
                    break
                
            except Exception as e:
                print(f"✗ Camera frame error: {e}")
                break
            
            time.sleep(0.033)
        
        if self.cap:
            self.cap.release()
            self.cap = None
    
    def process_frame(self, frame):
        """Process frame with exercise-specific joint detection"""
        if frame is None:
            return np.zeros((480, 640, 3), dtype=np.uint8)
        
        frame = cv2.flip(frame, 1)
        h, w, c = frame.shape
        
        # FIX 5: TEXT ONLY - NO BACKGROUND
        cv2.putText(frame, "ADJUST POSITION", (20, 40),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        cv2.putText(frame, "ENSURE UPPER BODY IS VISIBLE", (20, 70),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        cv2.putText(frame, f"Reps: {self.rep_count}", (20, h-30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
        
        if self.pose and self.mediapipe_available:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.pose.process(rgb_frame)
            
            if results.pose_landmarks:
                self.draw_exercise_joints(frame, results.pose_landmarks)
                
                left_angle = self.calculate_angle(results.pose_landmarks.landmark, "left")
                right_angle = self.calculate_angle(results.pose_landmarks.landmark, "right")
                
                if left_angle is not None and right_angle is not None:
                    # FIX 1: ANGLE STABILIZATION WITH MOVING AVERAGE
                    raw_angle = (left_angle + right_angle) / 2
                    self.angle_buffer.append(raw_angle)
                    
                    if len(self.angle_buffer) > self.angle_buffer_size:
                        self.angle_buffer.pop(0)
                    
                    smoothed_angle = sum(self.angle_buffer) / len(self.angle_buffer)
                    self.current_angle = smoothed_angle
                    
                    # Update angle display
                    color = "#4CAF50" if self.posture_correct else "#F44336"
                    self.after(0, lambda a=smoothed_angle, c=color: self.update_angle_display(a, c))
                    
                    # Check posture and reps
                    self.check_posture_and_reps(smoothed_angle)
                    
                    # Draw angle on frame
                    cv2.putText(frame, f"Angle: {smoothed_angle:.0f}°", (20, 100),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
                else:
                    self.after(0, lambda: self.update_angle_display(None, "#FF9800"))
                    self.after(0, lambda: self.update_status("Adjust position", "Ensure joints are visible", "#FF9800"))
            else:
                self.after(0, lambda: self.update_angle_display(None, "#FF9800"))
                self.after(0, lambda: self.update_status("No pose detected", "Stand in frame", "#FF9800"))
        else:
            # Mock mode
            self.mock_angle += self.mock_increment
            if self.mock_angle > 170 or self.mock_angle < 80:
                self.mock_increment = -self.mock_increment
            
            self.current_angle = self.mock_angle
            
            # Apply smoothing to mock data too
            self.angle_buffer.append(self.mock_angle)
            if len(self.angle_buffer) > self.angle_buffer_size:
                self.angle_buffer.pop(0)
            smoothed_mock = sum(self.angle_buffer) / len(self.angle_buffer)
            
            # Check posture with smoothed angle
            self.check_posture_and_reps(smoothed_mock)
            
            # Update displays
            color = "#4CAF50" if self.posture_correct else "#F44336"
            self.after(0, lambda a=smoothed_mock, c=color: self.update_angle_display(a, c))
            
            # FIX 4: NO DARK OVERLAY - just text
            cv2.putText(frame, "MOCK MODE", (w-150, 40),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        
        return frame
    
    def draw_exercise_joints(self, frame, landmarks):
        """Draw only exercise-specific joints"""
        if not self.exercise_config:
            return
        
        h, w, c = frame.shape
        
        # Draw connections first
        connections = [
            (11, 13), (13, 15),  # Left arm
            (12, 14), (14, 16),  # Right arm
        ]
        
        for start_idx, end_idx in connections:
            if (start_idx < len(landmarks.landmark) and 
                end_idx < len(landmarks.landmark)):
                start = landmarks.landmark[start_idx]
                end = landmarks.landmark[end_idx]
                
                start_x = int(start.x * w)
                start_y = int(start.y * h)
                end_x = int(end.x * w)
                end_y = int(end.y * h)
                
                cv2.line(frame, (start_x, start_y), (end_x, end_y), (0, 255, 0), 3)
        
        # Draw joints
        indices = [11, 12, 13, 14, 15, 16]
        for idx in indices:
            if idx < len(landmarks.landmark):
                landmark = landmarks.landmark[idx]
                x = int(landmark.x * w)
                y = int(landmark.y * h)
                
                if idx in [11, 12]:  # Shoulders
                    color = (0, 255, 0)
                    radius = 10
                elif idx in [13, 14]:  # Elbows
                    color = (255, 255, 0)
                    radius = 12
                else:  # Wrists
                    color = (0, 255, 255)
                    radius = 8
                
                cv2.circle(frame, (x, y), radius, color, -1)
                cv2.circle(frame, (x, y), radius + 2, (255, 255, 255), 2)
    
    def calculate_angle(self, landmarks, side):
        """Calculate angle for specific side"""
        if not self.exercise_config:
            return None
        
        try:
            if side == "left":
                indices = self.exercise_config["landmarks"]["left"]
            else:
                indices = self.exercise_config["landmarks"]["right"]
            
            idx_a, idx_b, idx_c = indices
            
            if idx_a >= len(landmarks) or idx_b >= len(landmarks) or idx_c >= len(landmarks):
                return None
            
            a = landmarks[idx_a]
            b = landmarks[idx_b]
            c = landmarks[idx_c]
            
            # Check visibility
            if hasattr(a, 'visibility') and a.visibility < 0.3:
                return None
            if hasattr(b, 'visibility') and b.visibility < 0.3:
                return None
            if hasattr(c, 'visibility') and c.visibility < 0.3:
                return None
            
            # Calculate angle
            ba = np.array([a.x - b.x, a.y - b.y])
            bc = np.array([c.x - b.x, c.y - b.y])
            
            cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
            cosine_angle = np.clip(cosine_angle, -1.0, 1.0)
            angle = np.degrees(np.arccos(cosine_angle))
            
            return 180 - angle
            
        except:
            return None
    
    def check_posture_and_reps(self, angle):
        """Check posture and count repetitions - FIXED VERSION"""
        if not self.exercise_config:
            return
        
        current_time = time.time()
        up_min, up_max = self.exercise_config["up_range"]
        down_min, down_max = self.exercise_config["down_range"]
        
        # Check if angle is in target range
        in_target_range = up_min <= angle <= up_max
        
        # FIX 2: CORRECT POSTURE HOLD TIMER
        if angle is None:
            self.correct_hold_start = None
            self.posture_correct = False
            self.after(0, lambda: self.update_status("Waiting for detection", "Stand in frame", "#FF9800"))
        elif in_target_range:
            # Start or continue hold timer
            if self.correct_hold_start is None:
                self.correct_hold_start = current_time
            
            # Check if held long enough
            if current_time - self.correct_hold_start >= self.correct_hold_time:
                self.posture_correct = True
                self.after(0, lambda: self.update_status("Correct posture", "Good form!", "#4CAF50"))
            else:
                # Still holding, not yet correct
                self.posture_correct = False
                hold_remaining = self.correct_hold_time - (current_time - self.correct_hold_start)
                self.after(0, lambda: self.update_status(f"Hold... {hold_remaining:.1f}s", "Keep position", "#FF9800"))
        else:
            # Not in target range - reset hold timer
            self.correct_hold_start = None
            self.posture_correct = False
            
            if angle < up_min:
                self.after(0, lambda: self.update_status("Incorrect posture", "Push further", "#F44336"))
            else:
                self.after(0, lambda: self.update_status("Incorrect posture", "Don't overextend", "#F44336"))
        
        # FIX 3: REP COUNT ONLY IF GREEN BLINK COMPLETES
        if current_time - self.last_state_change > self.rep_debounce:
            if self.rep_state == "down":
                if self.posture_correct:  # Only if fully correct (held long enough)
                    self.rep_state = "up"
                    self.last_state_change = current_time
                    
            elif self.rep_state == "up":
                if not in_target_range and down_min <= angle <= down_max:
                    # Only count if we were in correct posture and now returned to down position
                    self.rep_count += 1
                    self.after(0, self.update_rep_display)
                    self.rep_state = "down"
                    self.last_state_change = current_time
    
    def update_camera_label(self, image):
        """Update camera label"""
        self.camera_label.config(image=image)
        self.camera_label.image = image
    
    def update_angle_display(self, angle, color="#FF9800"):
        """Update angle display"""
        if angle is None:
            self.angle_display.config(text="No angle", fg="#FF9800")
        else:
            self.angle_display.config(text=f"{angle:.0f}°", fg=color)
    
    def update_rep_display(self):
        """Update rep counter display"""
        self.rep_display.config(text=str(self.rep_count))
    
    def update_status(self, status, feedback, color):
        """Update status and feedback"""
        self.status_display.config(text=status, fg=color)
        
        self.feedback_text.config(state="normal")
        self.feedback_text.delete("1.0", "end")
        
        if not self.mediapipe_available:
            self.feedback_text.insert("1.0", 
                f"⚠ MOCK MODE\n\n"
                f"Status: {status}\n"
                f"Feedback: {feedback}\n\n"
                f"Install MediaPipe for real detection:\n"
                f"pip install mediapipe"
            )
        else:
            self.feedback_text.insert("1.0", 
                f"Exercise: {self.current_exercise}\n"
                f"Target Angle: 160° – 175°\n\n"
                f"Status: {status}\n"
                f"Feedback: {feedback}\n\n"
                f"Reps: {self.rep_count}"
            )
        
        self.feedback_text.config(state="disabled")
    
    def update_border_animation(self):
        """Update border color with blinking effect"""
        if not self.running:
            return
        
        current_time = time.time() * 1000
        
        if self.current_angle is None:
            self.camera_border.config(bg="#2196F3")
        elif self.posture_correct:
            self.camera_border.config(bg="#4CAF50")
            self.blink_state = False
        else:
            if current_time - self.last_blink_time > self.blink_interval:
                if self.blink_state:
                    self.camera_border.config(bg="#F44336")
                else:
                    self.camera_border.config(bg="#000000")
                self.blink_state = not self.blink_state
                self.last_blink_time = current_time
        
        self.after(100, self.update_border_animation)
    
    def reset_counter(self):
        """Reset the repetition counter"""
        self.rep_count = 0
        self.rep_display.config(text="0")
        print("✓ Rep counter reset")
    
    def stop_and_go_back(self):
        """Stop camera and go back"""
        self.stop_camera()
        self.controller.show_frame("ProcedurePage")
    
    def stop_camera(self):
        """Stop camera"""
        self.running = False
        if self.cap:
            self.cap.release()
        if self.pose:
            try:
                self.pose.close()
            except:
                pass