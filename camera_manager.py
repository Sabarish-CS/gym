"""
Camera Manager
Handles camera initialization, capture, and release
"""
import cv2
import threading
import time

class CameraManager:
    """Manages camera operations in a separate thread"""
    
    def __init__(self, camera_id=0):
        self.camera_id = camera_id
        self.cap = None
        self.frame = None
        self.running = False
        self.lock = threading.Lock()
        self.callback = None
        
    def start(self, callback=None):
        """Start camera capture thread"""
        self.running = True
        self.callback = callback
        self.thread = threading.Thread(target=self._capture_loop, daemon=True)
        self.thread.start()
    
    def _capture_loop(self):
        """Main capture loop running in separate thread"""
        self.cap = cv2.VideoCapture(self.camera_id)
        
        # Optimize for Raspberry Pi
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Reduce latency
        
        while self.running and self.cap.isOpened():
            ret, frame = self.cap.read()
            
            if ret:
                with self.lock:
                    self.frame = frame
                
                # Call callback if provided
                if self.callback:
                    self.callback(frame)
            
            # Small delay to prevent CPU overuse
            time.sleep(0.01)
    
    def get_frame(self):
        """Get the latest frame"""
        with self.lock:
            return self.frame.copy() if self.frame is not None else None
    
    def stop(self):
        """Stop camera and release resources"""
        self.running = False
        
        if self.thread.is_alive():
            self.thread.join(timeout=1)
        
        if self.cap:
            self.cap.release()
        
        with self.lock:
            self.frame = None
    
    def is_opened(self):
        """Check if camera is opened"""
        return self.cap is not None and self.cap.isOpened()