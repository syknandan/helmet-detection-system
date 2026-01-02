"""
FIXED VERSION - Helmet Detection System
"""

import sys
import os
# Add these 2 lines at the TOP (around line 1-10)
import io
from flask import send_file

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("🚀 STARTING HELMET DETECTION SYSTEM")
print("=" * 60)

# Import modules
try:
    from camera_module import RealCamera
    from detection_module import AIDetector
    from control_module import VehicleControl
    print("✅ Modules imported successfully!")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("\n📁 Files in current directory:")
    for f in os.listdir('.'):
        print(f"   {f}")
    sys.exit(1)

# Import Flask and other packages
from flask import Flask, render_template, Response, jsonify, request
import cv2
import threading
import time
import numpy as np

# Create Flask app
app = Flask(__name__)

# Create system components
camera = RealCamera()
detector = AIDetector()
controller = VehicleControl()
system_active = False

print("\n🎯 System Components:")
print(f"   Camera: {camera.__class__.__name__}")
print(f"   Detector: {detector.__class__.__name__}")
print(f"   Controller: {controller.__class__.__name__}")

@app.route('/')
def home():
    """Main dashboard with camera"""
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Helmet Detection System</title>
        <style>
            body { 
                font-family: Arial, sans-serif; 
                padding: 20px;
                background: #f0f2f5;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            h1 {
                color: #333;
                text-align: center;
                margin-bottom: 30px;
            }
            .camera-box {
                background: #000;
                border-radius: 10px;
                padding: 10px;
                margin-bottom: 20px;
                text-align: center;
            }
            .camera-box img {
                max-width: 100%;
                border-radius: 5px;
            }
            .controls {
                display: flex;
                gap: 10px;
                flex-wrap: wrap;
                margin-bottom: 20px;
                justify-content: center;
            }
            .btn {
                padding: 12px 24px;
                border: none;
                border-radius: 5px;
                font-size: 16px;
                cursor: pointer;
                font-weight: bold;
            }
            .btn-start { background: #4CAF50; color: white; }
            .btn-detect { background: #2196F3; color: white; }
            .btn-override { background: #FF9800; color: white; }
            .btn-refresh { background: #9C27B0; color: white; }
            
            .result-box {
                padding: 20px;
                margin-top: 20px;
                border-radius: 5px;
                font-size: 18px;
                font-weight: bold;
                text-align: center;
            }
            .result-good { background: #d4edda; color: #155724; border: 2px solid #4CAF50; }
            .result-bad { background: #f8d7da; color: #721c24; border: 2px solid #f44336; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎯 Helmet Detection System</h1>
            
            <!-- Camera Feed -->
            <div class="camera-box">
                <h3>📹 Live Camera Feed</h3>
                <img id="cameraImage" src="/camera_feed" alt="Camera Feed" width="640" height="480">
            </div>
            
            <!-- Controls -->
            <div class="controls">
                <button class="btn btn-start" onclick="startSystem()">▶ Start System</button>
                <button class="btn btn-detect" onclick="runDetection()">🔍 Run Detection</button>
                <button class="btn btn-override" onclick="toggleOverride()">🔓 Toggle Override</button>
                <button class="btn btn-refresh" onclick="refreshCamera()">🔄 Refresh Camera</button>
            </div>
            
            <!-- Results -->
            <div id="result" class="result-box">
                Click "Run Detection" to see results
            </div>
            
            <!-- Status -->
            <div style="text-align: center; margin-top: 20px; color: #666;">
                <p>🔄 Camera auto-refreshes every 3 seconds</p>
            </div>
        </div>
        
        <script>
            // Refresh camera image
            function refreshCamera() {
                const img = document.getElementById('cameraImage');
                img.src = '/camera_feed?' + new Date().getTime();
            }
            
            // Auto-refresh every 3 seconds
            setInterval(refreshCamera, 3000);
            
            // Start system
            function startSystem() {
                fetch('/api/start', {method: 'POST'})
                    .then(r => r.json())
                    .then(data => {
                        document.getElementById('result').innerHTML = 
                            `<h3>✅ ${data.message}</h3>`;
                    });
            }
            
            // Run detection
            function runDetection() {
                fetch('/api/detect')
                    .then(r => r.json())
                    .then(data => {
                        const result = document.getElementById('result');
                        if (data.success) {
                            if (data.helmet_detected) {
                                result.innerHTML = `
                                    <h3>✅ HELMET DETECTED</h3>
                                    <p>Confidence: ${(data.confidence * 100).toFixed(1)}%</p>
                                    <p>${data.message}</p>
                                `;
                                result.className = 'result-box result-good';
                            } else {
                                result.innerHTML = `
                                    <h3>❌ NO HELMET</h3>
                                    <p>Confidence: ${(data.confidence * 100).toFixed(1)}%</p>
                                    <p>${data.message}</p>
                                `;
                                result.className = 'result-box result-bad';
                            }
                        } else {
                            result.innerHTML = `<h3>❌ ${data.error}</h3>`;
                        }
                    });
            }
            
            // Toggle override
            function toggleOverride() {
                fetch('/api/toggle_override', {method: 'POST'})
                    .then(r => r.json())
                    .then(data => {
                        alert('Safety override: ' + (data.override ? 'ON' : 'OFF'));
                    });
            }
            
            // Initial camera refresh
            refreshCamera();
        </script>
    </body>
    </html>
    '''

@app.route('/api/start', methods=['POST'])
def start_system():
    global system_active
    try:
        camera.start()
        system_active = True
        return jsonify({
            'success': True,
            'message': 'System started! Camera active.'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/detect')
def detect():
    if not system_active:
        return jsonify({'success': False, 'error': 'Start system first'})
    
    try:
        frame = camera.get_frame()
        helmet_detected, confidence, timestamp = detector.detect(frame)
        ignition_allowed, message = controller.check_and_control(helmet_detected, confidence)
        
        return jsonify({
            'success': True,
            'helmet_detected': helmet_detected,
            'confidence': confidence,
            'ignition_allowed': ignition_allowed,
            'message': message,
            'timestamp': timestamp
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/toggle_override', methods=['POST'])
def toggle_override():
    override, message = controller.toggle_override()
    return jsonify({'override': override, 'message': message})

# ======== ADD THIS CODE RIGHT HERE ========

@app.route('/camera_feed')
def camera_feed():
    """Get camera image"""
    try:
        # Get frame from camera
        frame = camera.get_frame()
        
        if frame is not None:
            # Convert to JPEG
            _, buffer = cv2.imencode('.jpg', frame)
            
            # Return as image
            return send_file(
                io.BytesIO(buffer.tobytes()),
                mimetype='image/jpeg'
            )
    except:
        pass
    
    # If camera fails, return black image
    img = np.zeros((480, 640, 3), dtype=np.uint8)
    cv2.putText(img, "Camera Loading...", (200, 240), 
               cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    _, buffer = cv2.imencode('.jpg', img)
    return send_file(
        io.BytesIO(buffer.tobytes()),
        mimetype='image/jpeg'
    )

if __name__ == '__main__':
    print("\n📡 Starting web server...")
    print("🌐 Open your browser and go to: http://localhost:5000")
    print("=" * 60)
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)