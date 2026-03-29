import cv2
import random
import time

from src.camera import Camera
from src.yolo_detector import YoloDetector
from src.decision_engine import DecisionEngine
from src.voice_alert import VoiceAlert

cam = Camera()
detector = YoloDetector()
engine = DecisionEngine()
voice = VoiceAlert()

last_spoken_time = 0
cooldown = 3  # seconds between alerts

while True:

    frame = cam.get_frame()
    if frame is None:
        break

    detections = detector.detect(frame)

    # Simulated single ultrasonic sensor distance (replace with Arduino later)
    distance = random.randint(20, 200)

    alert = engine.evaluate(detections, distance, frame)

    if alert and (time.time() - last_spoken_time > cooldown):
        voice.speak(alert)
        print(f"[ALERT] {alert}")
        last_spoken_time = time.time()

    annotated_frame = detections[0].plot() if detections else frame

    # Show simulated distance on screen
    cv2.putText(
        annotated_frame,
        f"Distance: {distance} cm (simulated)",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        2
    )

    cv2.imshow("AI Vision Assist", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()