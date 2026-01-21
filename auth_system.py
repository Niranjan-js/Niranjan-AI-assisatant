import cv2
import face_recognition
import os
import sys

OWNER_IMAGE_PATH = "owner.jpg"

def capture_owner():
    """Captures a frame from the camera and saves it as the owner's reference image."""
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        print("Error: Could not open camera.")
        return False
        
    print("Look at the camera for 3 seconds...")
    cv2.waitKey(3000)
    
    ret, frame = cam.read()
    if ret:
        cv2.imwrite(OWNER_IMAGE_PATH, frame)
        print(f"Owner image saved to {OWNER_IMAGE_PATH}")
    else:
        print("Error: Could not capture image.")
        
    cam.release()
    cv2.destroyAllWindows()
    return ret

def authenticate_owner(timeout_seconds=10):
    """
    Captures frames persistently for a timeout period to authenticate.
    Returns True if owner is detected within the window.
    """
    if not os.path.exists(OWNER_IMAGE_PATH):
        print("Error: Owner image not found.")
        return False

    import numpy as np
    from PIL import Image
    import time
    
    try:
        # Load reference
        img = Image.open(OWNER_IMAGE_PATH).convert('RGB')
        known_encodings = face_recognition.face_encodings(np.array(img))
        if not known_encodings: return False
        known_encoding = known_encodings[0]
        
        cam = cv2.VideoCapture(0)
        if not cam.isOpened(): return False
        
        print(f"🔒 Authenticating (Timeout: {timeout_seconds}s)...")
        start_time = time.time()
        
        while (time.time() - start_time) < timeout_seconds:
            ret, frame = cam.read()
            if not ret: continue
            
            # Show authentication in progress
            cv2.putText(frame, "NIRANJAN_SEC_AUTH: SEARCHING...", (20, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
            cv2.imshow("Niranjan Security Login", frame)
            cv2.waitKey(1)
            
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            unknown_encodings = face_recognition.face_encodings(rgb_frame)
            
            for unknown_encoding in unknown_encodings:
                results = face_recognition.compare_faces([known_encoding], unknown_encoding, tolerance=0.5)
                if results[0]:
                    print("✅ Access Granted!")
                    cv2.putText(frame, "MATCH DETECTED: WELCOME SIR", (20, 50), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                    cv2.imshow("Niranjan Security Login", frame)
                    cv2.waitKey(1000)
                    cam.release()
                    cv2.destroyAllWindows()
                    return True
        
        print("❌ Access Denied: Timeout reached.")
        cam.release()
        cv2.destroyAllWindows()
        return False
            
    except Exception as e:
        print(f"Authentication error: {e}")
        return False

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Niranjan AI Authentication System")
    parser.add_argument("--capture", action="store_true", help="Capture owner face")
    parser.add_argument("--verify", action="store_true", help="Verify owner face")
    
    args = parser.parse_args()
    
    if args.capture:
        capture_owner()
    elif args.verify:
        if authenticate_owner():
            sys.exit(0)
        else:
            sys.exit(1)
    else:
        parser.print_help()
