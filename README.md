# 🦯 AI Vision Assist
### Smart Obstacle Detection System for Visually Impaired People

![Python](https://img.shields.io/badge/Python-3.8+-blue) ![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-orange) ![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green) ![Arduino](https://img.shields.io/badge/Arduino-HC--SR04-teal)

---

## 📌 Overview

**AI Vision Assist** is a real-time obstacle detection system built to assist visually impaired individuals. It uses a laptop camera combined with a YOLOv8 deep learning model to detect dangerous objects in the environment, determines their direction (left / center / right), and alerts the user through voice output.

In the current phase, distance is **simulated** via random values. In the hardware phase, an **HC-SR04 ultrasonic sensor** connected via **Arduino** will provide real distance measurements.

---

## 🎯 Features

- 🎥 Real-time object detection using **YOLOv8n** (80 COCO classes)
- 📐 Direction detection — **Left / Center / Right** using bounding box analysis
- 📏 Distance measurement — simulated now, Arduino ultrasonic sensor later
- 🔊 Voice alerts using **pyttsx3** (offline text-to-speech)
- ⚡ Non-blocking speech using **Python threading**
- 🛑 Two-level danger system — Normal alert (< 100 cm) and Warning alert (< 50 cm)
- ⏱️ 3-second cooldown to prevent alert spam
- 🖥️ Live annotated video feed with distance overlay

---

## 🗂️ Project Structure

```
AI-Vision-Assist/
│
├── models/
│   └── yolov8n.pt              ← Pretrained YOLOv8 model (COCO)
│
├── src/
│   ├── camera.py               ← Captures live video frames
│   ├── yolo_detector.py        ← Runs YOLO object detection
│   ├── decision_engine.py      ← Determines danger, direction, alert level
│   ├── voice_alert.py          ← Speaks alerts via TTS (threaded)
│   └── main.py                 ← Entry point — ties all modules together
│
├── arduino/
│   └── obstacle_sensor.ino     ← Arduino ultrasonic + buzzer code (Phase 2)
│
├── utils/
│   └── config.py               ← (Reserved for future config settings)
│
├── requirements.txt
└── README.md
```

---

## ⚙️ How It Works

```
Camera captures frame
        ↓
YOLOv8 detects objects in frame
        ↓
For each detected object:
  ├── Confidence check  (skip if < 60%)
  ├── Get label         (person / car / chair ...)
  └── Calculate direction from bounding box center
              ↓
        Distance check:
          < 50 cm  → "Warning! {label} very close on {direction}"
          < 100 cm → "{label} on {direction} at {distance} cm"
              ↓
        Voice speaks alert (background thread)
              ↓
        Frame displayed with bounding boxes + distance overlay
              ↓
        Loop repeats
```

---

## 📁 Module Breakdown

### `camera.py`
Opens the laptop camera using OpenCV and captures frames one by one. Returns `None` if the camera fails.

### `yolo_detector.py`
Loads the pretrained `yolov8n.pt` model and runs detection on each frame. Returns bounding boxes, class labels, and confidence scores. Uses `verbose=False` to suppress terminal logs.

### `decision_engine.py`
The brain of the system. For every detected object:
- Skips detections below **60% confidence**
- Calculates bounding box center to determine **direction**
- Checks distance against **two thresholds** (50 cm and 100 cm)
- Collects all alerts and returns the **most urgent one first**

**Direction zones:**
```
|---- LEFT ----|---- CENTER ----|---- RIGHT ----|
0            w/3              2w/3              w
```

**Danger objects list (20 classes):**
```
person, bicycle, car, motorcycle, bus, truck,
dog, cat, horse, cow,
chair, couch, bed, dining table,
traffic light, stop sign, fire hydrant,
backpack, suitcase, bottle
```

### `voice_alert.py`
Uses `pyttsx3` for offline text-to-speech. Runs speech in a **background thread** with a **lock** to prevent overlapping alerts and camera freezing.

### `main.py`
Entry point. Initializes all modules, runs the detection loop, handles cooldown logic, overlays distance on the video frame, and displays the live feed.

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/AI-Vision-Assist.git
cd AI-Vision-Assist
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Download YOLOv8 Model
Place `yolov8n.pt` inside the `models/` folder.
Download from: https://github.com/ultralytics/assets/releases

### 5. Run the Project
```bash
python src/main.py
```

Press **Q** to quit the live feed.

---

## 📦 Requirements

```
ultralytics
opencv-python
pyttsx3
pyserial
```

Install with:
```bash
pip install ultralytics opencv-python pyttsx3 pyserial
```

---

## 🔌 Hardware Phase (Coming Next)

Currently distance is simulated:
```python
# Current (simulated)
distance = random.randint(20, 200)
```

After connecting Arduino with HC-SR04, replace with:
```python
# Phase 2 (real hardware)
distance = distance_sensor.get_distance()
```

**Only this one line changes. Everything else stays the same.**

### Hardware Setup
| Component | Purpose |
|-----------|---------|
| Arduino Uno | Microcontroller |
| HC-SR04 | Ultrasonic distance sensor |
| Buzzer | Physical audio alert |
| USB Cable | Serial communication with laptop |

### Arduino Workflow
1. Upload `arduino/obstacle_sensor.ino` via Arduino IDE
2. Close Serial Monitor (important — Python needs the port)
3. Note the COM port (e.g., `COM4` on Windows, `/dev/ttyUSB0` on Linux)
4. Update port in `distance_reader.py`
5. Run `main.py` as usual

---

## 🧠 Alert Examples

```
"Warning! person very close on center at 35 cm"    ← distance < 50 cm
"car on left at 80 cm"                             ← distance < 100 cm
"dog on right at 65 cm"                            ← distance < 100 cm
```

---

## 📊 Tech Stack

| Layer | Technology |
|-------|-----------|
| Object Detection | YOLOv8n (Ultralytics) |
| Computer Vision | OpenCV |
| Voice Output | pyttsx3 |
| Hardware Communication | PySerial + Arduino |
| Distance Sensing | HC-SR04 Ultrasonic |
| Language | Python 3.8+ |

---

## 🛠️ Future Improvements

- [ ] Connect Arduino HC-SR04 for real distance measurement
- [ ] Add object tracking with DeepSORT
- [ ] Add monocular depth estimation
- [ ] Port to Raspberry Pi for wearable version
- [ ] Add emergency SMS alert
- [ ] Build mobile app interface

---

## 👤 Author

**Arya**
B.Tech Student | AI & Computer Vision Enthusiast

---

## 📄 License

This project is for educational purposes.