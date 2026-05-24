import os

# --- Model Configurations ---
# yolov8n.pt (Nano) is highly optimized for fast inference on standard CPUs
MODEL_NAME = "yolov8n.pt"  
MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, MODEL_NAME)

# --- Inference Thresholds ---
DEFAULT_CONF_THRESHOLD = 0.40  # Filter out detections below 40% confidence
IOU_THRESHOLD = 0.45           # For overlapping bounding box filtering

# --- Video / Camera Settings ---
# 0 targets your built-in/USB webcam. You can later change this to a video file path string.
VIDEO_SOURCE = 0  
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

# --- Analytics & Crowd Tracking ---
CROWD_THRESHOLD = 5  # Alert trigger if more than 5 people are counted together

# --- Output Paths ---
SCREENSHOT_DIR = os.path.join("outputs", "screenshots")
VIDEO_OUTPUT_DIR = os.path.join("outputs", "videos")

# --- Specific Campus Target Classes (COCO Dataset IDs) ---
TARGET_CLASSES = {
    0: "Person",
    2: "Car",
    3: "Motorcycle",
    5: "Bus",
    11: "Stop Sign",
    13: "Bench",
    24: "Backpack",
    26: "Handbag",
    39: "Bottle",
    56: "Chair",
    60: "Dining Table",
    63: "Laptop",
    67: "Cell Phone"
}