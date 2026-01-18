
import os
from livekit.agents import function_tool

# We delay import to avoid crashing the whole agent if torch/ultralytics has DLL issues
YOLO = None
IMPORT_ERROR = "None"

try:
    from ultralytics import YOLO
    import cv2
except Exception as e:
    YOLO = None
    IMPORT_ERROR = str(e)

@function_tool
def detect_objects_tool(image_path: str):
    """
    Detects objects in an image using YOLOv8 (Ultralytics).
    Returns a list of detected items (e.g., 'Person', 'Laptop').
    """
    if YOLO is None:
        return f"❌ Vision Error: Could not load 'ultralytics/torch'. Error: {IMPORT_ERROR}. Use CPU-only torch for stability."

    if not os.path.exists(image_path):
        return f"❌ Error: Image file not found at {image_path}"

    try:
        model = YOLO("yolov8n.pt") 
        results = model(image_path)
        
        detections = []
        for result in results:
            for box in result.boxes:
                class_id = int(box.cls[0])
                label = model.names[class_id]
                conf = float(box.conf[0])
                if conf > 0.5:
                     detections.append(f"{label} ({int(conf*100)}%)")
        
        if not detections:
            return "Vision Analysis: No specific objects detected with high confidence."
            
        summary = f"👁️ **Niranjan Vision Scan Complete:**\n- " + "\n- ".join(list(set(detections)))
        return summary
            
    except Exception as e:
        return f"Vision processing error: {e}"

@function_tool
async def analyze_screen_content():
    """
    Captures the current screen and uses YOLOv8 to identify all active windows or items.
    Combines screenshot and vision capabilities.
    """
    try:
        from Niranjan_screenshot import screenshot_tool
        # Take a snapshot
        snap_res = await screenshot_tool()
        if "successfully" not in snap_res:
            return f"Vision Error: {snap_res}"
            
        # Extract path from message "Saved as screenshots/..."
        import re
        path_match = re.search(r'screenshots/[^\s]+', snap_res)
        if not path_match:
            return "Vision Error: Could not parse screenshot path."
            
        image_path = path_match.group(0)
        
        # Analyze it
        analysis = detect_objects_tool(image_path)
        return f"🖥️ **Live Screen Analysis:**\n{analysis}\n\n*Reference Image: {image_path}*"
        
    except Exception as e:
        return f"Screen analysis failed: {e}"
