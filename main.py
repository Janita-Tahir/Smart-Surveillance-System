import cv2
import config
from video_handler import VideoStreamHandler
from detector import SmartDetector
from evaluation import PerformanceEvaluator
from ui import SmartSurveillanceUI

def run_system():
    print("====================================================")
    print("   AI-Based Real-Time Smart Surveillance System")
    print("====================================================")
    
    # Instantiate architectural components from separate modules
    stream_manager = VideoStreamHandler()
    ai_engine = SmartDetector()
    metrics_worker = PerformanceEvaluator()
    gui_layer = SmartSurveillanceUI()

    # Establish camera connections
    if not stream_manager.start_stream():
        return

    gui_layer.setup_window()
    print("\n[KEYBOARD HOTKEYS ACTIVE]:")
    print(" -> Press 'Q' inside screen window to Exit safely.")
    print(" -> Press 'S' inside screen window to Save Live Screenshot.")
    print("====================================================\n")

    # Master Execution Application Loop
    while True:
        # Step 1: Query camera hardware for fresh pixel telemetry
        success, frame = stream_manager.get_frame()
        if not success:
            print("[WARN] Frame drop detected. Stream ending or searching...")
            break

        # Step 2: Pass frame down the AI inference processing funnel
        detections, object_counts = ai_engine.process_frame(frame)

        # Step 3: Run evaluations and crunch frame metrics
        live_fps = metrics_worker.calculate_fps()
        is_crowded, alert_message = metrics_worker.check_crowd_alert(object_counts)

        # Step 4: Construct user dashboard visualization
        gui_layer.draw_dashboard(
            frame=frame,
            detections=detections,
            class_counts=object_counts,
            fps=live_fps,
            alert_status=is_crowded,
            alert_msg=alert_message
        )

        # Step 5: Process active user hardware inputs
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q') or key == ord('Q'):
            print("[INFO] Shutdown command intercepted.")
            break
        elif key == ord('s') or key == ord('S'):
            gui_layer.capture_screenshot(frame)

    # Teardown pipelines gracefully to prevent memory leaks and OS locks
    stream_manager.release_stream()
    gui_layer.close_window()
    print("[SUCCESS] Application runtime terminated cleanly. Goodbye.")

if __name__ == "__main__":
    run_system()