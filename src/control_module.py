"""
Vehicle Control Module
"""

import csv
import time
from datetime import datetime
import os

class VehicleControl:
    """Controls vehicle based on helmet detection"""
    
    def __init__(self):
        self.ignition = False
        self.safety_override = False
        self.log_file = 'detection_logs.csv'
        self.logs = []
        
        # Initialize log file
        self._init_logging()
        
        print("🚗 Vehicle Control initialized")
    
    def _init_logging(self):
        """Create log file if doesn't exist"""
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['timestamp', 'helmet_detected', 
                               'confidence', 'ignition_status', 'override'])
    
    def check_and_control(self, helmet_detected, confidence):
        """Make control decision"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Log detection
        self._log_to_csv(timestamp, helmet_detected, confidence)
        
        # Add to memory logs
        log_entry = f"{timestamp} - Helmet: {'YES' if helmet_detected else 'NO'} ({confidence:.0%})"
        self.logs.append(log_entry)
        
        # Keep only last 20 logs in memory
        if len(self.logs) > 20:
            self.logs = self.logs[-20:]
        
        # Control logic
        if self.safety_override:
            self.ignition = True
            return True, "🚨 SAFETY OVERRIDE: Vehicle allowed"
        
        if helmet_detected and confidence > 0.5:
            self.ignition = True
            return True, f"✅ ALLOWED: Helmet detected ({confidence:.0%} confidence)"
        else:
            self.ignition = False
            if not helmet_detected:
                return False, "❌ BLOCKED: No helmet detected"
            else:
                return False, f"⚠️ BLOCKED: Low confidence ({confidence:.0%})"
    
    def _log_to_csv(self, timestamp, helmet_detected, confidence):
        """Log to CSV file"""
        try:
            with open(self.log_file, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    timestamp,
                    'YES' if helmet_detected else 'NO',
                    f"{confidence:.2f}",
                    'ON' if self.ignition else 'OFF',
                    'YES' if self.safety_override else 'NO'
                ])
        except Exception as e:
            print(f"Logging error: {e}")
    
    def toggle_override(self):
        """Toggle safety override"""
        self.safety_override = not self.safety_override
        status = "ON" if self.safety_override else "OFF"
        return self.safety_override, f"Safety override: {status}"
    
    def get_logs(self, count=10):
        """Get recent logs"""
        return self.logs[-count:] if self.logs else []
    
    def get_status(self):
        return {
            'ignition': self.ignition,
            'override': self.safety_override,
            'log_count': len(self.logs)
        }