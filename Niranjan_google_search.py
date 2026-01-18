
import webbrowser
from datetime import datetime
from livekit.agents import function_tool

@function_tool
def google_search(query: str):
    """
    Performs a standard Google Search for the user's query in the default browser.
    """
    try:
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        webbrowser.open(url)
        return f"🌐 Searching Google for: '{query}'. Results opening in browser."
    except Exception as e:
        return f"⚠️ Search Error: {e}"

@function_tool
def get_current_datetime():
    """
    Returns the current date and precise time.
    """
    now = datetime.now()
    return now.strftime("📅 Date: %Y-%m-%d | ⏰ Time: %H:%M:%S")
    
@function_tool
def check_system_time():
    """Dedicated tool to check current time for the user."""
    return get_current_datetime()
