import config
from model_loader import load_yolo_model

class SmartDetector:
    def __init__(self):
        # Load our trained neural network using our loader utility
        self.model = load_yolo_model()
        
        # Pull configurations from our central config file
        self.target_classes = config.TARGET_CLASSES
        self.conf_threshold = config.DEFAULT_CONF_THRESHOLD
        self.iou_threshold = config.IOU_THRESHOLD

    def process_frame(self, frame):
        """
        Runs YOLOv8 inference on a single video frame.
        Filters and structures data cleanly for the UI layer.
        """
        if self.model is None:
            print("[ERROR] Model engine not initialized.")
            return [], {}

        # Run inference using PyTorch backend. 
        # verbose=False keeps the terminal clean from standard logging outputs.
        results = self.model(
            frame, 
            conf=self.conf_threshold, 
            iou=self.iou_threshold, 
            verbose=False
        )[0]

        parsed_detections = []
        class_counts = {}

        # Extract predicted boxes, confidence values, and class IDs from tensors
        boxes = results.boxes.xyxy.cpu().numpy()     # Bounding box coordinates [x1, y1, x2, y2]
        scores = results.boxes.conf.cpu().numpy()    # Model confidence levels (0.0 to 1.0)
        class_ids = results.boxes.cls.cpu().numpy()  # Numeric index mapping to COCO class

        for box, score, class_id in zip(boxes, scores, class_ids):
            class_id = int(class_id)
            
            # Filter: Only care about objects critical to our Smart Campus requirements
            if class_id in self.target_classes:
                class_name = self.target_classes[class_id]
                x1, y1, x2, y2 = map(int, box)  # Convert coordinates to integers for OpenCV

                # Structure data into a consistent data contract for Member 2/UI files
                detection_data = {
                    "box": (x1, y1, x2, y2),
                    "class_name": class_name,
                    "confidence": float(score)
                }
                parsed_detections.append(detection_data)

                # Keep track of individual object metrics for counting requirements
                class_counts[class_name] = class_counts.get(class_name, 0) + 1

        return parsed_detections, class_counts

if __name__ == "__main__":
    # Small isolated backend verification test
    import numpy as np
    print("[INFO] Testing detector module compilation...")
    detector = SmartDetector()
    
    # Generate a dummy blank image array to simulate a camera frame
    dummy_frame = np.zeros((480, 640, 3), dtype=np.uint8)
    detections, counts = detector.process_frame(dummy_frame)
    print(f"[SUCCESS] Module compiled. Dummy run output -> Detections: {len(detections)}, Counts: {counts}")