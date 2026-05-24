import cv2
import config

class VideoStreamHandler:
    def __init__(self, source=None):
        # Fallback to config default source if no specific source path is provided
        self.source = source if source is not None else config.VIDEO_SOURCE
        self.cap = None
        self.width = config.FRAME_WIDTH
        self.height = config.FRAME_HEIGHT

    def start_stream(self):
        """Initializes and opens the video capture stream hardware."""
        print(f"[INFO] Opening video source connection: {self.source}")
        self.cap = cv2.VideoCapture(self.source)
        
        # Apply custom hardware frame resolution settings if targeting a webcam
        if isinstance(self.source, int):
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
            
        if not self.cap.isOpened():
            print(f"[ERROR] Critical: Unable to access video source: {self.source}")
            return False
            
        print("[INFO] Video stream successfully established.")
        return True

    def get_frame(self):
        """Grabs a single frame from the stream and handles preprocessing."""
        if self.cap is None or not self.cap.isOpened():
            return False, None

        ret, frame = self.cap.read()
        if not ret:
            return False, None

        # Standardize frame resolution across different camera models
        frame = cv2.resize(frame, (self.width, self.height))
        return True, frame

    def release_stream(self):
        """Safely closes the camera hardware connection to avoid OS resource leaks."""
        if self.cap and self.cap.isOpened():
            self.cap.release()
            print("[INFO] Video capture hardware released safely.")