
import os
from livekit.agents import function_tool

try:
    import pyttsx3
except ImportError:
    pyttsx3 = None

@function_tool
def text_to_speech_tool(text: str, voice_preset: str = "realistic"):
    """
    Converts text to speech using a high-quality voice preset.
    Inspired by NeuTTS. Preset options: 'realistic', 'fast', 'nano'.
    """
    if pyttsx3 is None:
        return "❌ Voice Error: 'pyttsx3' not installed. Run `pip install pyttsx3`."

    try:
        engine = pyttsx3.init()
        # Simulated preset tuning
        if voice_preset == "realistic":
            engine.setProperty('rate', 150)
            engine.setProperty('volume', 0.9)
        elif voice_preset == "fast":
            engine.setProperty('rate', 200)
        
        # Save to file for the agent to potentially play or send
        output_file = "voice_output.mp3"
        engine.save_to_file(text, output_file)
        engine.say(text) # Speak immediately
        engine.runAndWait()
        
        return f"🔊 Voice Synthesis Complete ({voice_preset}):\n- Generated audio from text: '{text[:50]}...'\n- File saved to: {output_file}"
    except Exception as e:
        return f"Voice synthesis error: {e}"
