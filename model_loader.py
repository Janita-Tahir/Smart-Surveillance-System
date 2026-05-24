import os
from ultralytics import YOLO
import config

def load_yolo_model():
    """
    Loads the YOLOv8 model weights. 
    If the weights are not found in the local models/ directory, 
    YOLO will automatically download them from the official server.
    """
    print("[INFO] Initializing AI Engine...")
    
    # Ensure the models directory exists
    if not os.path.exists(config.MODEL_DIR):
        os.makedirs(config.MODEL_DIR)
        print(f"[INFO] Created missing directory: {config.MODEL_DIR}")
        
    try:
        # Initialize YOLOv8 model with configured path (e.g., 'models/yolov8n.pt')
        print(f"[INFO] Loading model weights from: {config.MODEL_PATH}")
        model = YOLO(config.MODEL_PATH)
        print("[INFO] YOLOv8 AI Model loaded successfully.")
        return model
        
    except Exception as e:
        print(f"[ERROR] Failed to load YOLOv8 model: {e}")
        return None

if __name__ == "__main__":
    # Test execution block to ensure model loads/downloads correctly independently
    test_model = load_yolo_model()
    if test_model:
        print("[SUCCESS] model_loader.py is functioning perfectly!")