"""
MAIN HELMET DETECTION SYSTEM APP
Complete system with REAL camera and AI!
"""

import sys
import os

# Fix Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Now import modules
try:
    from camera_module import RealCamera
    from detection_module import AIDetector
    from control_module import VehicleControl
    print("✅ All modules imported successfully!")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Current directory:", current_dir)
    print("Files in directory:", os.listdir(current_dir))
    sys.exit(1)


from flask import Flask, render_template, Response, jsonify, request
import cv2
import threading
import time
import numpy as np
from src.camera_module import RealCamera
from src.detection_module import AIDetector
from src.control_module import VehicleControl

app = Flask(__name__)

# Global system components
camera = RealCamera()
detector = AIDetector()
controller = VehicleControl()
system_active = False
detection_thread = None

# Current status
current_status = {
    'helmet_detected': False,
    'confidence': 0.0,
    'ignition_allowed': False,
    'message': 'System ready. Click START.',
    'timestamp': '',
    'camera_frames': 0
}

@app.route('/')
def index():
    """Main dashboard"""
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    """Live video stream"""
    def generate():
        while system_active:
            frame_bytes = camera.get_frame_for_web()
            if frame_bytes:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + 
                       frame_bytes + b'\r\n')
            else:
                # Send placeholder
                placeholder = np.zeros((480, 640, 3), dtype=np.uint8)
                cv2.putText(placeholder, "NO CAMERA FEED", 
                           (150, 240), cv2.FONT_HERSHEY_SIMPLEX, 
                           1, (255, 255, 255), 2)
                ret, buffer = cv2.imencode('.jpg', placeholder)
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + 
                       buffer.tobytes() + b'\r\n')
            time.sleep(0.03)  # ~30 FPS
    
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/api/status')
def get_status():
    """Get current system status"""
    camera_status = camera.get_status()
    detector_status = detector.get_status()
    control_status = controller.get_status()
    
    status = {
        'system_active': system_active,
        'camera': camera_status,
        'detector': detector_status,
        'controller': control_status,
        'current': current_status,
        'timestamp': time.strftime("%H:%M:%S")
    }
    
    return jsonify(status)

@app.route('/api/start', methods=['POST'])
def start_system():
    """Start the helmet detection system"""
    global system_active, detection_thread
    
    try:
        # Start camera
        if not camera.start():
            return jsonify({
                'success': False,
                'error': 'Failed to start camera'
            })
        
        system_active = True
        
        # Start detection thread
        detection_thread = threading.Thread(target=detection_loop)
        detection_thread.daemon = True
        detection_thread.start()
        
        return jsonify({
            'success': True,
            'message': 'Helmet Detection System started!',
            'camera': 'Active',
            'ai': 'Ready',
            'control': 'Active'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/stop', methods=['POST'])
def stop_system():
    """Stop the system"""
    global system_active
    
    system_active = False
    camera.stop()
    
    return jsonify({
        'success': True,
        'message': 'System stopped'
    })

@app.route('/api/toggle_override', methods=['POST'])
def toggle_override():
    """Toggle safety override"""
    override, message = controller.toggle_override()
    return jsonify({
        'override': override,
        'message': message
    })

@app.route('/api/logs')
def get_logs():
    """Get recent logs"""
    logs = controller.get_logs(20)
    return jsonify({
        'logs': logs,
        'count': len(logs)
    })

def detection_loop():
    """Main detection loop"""
    global current_status
    
    while system_active:
        try:
            # Get frame from camera
            frame = camera.get_frame()
            
            if frame is not None:
                # Run AI detection
                helmet_detected, confidence, timestamp = detector.detect(frame)
                
                # Control vehicle
                ignition_allowed, message = controller.check_and_control(
                    helmet_detected, confidence
                )
                
                # Update current status
                current_status = {
                    'helmet_detected': helmet_detected,
                    'confidence': float(confidence),
                    'ignition_allowed': ignition_allowed,
                    'message': message,
                    'timestamp': timestamp,
                    'camera_frames': camera.frame_count
                }
                
                # Draw on frame for display
                draw_detection_on_frame(frame, helmet_detected, confidence, message)
            
            time.sleep(0.5)  # Run detection twice per second
            
        except Exception as e:
            print(f"Detection error: {e}")
            time.sleep(1)

def draw_detection_on_frame(frame, helmet_detected, confidence, message):
    """Draw detection results on frame"""
    if frame is None:
        return
    
    # Add status text
    status_color = (0, 255, 0) if helmet_detected else (0, 0, 255)
    status_text = "HELMET: YES" if helmet_detected else "HELMET: NO"
    
    cv2.putText(frame, status_text, (20, 40),
               cv2.FONT_HERSHEY_SIMPLEX, 1, status_color, 2)
    
    cv2.putText(frame, f"Confidence: {confidence:.0%}", (20, 80),
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, status_color, 2)
    
    cv2.putText(frame, message[:40], (20, 120),
               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
    
    cv2.putText(frame, time.strftime("%H:%M:%S"), (20, 460),
               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    # Draw a box around detection area
    height, width = frame.shape[:2]
    cv2.rectangle(frame, (width//4, height//4), 
                 (3*width//4, 3*height//4), status_color, 2)

if __name__ == '__main__':
    print("=" * 70)
    print("🚀 HELMET DETECTION SYSTEM - COMPLETE VERSION")
    print("=" * 70)
    print("Features:")
    print("  ✅ REAL camera with OpenCV")
    print("  ✅ AI detection with YOLOv8 (ultralytics)")
    print("  ✅ Vehicle control logic")
    print("  ✅ Web dashboard with live video")
    print("  ✅ Detection logging")
    print("\n📡 Starting server...")
    print("🌐 Open your browser and go to: http://localhost:5000")
    print("=" * 70)
    
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)