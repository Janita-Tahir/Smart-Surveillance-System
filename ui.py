import cv2
import os
import time
import config

class SmartSurveillanceUI:
    def __init__(self):
        self.window_name = "AI Smart Campus Surveillance Dashboard"
        # Theme colors (BGR format for OpenCV)
        self.COLOR_PRIMARY = (0, 255, 0)      # Neon Green for normal bounding boxes
        self.COLOR_ALERT = (0, 0, 255)        # Crimson Red for high-risk alerts
        self.COLOR_TEXT = (255, 255, 255)     # Clean White for readable fonts
        self.COLOR_PANEL = (40, 40, 40)       # Dark Charcoal Gray for the HUD banner

    def setup_window(self):
        """Creates an interactive GUI window context."""
        cv2.namedWindow(self.window_name, cv2.WINDOW_AUTOSIZE)

    def draw_dashboard(self, frame, detections, class_counts, fps, alert_status, alert_msg):
        """Renders all bounding boxes, stats banners, and alerts onto the frame."""
        
        # 1. Draw Bounding Boxes and Floating Labels
        for det in detections:
            x1, y1, x2, y2 = det["box"]
            label = det["class_name"]
            conf = det["confidence"]

            # Choose color scheme based on active crowd alert status
            box_color = self.COLOR_ALERT if (label == "Person" and alert_status) else self.COLOR_PRIMARY

            # Render the rectangle borders
            cv2.rectangle(frame, (x1, y1), (x2, y2), box_color, 2)

            # Build readable status string (e.g., "Person: 84%")
            status_text = f"{label}: {int(conf * 100)}%"
            
            # Draw a small text background tag for premium UI contrast
            (text_w, text_h), _ = cv2.getTextSize(status_text, cv2.FONT_HERSHEY_SIMPLEX, 0.45, 1)
            cv2.rectangle(frame, (x1, y1 - 20), (x1 + text_w, y1), box_color, -1)
            cv2.putText(frame, status_text, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.45, self.COLOR_TEXT, 1)

        # 2. Draw Top Telemetry Panel Banner (Dark HUD overlay)
        cv2.rectangle(frame, (0, 0), (config.FRAME_WIDTH, 45), self.COLOR_PANEL, -1)

        # 3. Render System Performance Metrics
        cv2.putText(frame, f"FPS: {fps}", (15, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.55, self.COLOR_PRIMARY, 2)

        # 4. Render Dynamic Object Counts
        count_summary = " | ".join([f"{k}: {v}" for k, v in class_counts.items() if v > 0])
        if not count_summary:
            count_summary = "Scanning Campus Environments..."
        cv2.putText(frame, count_summary, (110, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.45, self.COLOR_TEXT, 1)

        # 5. Render Critical Overcrowding Alarm System
        if alert_status:
            # Draw blinking indicator banner at bottom of screen
            cv2.rectangle(frame, (0, config.FRAME_HEIGHT - 35), (config.FRAME_WIDTH, config.FRAME_HEIGHT), self.COLOR_ALERT, -1)
            cv2.putText(frame, alert_msg, (20, config.FRAME_HEIGHT - 12), cv2.FONT_HERSHEY_SIMPLEX, 0.55, self.COLOR_TEXT, 2)

        # Display final composited frame window to desktop monitor
        cv2.imshow(self.window_name, frame)

    def capture_screenshot(self, frame):
        """Saves current frame state to output drive instantly."""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"capture_{timestamp}.png"
        filepath = os.path.join(config.SCREENSHOT_DIR, filename)
        cv2.imwrite(filepath, frame)
        print(f"[UI ALERT] Snapshot exported securely to: {filepath}")

    def close_window(self):
        """Termitnates interface window pipelines safely."""
        cv2.destroyAllWindows()