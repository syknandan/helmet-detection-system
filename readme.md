# 🛡️ Helmet Detection System

A real-time computer vision system for detecting helmet usage using YOLOv8 and Flask.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.3%2B-lightgrey)
![OpenCV](https://img.shields.io/badge/OpenCV-4.8%2B-green)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-red)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Development Journey](#development-journey)
- [Troubleshooting](#troubleshooting)
- [Future Improvements](#future-improvements)
- [License](#license)

## 🎯 Overview

This system detects whether individuals are wearing helmets in real-time using YOLOv8 object detection. Designed for safety monitoring at construction sites, industrial facilities, and for motorcycle riders. The system provides a web-based interface for live monitoring and logs all detection events.

## ✨ Features

- **Real-time Detection**: Processes video streams with 30+ FPS
- **Web Interface**: User-friendly dashboard built with Flask
- **Multi-source Input**: Works with webcam, IP cameras, and video files
- **Violation Logging**: Automatically logs detection events with timestamps
- **Modular Architecture**: Easily extensible code structure
- **Low Hardware Requirements**: Runs on CPU (GPU optional for better performance)

## 📁 Project Structure

```
helmet-detection-system/
├── src/                          # Source code
│   ├── app_fixed.py             # Main Flask application
│   ├── detection_module.py      # YOLOv8 detection logic
│   ├── camera_module.py         # Video stream handling
│   ├── control_module.py        # System controls
│   ├── utils.py                 # Utility functions
│   ├── yolov8n.pt              # YOLO model (gitignored)
│   └── detection_logs.csv       # Detection records
├── static/                      # Web assets
│   ├── css/
│   │   └── styles.css          # Styling
│   └── js/
│       └── script.js           # Frontend logic
├── templates/                   # HTML templates
│   └── html/
│       └── index.html          # Main dashboard
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git exclusion rules
└── README.md                   # This file
```

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher(python 10.x.x suggested)
- pip package manager
- Webcam or video source

### Step 1: Clone Repository
```bash
git clone https://github.com/yourusername/helmet-detection-system.git
cd helmet-detection-system
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

If you don't have `requirements.txt`, install manually:
```bash
pip install flask opencv-python ultralytics pandas numpy pillow
```

### Step 3: Download YOLO Model
The model file is excluded from Git due to size. You need to download it separately:

**Option A: Automatic download (recommended)**
```bash
python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"
```

**Option B: Manual download**
1. Download `yolov8n.pt` from [Ultralytics YOLOv8 Releases](https://github.com/ultralytics/ultralytics)
2. Place it in the `src/` folder

## 💻 Usage

### Starting the Application
```bash
cd src
python app_fixed.py
```

### Accessing the Web Interface
1. Open your browser
2. Navigate to: `http://localhost:5000`
3. You should see the helmet detection dashboard

### Using the System
1. Click **"Start Detection"** to begin video analysis
2. View real-time helmet detection results
3. Detection logs are saved to `detection_logs.csv`
4. Click **"Stop Detection"** to pause the system

## 🔧 How It Works

### Detection Pipeline
```
Video Input → Frame Capture → YOLOv8 Processing → Helmet Detection → Results Display
      ↓              ↓              ↓                  ↓               ↓
   Camera      OpenCV Capture   Neural Network    Bounding Boxes   Web Interface
```

### Key Components
1. **YOLOv8 Model**: Pre-trained object detector fine-tuned for helmet detection
2. **Flask Server**: Handles web requests and serves the interface
3. **OpenCV**: Manages video capture and frame processing
4. **Frontend**: Real-time updates using JavaScript and CSS

## 📖 Development Journey

### Challenges Overcome
1. **Git Configuration**: Learned to set up `user.name` and `user.email` for commits
2. **Large File Management**: Discovered that model files (.pt) should be gitignored
3. **Environment Issues**: Resolved dependency conflicts between system Python and virtual environments
4. **Performance Optimization**: Fixed slow commits by excluding binary files

### Key Learnings
- Git is for source code, not large binary files
- Always use `.gitignore` for model files, logs, and dependencies
- Virtual environments prevent dependency conflicts
- Modular code structure makes debugging easier

## 🐛 Troubleshooting

### Common Issues

**Issue:** `ModuleNotFoundError: No module named 'flask'`  
**Solution:** Install dependencies with `pip install -r requirements.txt`

**Issue:** Slow Git commits (minutes instead of seconds)  
**Solution:** Check if you're trying to commit large files; update `.gitignore`

**Issue:** Webcam not detected  
**Solution:** Check camera index in `camera_module.py` (try 0, 1, or 2)

**Issue:** Low detection accuracy  
**Solution:** Try different YOLO model (yolov8s.pt, yolov8m.pt for better accuracy)

### Debugging Commands
```bash
# Check Python version
python --version

# Verify installed packages
pip list

# Test camera access
python -c "import cv2; cap = cv2.VideoCapture(0); print('Camera working' if cap.isOpened() else 'Check camera')"
```

## 🔮 Future Improvements

### Planned Features
- [ ] **Multi-class Detection**: Add detection for safety vests, gloves, goggles
- [ ] **Alert System**: Email/SMS notifications for violations
- [ ] **Database Integration**: Replace CSV with SQL database
- [ ] **Multi-camera Support**: Monitor multiple locations simultaneously
- [ ] **Mobile App**: Companion app for remote monitoring
- [ ] **Cloud Deployment**: Deploy as web service with GPU acceleration
- [ ] **Custom Training**: Fine-tune model on specific helmet types

### Technical Improvements
- [ ] Add unit tests and CI/CD pipeline
- [ ] Implement logging system
- [ ] Add configuration file for easy settings adjustment
- [ ] Create Docker container for easy deployment
- [ ] Optimize for edge devices (Raspberry Pi, Jetson Nano)

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Contribution Guidelines
- Follow PEP 8 Python style guide
- Add comments for complex logic
- Update documentation when adding features
- Test changes before submitting PR

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Ultralytics](https://ultralytics.com/) for YOLOv8
- [OpenCV](https://opencv.org/) for computer vision tools
- [Flask](https://flask.palletsprojects.com/) for web framework
- Contributors and testers who helped improve the system

## 📞 Support

For questions, issues, or suggestions:
1. Check the [Issues](https://github.com/syknandan/helmet-detection-system/issues) page
2. Create a new issue with detailed description
3. Email: syknandan@gmail.com

---

**⭐ If you find this project useful, please give it a star!**

*Last Updated: [03-01-2025] 
*Version: 1.0.0*
