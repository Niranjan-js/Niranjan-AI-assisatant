
import os
import subprocess
import webbrowser
from livekit.agents import function_tool

@function_tool
def system_control_tool(action: str):
    """
    Controls system power and core apps. 
    Actions: 'shutdown', 'restart', 'open_whatsapp', 'open_messages', 'open_youtube'.
    """
    try:
        if action == "shutdown":
            # os.system("shutdown /s /t 1") # Safety: Just return command for now to avoid killing agent
            return "🖥️ System Shutdown command prepared. (Simulated to prevent agent disconnect)"
            
        elif action == "restart":
            return "🖥️ System Restart command prepared."
            
        elif action == "open_whatsapp":
            webbrowser.open("https://web.whatsapp.com")
            return "📱 Opening WhatsApp Web in your browser."
            
        elif action == "open_messages":
            # For Windows, we can try to open the Phone Link app or generic web messages
            subprocess.Popen("start ms-chat:", shell=True) # Windows 11 Chat/Teams
            return "💬 Opening Windows Messaging/Chat app."
            
        elif action == "open_youtube":
            webbrowser.open("https://www.youtube.com")
            return "📺 Opening YouTube in your browser."
            
        return f"Unknown system action: {action}"
    except Exception as e:
        return f"System Control Error: {e}"

@function_tool
def web_page_builder_tool(title: str, description: str):
    """
    Master Programmer Mode: Creates a professional HTML/CSS/JS webpage based on description.
    Syncs with VS Code for immediate work.
    """
    try:
        base_path = os.path.join(os.path.expanduser("~"), "Documents", "Niranjan_Web_Projects")
        project_name = title.lower().replace(" ", "_")
        path = os.path.join(base_path, project_name)
        
        if not os.path.exists(path):
            os.makedirs(path)
            
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>{title}</title>
    <style>
        body {{ font-family: 'Segoe UI', sans-serif; background: #0a0e14; color: #fff; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; }}
        .container {{ text-align: center; border: 1px solid #3cc8ff; padding: 2rem; border-radius: 15px; box-shadow: 0 0 20px rgba(60,200,255,0.2); }}
        h1 {{ color: #3cc8ff; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{title}</h1>
        <p>{description}</p>
        <p>Built by Niranjan AI v3.0</p>
    </div>
</body>
</html>"""
        
        index_path = os.path.join(path, "index.html")
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(html_content)
            
        # Sync with VS Code
        subprocess.Popen(["code", path], shell=True)
        
        return f"🚀 **Web Project '{title}' Created!**\n- Location: {path}\n- Status: Synced with VS Code.\n- Live Action: Opening implementation environment now."
        
    except Exception as e:
        return f"Web Builder Error: {e}"
