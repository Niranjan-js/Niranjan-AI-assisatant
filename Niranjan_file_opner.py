
import os
import webbrowser
from livekit.agents import function_tool

@function_tool
def Play_file(file_path: str):
    """
    Plays or opens any file using the default system application.
    Supports MP4, MP3, PDF, PNG, JPG, DOCX, etc.
    """
    try:
        abs_path = os.path.abspath(file_path)
        if os.path.exists(abs_path):
            os.startfile(abs_path)
            return f"🎬 Playing file: {os.path.basename(file_path)}"
        else:
            return f"❌ File not found at path: {file_path}"
    except Exception as e:
        return f"⚠️ Playback Error: {e}"
