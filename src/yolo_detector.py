from ultralytics import YOLO

class YoloDetector:
    def __init__(self, model_path="models/yolov8n.pt"):
        self.model = YOLO(model_path)

    def detect(self, frame):
        results = self.model(frame)
        return results