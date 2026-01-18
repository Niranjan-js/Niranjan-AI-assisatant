
import pyautogui
import os
import time
from livekit.agents import function_tool

@function_tool
async def screenshot_tool():
    """Takes a screenshot of the main screen and saves it as a PNG."""
    try:
        if not os.path.exists("screenshots"):
            os.makedirs("screenshots")
        
        timestamp = int(time.time())
        path = f"screenshots/niranjan_snap_{timestamp}.png"
        
        # Use pyautogui to take screenshot
        screenshot = pyautogui.screenshot()
        screenshot.save(path)
        
        return f"✅ Screenshot taken successfully, Sir! Saved as {path}"
    except Exception as e:
        return f"❌ Failed to take screenshot: {e}. Please ensure 'pyautogui' and 'Pillow' are installed."
