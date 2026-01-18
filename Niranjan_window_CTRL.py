
import os
import subprocess
from livekit.agents import function_tool

@function_tool
def open(app_name: str):
    """
    Opens a system application or utility by name.
    Example: 'notepad', 'calc', 'explorer', 'chrome'.
    """
    try:
        # Using 'start' to open applications in Windows
        subprocess.Popen(f"start {app_name}", shell=True)
        return f"🚀 Opening {app_name}, Sir. Commands are being processed."
    except Exception as e:
        return f"⚠️ Could not open {app_name}: {e}"

@function_tool
def close(app_name: str):
    """
    Forcefully closes a running application.
    Example: 'notepad', 'chrome', 'python'.
    """
    try:
        subprocess.run(f"taskkill /F /IM {app_name}.exe /T", shell=True)
        return f"🛑 {app_name} has been terminated as requested."
    except Exception as e:
        return f"⚠️ Error terminating {app_name}: {e}"

@function_tool
def folder_file(path: str):
    """
    Opens a specific folder or directory path in Windows Explorer.
    """
    try:
        if os.path.exists(path):
            os.startfile(path)
            return f"📂 Opening folder at: {path}"
        else:
            return f"❓ Path not found: {path}"
    except Exception as e:
        return f"⚠️ Folder access error: {e}"
