
import requests
from livekit.agents import function_tool

@function_tool
def get_weather(city: str):
    """
    Fetches real-time weather information for the specified city.
    """
    try:
        # Using wttr.in for a simple, keyless weather check if no API key is set
        response = requests.get(f"https://wttr.in/{city}?format=3")
        if response.status_code == 200:
            return f"🌤️ Weather Report for {city.capitalize()}: {response.text.strip()}"
        else:
            return f"⚠️ Could not fetch weather for {city} via standard protocol."
    except Exception as e:
        return f"❌ Weather Retrieval Error: {e}"
