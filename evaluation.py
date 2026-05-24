import time
import config

class PerformanceEvaluator:
    def __init__(self):
        self.prev_time = 0
        self.crowd_threshold = config.CROWD_THRESHOLD

    def calculate_fps(self):
        """Calculates actual system processing speed (Frames Per Second)."""
        current_time = time.time()
        
        # Prevent division by zero errors on the first loop initialization
        if self.prev_time == 0:
            self.prev_time = current_time
            return 0.0
            
        time_differential = current_time - self.prev_time
        fps = 1 / time_differential
        self.prev_time = current_time
        return round(fps, 1)

    def check_crowd_alert(self, class_counts):
        """
        Evaluates current class densities.
        Returns True if 'Person' count exceeds safety thresholds.
        """
        person_count = class_counts.get("Person", 0)
        if person_count >= self.crowd_threshold:
            return True, f"ALERT: Suspicious Crowd Detected! ({person_count} People)"
        return False, ""