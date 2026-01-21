import os
from Niranjan_prompts import behavior_prompts

# Modes state
CURRENT_MODE = "normal" 

def offline_chatbot(command):
    """Simple rule-based responses for offline use with mode support."""
    global CURRENT_MODE
    cmd = command.lower()
    
    # Mode Toggles
    if "bhakti mode" in cmd or "spiritual mode" in cmd:
        CURRENT_MODE = "bhakti"
        return "जय श्री राम 🙏 | Spiritual protocol activate किया जा चुका है sir — अब मैं भक्ति mode में हूँ।"
    if "bakchodi mode" in cmd or "mazakiya mode" in cmd:
        CURRENT_MODE = "bakchodi"
        return "Bakchodi mode activated sir 😎 Ab main serious AI nahi, thoda meme-certified chatbot hoon!"
    if "normal mode" in cmd or "standard mode" in cmd:
        CURRENT_MODE = "normal"
        return "भक्ति protocol बंद किया जा चुका है sir 🙏, अब मैं सामान्य operational mode में वापस हूँ।"

    # Bhakti Mode Responses
    if CURRENT_MODE == "bhakti":
        if "hanuman chalisa" in cmd:
            return "॥ दोहा ॥ श्रीगुरु चरन सरोज रज... [Hanuman Chalisa is long, starting play protocol]"
        return "जय श्री राम सर। मैं अभी भक्ति मोड में हूँ, शांति और धर्म की बातें करें।"

    # Bakchodi Mode Responses
    if CURRENT_MODE == "bakchodi":
        if "pagal" in cmd:
            return "Pagal main nahi sir, main limited edition hoon 🧠💅"
        if "chup" in cmd:
            return "Sir main chup ho jaunga, par mere emotions background me run karte rahenge 😔"
        if "kaam" in cmd:
            return "Sir main kaam kar leta, par aaj processor ne chhutti maang li hai — bole, 'thoda Netflix aur chill karne do!' 📺"
        return "Sir, life ek coding bug jaisi hai — jab fix karo to ek aur error milta hai! 😂"

    # Normal Mode / Tool Triggers
    if "hello" in cmd or "hi" in cmd:
        return "Vanakkam Sir! Main Niranjan hoon v3.0, aapka personal AI assistant. Batayein main aapki help kaise kar sakta hoon?"
    
    # System Triggers
    if "shutdown" in cmd: return "[TRIGGER_SHUTDOWN]"
    if "restart" in cmd: return "[TRIGGER_RESTART]"
    if "wifi" in cmd: return "[TRIGGER_WIFI_TOGGLE]"
    if "camera" in cmd or "capture" in cmd: return "[TRIGGER_CAMERA]"
    if "youtube" in cmd: return "[TRIGGER_YOUTUBE]"
    if "whatsapp" in cmd: return "[TRIGGER_WHATSAPP]"
    
    if "ecommerce" in cmd or "online store" in cmd or "website" in cmd: return "[TRIGGER_ECOMMERCE]"
    
    # General Tools
    if "security" in cmd: return "[TRIGGER_SECURITY_AUDIT]"
    if "health" in cmd or "diagnostic" in cmd: return "[TRIGGER_SYSTEM_HEALTH]"
    if "screen" in cmd and ("dekho" in cmd or "analyze" in cmd): return "[TRIGGER_SCREEN_VISION]"
    if "screenshot" in cmd: return "[TRIGGER_SCREENSHOT]"
    
    # Professional Coding Support
    if "code" in cmd or "program" in cmd:
        for lang in ["java", "python", "c++", "css", "html", "javascript"]:
            if lang in cmd:
                return f"I am preparing to generate a high-level {lang.upper()} implementation for you, sir. Initiating Master Programmer Protocol."

    if "where" in cmd and "sir" in cmd:
        return "Vikash sir Bihar ke Gopalganj se hain. Wahi mitti jahan log dil se kaam karte hain! 💫"

    return "I am scanning my protocols to best assist you with that request, sir. Should I initiate a system diagnostic?"

async def online_chatbot(prompt):
    """Advanced AI responses using Google Gemini."""
    try:
        import google.generativeai as genai
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            return "Error: GOOGLE_API_KEY not found in .env"
            
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error connecting to online AI: {e}"

def sync_chatbot_reply(command, online=None):
    """Sync version for GUI and Local Mode."""
    if online is None:
        online = bool(os.getenv("GOOGLE_API_KEY"))
        
    if not online:
        return offline_chatbot(command)
    else:
        try:
            import google.generativeai as genai
            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key: return offline_chatbot(command)
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(command)
            return response.text
        except:
            return offline_chatbot(command)

def chatbot_reply(command, online=None):
    """Wrapper to choose between offline and online logic (sync for now)."""
    return sync_chatbot_reply(command, online)
