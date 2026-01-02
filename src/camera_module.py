"""
Camera Module - REAL camera using your working OpenCV!
"""

import cv2
import time
import threading

class RealCamera:
    """Real camera class - uses your working OpenCV!"""
    
    def __init__(self, camera_id=0):
        self.camera_id = camera_id
        self.cap = None
        self.frame = None
        self.is_running = False
        self.thread = None
        self.frame_count = 0
        
    def start(self):
        """Start REAL camera"""
        print(f"📹 Starting REAL camera {self.camera_id}...")
        
        # Open camera
        self.cap = cv2.VideoCapture(self.camera_id)
        
        if not self.cap.isOpened():
            print(f"❌ Camera {self.camera_id} failed. Trying camera 1...")
            self.camera_id = 1
            self.cap = cv2.VideoCapture(1)
            
        if not self.cap.isOpened():
            print("❌ No camera found. Please check:")
            print("   1. Camera is connected")
            print("   2. No other app is using camera (Zoom, Teams, etc.)")
            print("   3. Camera permissions are granted")
            return False
        
        # Set camera properties
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        
        self.is_running = True
        
        # Start thread to capture frames
        self.thread = threading.Thread(target=self._capture_loop)
        self.thread.daemon = True
        self.thread.start()
        
        # Wait for first frame
        time.sleep(1)
        
        print(f"✅ Camera {self.camera_id} started successfully!")
        print("   You should see yourself in the web interface!")
        return True
    
    def _capture_loop(self):
        """Continuously capture frames"""
        while self.is_running:
            ret, frame = self.cap.read()
            if ret:
                self.frame = frame
                self.frame_count += 1
            else:
                print("⚠️ Failed to read frame")
                time.sleep(0.1)
    
    def get_frame(self):
        """Get the latest frame"""
        return self.frame
    
    def get_frame_for_web(self):
        """Get frame as JPEG bytes for web display"""
        if self.frame is None:
            return None
        
        # Resize for web
        frame_resized = cv2.resize(self.frame, (640, 480))
        
        # Convert to JPEG
        ret, buffer = cv2.imencode('.jpg', frame_resized, 
                                   [cv2.IMWRITE_JPEG_QUALITY, 85])
        if ret:
            return buffer.tobytes()
        return None
    
    def stop(self):
        """Stop camera"""
        self.is_running = False
        if self.thread:
            self.thread.join(timeout=2)
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
        print("🛑 Camera stopped")
    
    def get_status(self):
        return {
            'running': self.is_running,
            'camera_id': self.camera_id,
            'frames_captured': self.frame_count,
            'type': 'REAL camera (OpenCV)'
        }

# Test function
def test_camera():
    """Test the camera"""
    print("🧪 Testing Real Camera...")
    cam = RealCamera()
    
    if cam.start():
        print("\n👀 Showing preview for 5 seconds...")
        print("Press 'q' to quit early")
        
        start_time = time.time()
        while time.time() - start_time < 5:
            frame = cam.get_frame()
            if frame is not None:
                # Add text
                cv2.putText(frame, "HELMET DETECTION SYSTEM", 
                           (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                           0.7, (0, 255, 0), 2)
                cv2.putText(frame, "REAL CAMERA WORKING!", 
                           (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 
                           0.7, (0, 255, 255), 2)
                
                # Show
                cv2.imshow('Real Camera Test', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cam.stop()
        cv2.destroyAllWindows()
        print("\n✅ Camera test successful!")

if __name__ == "__main__":
    test_camera()