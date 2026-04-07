import cv2
import time
import random

from src.camera import Camera
from src.yolo_detector import YoloDetector
from src.decision_engine import DecisionEngine
from src.voice_alert import VoiceAlert
from utils.config import (
    SERIAL_PORT, BAUD_RATE, 
    ALERT_COOLDOWN_SEC, MODEL_PATH
)

# Initialize components
cam = Camera()
detector = YoloDetector(MODEL_PATH)
engine = DecisionEngine()
voice = VoiceAlert()

# Try connecting Arduino — fallback to simulation if not connected
try:
    import serial
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)
    print(f"[INFO] Arduino connected on {SERIAL_PORT}")
    arduino_connected = True
except Exception as e:
    print(f"[WARNING] Arduino not connected: {e}")
    print("[INFO] Running with simulated distance")
    ser = None
    arduino_connected = False

last_spoken_time = 0

while True:
    frame = cam.get_frame()
    if frame is None:
        print("[ERROR] Camera frame not received")
        break

    detections = detector.detect(frame)

    # Get distance — real or simulated
    if arduino_connected and ser.is_open:
        try:
            line = ser.readline().decode('utf-8').strip()
            distance = int(line) if line.isdigit() else 200
        except Exception:
            distance = 200
    else:
        distance = random.randint(20, 200)  # simulation

    alert = engine.evaluate(detections, distance, frame)

    if alert and (time.time() - last_spoken_time > ALERT_COOLDOWN_SEC):
        voice.speak(alert)
        print(f"[ALERT] {alert}")
        last_spoken_time = time.time()

    annotated_frame = detections[0].plot() if detections else frame

    # Show status on screen
    source_label = "Arduino" if arduino_connected else "Simulated"
    cv2.putText(
        annotated_frame,
        f"Distance: {distance} cm ({source_label})",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0) if arduino_connected else (0, 165, 255),  # green or orange
        2
    )

    cv2.imshow("AI Vision Assist", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cam.release()
if ser:
    ser.close()
    print("[INFO] Arduino disconnected")