class DecisionEngine:

    def evaluate(self, detections, distance, frame):

        danger_objects = [
            "person", "bicycle", "car", "motorcycle", "bus", "truck",
            "dog", "cat", "horse", "cow",
            "chair", "couch", "bed", "dining table",
            "traffic light", "stop sign", "fire hydrant",
            "backpack", "suitcase", "bottle"
        ]

        alerts = []

        for result in detections:
            for box in result.boxes:

                if box.conf[0] < 0.6:
                    continue

                cls_id = int(box.cls[0])
                label = result.names[cls_id]

                x_center = float((box.xyxy[0][0] + box.xyxy[0][2]) / 2)
                frame_width = frame.shape[1]

                if x_center < frame_width / 3:
                    direction = "left"
                elif x_center > 2 * frame_width / 3:
                    direction = "right"
                else:
                    direction = "center"

                # Priority: closer objects alerted first
                if label in danger_objects:
                    if distance < 50:
                        alerts.append((0, f"Warning! {label} very close on {direction} at {distance} cm"))
                    elif distance < 100:
                        alerts.append((1, f"{label} on {direction} at {distance} cm"))

        # Sort by priority (0 = most urgent first)
        alerts.sort(key=lambda x: x[0])

        return alerts[0][1] if alerts else None