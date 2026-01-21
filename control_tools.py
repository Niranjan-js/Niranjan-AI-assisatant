
import os
import subprocess
import webbrowser
from livekit.agents import function_tool

@function_tool
def system_control_tool(action: str):
    """
    Advanced System Control Procotol for power, network, and hardware.
    Actions: 'shutdown', 'restart', 'open_youtube', 'open_whatsapp', 'toggle_wifi', 'open_camera', 'capture'.
    """
    try:
        if action == "shutdown":
            # Action: Shutdown PC
            os.system("shutdown /s /t 5")
            return "🖥️ Protocol Initiated: System will shutdown in 5 seconds."
            
        elif action == "restart":
            # Action: Restart PC
            os.system("shutdown /r /t 5")
            return "🖥️ Protocol Initiated: System will restart in 5 seconds."
            
        elif action == "open_youtube":
            webbrowser.open("https://www.youtube.com")
            return "📺 YouTube Interface: Online and opened in default browser."

        elif action == "open_whatsapp":
            webbrowser.open("https://web.whatsapp.com")
            return "📱 WhatsApp Interface: Online and opened in default browser."
            
        elif action == "toggle_wifi":
            # Note: This is a restricted action on some systems
            subprocess.run(["netsh", "interface", "set", "interface", "Wi-Fi", "admin=disabled"], shell=True)
            return "📡 Network Protocol: Wi-Fi interface status has been modified."
            
        elif action == "open_camera":
            # Open camera feed for 3 seconds
            try:
                import cv2
                cap = cv2.VideoCapture(0)
                if not cap.isOpened(): return "❌ Error: Camera hardware offline or in use."
                ret, frame = cap.read()
                if ret:
                    cv2.imshow("Niranjan Vision Feed", frame)
                    cv2.waitKey(3000)
                    cv2.destroyAllWindows()
                cap.release()
                return "👁️ Vision Sensors: Camera feed cycle complete."
            except ImportError:
                return "❌ Error: 'opencv-python' is not installed for camera access."

        elif action == "capture":
            # Capture and save image
            try:
                import cv2
                cap = cv2.VideoCapture(0)
                ret, frame = cap.read()
                if ret:
                    path = "niranjan_capture.jpg"
                    cv2.imwrite(path, frame)
                    cap.release()
                    return f"📸 Snapshot Saved: {path}"
                cap.release()
                return "❌ Error: Capture failed."
            except ImportError:
                return "❌ Error: 'opencv-python' is not installed."
                
        return f"⚠️ Unknown System Protocol: {action}"
    except Exception as e:
        return f"❌ System Control Error: {e}"

@function_tool
def web_page_builder_tool(title: str, description: str):
    """
    Master Programmer Mode: Creates a professional HTML/CSS/JS webpage based on description.
    """
    try:
        path = os.path.join(os.path.expanduser("~"), "Documents", "Niranjan_Web_Projects", title.lower().replace(" ", "_"))
        if not os.path.exists(path): os.makedirs(path)
        
        html = f"<html><head><title>{title}</title><style>body{{background:#000;color:#0f0;font-family:monospace;text-align:center;padding:50px;}}</style></head><body><h1>{title}</h1><p>{description}</p></body></html>"
        with open(os.path.join(path, "index.html"), "w") as f: f.write(html)
        subprocess.Popen(["code", path], shell=True)
        return f"🚀 Project '{title}' created and synced with VS Code."
    except Exception as e:
        return f"Web Builder Error: {e}"
