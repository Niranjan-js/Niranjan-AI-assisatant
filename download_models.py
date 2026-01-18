import os
import sys

print("[INFO] Starting Model Downloads...")

try:
    print("[1/2] Checking YOLOv8 (Vision)...")
    from ultralytics import YOLO
    # This triggers the download of yolov8n.pt if not present
    model = YOLO("yolov8n.pt")
    print("[OK] YOLOv8 model ready.")
except ImportError:
    print("[ERROR] Ultralytics not found. Install still running?")
except Exception as e:
    print(f"[ERROR] YOLO Error: {e}")

try:
    print("[2/2] Checking EasyOCR (Docs)...")
    import easyocr
    # This triggers the download of the detection and recognition models
    reader = easyocr.Reader(['en'], gpu=False)
    print("[OK] EasyOCR models ready.")
except ImportError:
    print("[ERROR] EasyOCR not found. Install still running?")
except Exception as e:
    print(f"[ERROR] EasyOCR Error: {e}")

print("[DONE] Model download check complete.")
