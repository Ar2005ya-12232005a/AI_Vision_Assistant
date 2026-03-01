import cv2
import random
import time

from camera import Camera
from yolo_detector import YoloDetector
from decision_engine import DecisionEngine
from voice_alert import VoiceAlert

cam = Camera()
detector = YoloDetector()
engine = DecisionEngine()
voice = VoiceAlert()

last_spoken_time = 0
cooldown = 3  # seconds

while True:

    frame = cam.get_frame()
    if frame is None:
        break

    detections = detector.detect(frame)

    # 🔥 Simulated distance (replace later with Arduino)
    distance = random.randint(20, 200)

    alert = engine.evaluate(detections, distance, frame)

    if alert and time.time() - last_spoken_time > cooldown:
        voice.speak(alert)
        print(alert)
        last_spoken_time = time.time()

    annotated_frame = detections[0].plot()

    cv2.imshow("AI Vision Assist", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()