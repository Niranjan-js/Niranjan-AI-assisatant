from dotenv import load_dotenv
import subprocess, os, sys, asyncio, logging, re, time, atexit

# --- SINGLETON PROCESS LOCK ---
LOCK_FILE = "niranjan.lock"
if os.path.exists(LOCK_FILE):
    try:
        if time.time() - os.path.getmtime(LOCK_FILE) < 10:
            print("⚠️ Another instance of Niranjan is already running. Exiting.")
            sys.exit(0)
    except: pass
with open(LOCK_FILE, "w") as f: f.write(str(os.getpid()))

def release_lock():
    if os.path.exists(LOCK_FILE):
        try: os.remove(LOCK_FILE)
        except: pass
atexit.register(release_lock)

async def update_lock_heartbeat():
    while True:
        if os.path.exists(LOCK_FILE):
            try: os.utime(LOCK_FILE, None)
            except: pass
        await asyncio.sleep(5)

from advanced_tools import send_email_tool, play_media_tool, shop_online_tool, download_file_tool, coding_agent_tool, send_whatsapp_tool
from tech_tools import run_terminal_command, analyze_clipboard_error, search_stackoverflow, github_trending, read_file_content, security_audit_tool, write_file_tool, system_health_diagnostic
from vision_tools import detect_objects_tool, analyze_screen_content
from doc_tools import ocr_scan_tool, summarize_doc_tool
from voice_tools import text_to_speech_tool
from physics_tools import solve_physics_problem
from agent_eng_tools import generate_prp_tool, execute_prp_tool
from access_tools import credential_vault_tool, session_audit_report
from skills_manager import publish_to_knowledge_hub, list_available_skills
from mastery_tools import master_coding_architect, programming_guru_advice, master_ecommerce_builder
from media_tools import media_processing_tool
from control_tools import system_control_tool, web_page_builder_tool

from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import (
    google,
    noise_cancellation,
)
from Niranjan_prompts import behavior_prompts, Reply_prompts
from Niranjan_screenshot import screenshot_tool
from Niranjan_google_search import google_search, get_current_datetime
from memory.niranjan_memory import load_memory, save_memory, get_recent_conversations, add_memory_entry
from memory_interceptor import MEMORY_KEYWORDS
from niranjan_get_whether import get_weather
from Niranjan_window_CTRL import open, close, folder_file
from Niranjan_file_opner import Play_file
from keyboard_mouse_CTRL import move_cursor_tool, mouse_click_tool, scroll_cursor_tool, type_text_tool, press_key_tool, swipe_gesture_tool, press_hotkey_tool, control_volume_tool
from auth_system import authenticate_owner
from offline_voice import listen_offline
from chatbot_logic import chatbot_reply
from fuzzywuzzy import process # For fuzzy command matching

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Memory interceptor flag - set to True to enable client-side memory injection
ENABLE_MEMORY_INTERCEPTOR = True


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(instructions=behavior_prompts,
                         tools=[
                            google_search,
                            get_current_datetime,
                            get_weather,
                            open, #ये apps ओपन करने के लिए हैं
                            close, 
                            load_memory, save_memory,
                            get_recent_conversations, # पिछली बातचीत निकालने के लिए
                            add_memory_entry, # मेमोरी में entry जोड़ने के लिए
                            folder_file, #ये folder ओपन करने के लिए है
                            Play_file,  #ये file रन करने के लिए है जैसे कि MP4, MP3, PDF, PPT, img, png etc.
                            screenshot_tool, # स्क्रीनशॉट लेने के लिए टूल
                            move_cursor_tool, #ये cursor move करने के लिए है
                            mouse_click_tool, #ये mouse click करने के लिए है
                            scroll_cursor_tool, #ये cursor scroll करने के लिए है
                            type_text_tool, #ये text type करने के लिए है
                            press_key_tool, #ये key press करने के लिए है
                            press_hotkey_tool, #ये hotkey press करने के लिए है
                            control_volume_tool, #ये volume control करने के लिए है
                            swipe_gesture_tool, #ये gesture wipe करने के लिए है 
                            send_email_tool,
                            send_whatsapp_tool, # WhatsApp automation tool
                            play_media_tool,
                            shop_online_tool,
                            download_file_tool,
                            coding_agent_tool,
                            run_terminal_command,
                            analyze_clipboard_error,
                            search_stackoverflow,
                            github_trending,
                            read_file_content,
                            security_audit_tool,
                            write_file_tool,
                            system_health_diagnostic,
                            detect_objects_tool,
                            analyze_screen_content,
                            ocr_scan_tool,
                            summarize_doc_tool,
                            text_to_speech_tool,
                            solve_physics_problem,
                            generate_prp_tool,
                            execute_prp_tool,
                            credential_vault_tool,
                            session_audit_report,
                            publish_to_knowledge_hub,
                            list_available_skills,
                            master_coding_architect,
                            programming_guru_advice,
                            media_processing_tool,
                            system_control_tool,
                            web_page_builder_tool
                            
                         ]
                         )


async def entrypoint(ctx: agents.JobContext):
    """Entry point for LiveKit agent session with improved error handling"""
    # Security: Face Recognition Login
    print("🔒 System Security: Authenticating...")
    if not authenticate_owner():
        print("❌ Access Denied: Unauthorized usage detected.")
        sys.exit(1)
    print("✅ Access Granted: Welcome, Niranjan.")

    max_retries = 5  # Increased from 3
    retry_count = 0
    base_wait_time = 3  # Increased from 2
    
    while retry_count < max_retries:
        try:
            print(f"\n🚀 Starting agent session (attempt {retry_count + 1}/{max_retries})...")
            
            session = AgentSession(
                llm=google.beta.realtime.RealtimeModel(
                    voice="Charon"
                )
            )
            
            await session.start(
                room=ctx.room,
                agent=Assistant(),
                room_input_options=RoomInputOptions(
                    noise_cancellation=noise_cancellation.BVC(),
                    video_enabled=True 
                ),
            )

            await ctx.connect()
            print("✅ Connected to room, waiting for audio input...")

            # Generate reply with timeout handling
            try:
                # Try to inject memory context into the reply instructions
                instructions = Reply_prompts
                
                if ENABLE_MEMORY_INTERCEPTOR:
                    try:
                        print("🧠 Fetching memory context...")
                        # Fetch recent conversations to inject context
                        memory_context = await get_recent_conversations(limit=5)  # Reduced from 10
                        
                        # Only inject if there's actual memory, keep it brief
                        if "अभी तक कोई बातचीत याद नहीं है" not in memory_context:
                            instructions = f"""{Reply_prompts}

[RECENT CONTEXT]
{memory_context}
[/CONTEXT]"""
                            print("✅ Memory context injected")
                        else:
                            instructions = Reply_prompts
                            print("ℹ️ No previous conversations to inject")
                    except Exception as e:
                        print(f"⚠️ Memory injection skipped: {e}")
                        instructions = Reply_prompts
                
                print("📡 Sending instructions to LLM (this may take a moment)...")
                await session.generate_reply(
                    instructions=instructions
                )
                print("✅ Session completed successfully")
                break  # Success - exit retry loop
                
            except Exception as e:
                error_msg = str(e).lower()
                print(f"⚠️ Reply generation error (attempt {retry_count + 1}/{max_retries}): {e}")
                
                # Check if it's a timeout/connection error worth retrying
                if any(keyword in error_msg for keyword in ["timed out", "timeout", "connection", "websocket", "closed"]):
                    if retry_count < max_retries - 1:
                        retry_count += 1
                        wait_time = base_wait_time * retry_count  # Exponential backoff
                        print(f"🔄 Connection issue detected. Retrying in {wait_time}s... ({retry_count}/{max_retries})")
                        await asyncio.sleep(wait_time)
                        continue
                    else:
                        print("❌ Max retries exceeded after multiple timeouts")
                        raise
                else:
                    # Not a timeout - propagate error immediately
                    raise
            
        except KeyboardInterrupt:
            print("\n⛔ Agent stopped by user")
            break
        except Exception as e:
            print(f"❌ Session error (attempt {retry_count + 1}/{max_retries}): {e}")
            retry_count += 1
            
            if retry_count < max_retries:
                wait_time = base_wait_time * retry_count  # Exponential backoff
                print(f"⏳ Waiting {wait_time}s before retry...")
                await asyncio.sleep(wait_time)
            else:
                print("❌ Max retries exceeded. Shutting down.")
                raise


async def run_local_mode():
    """Fallback mode when LiveKit is not configured. Uses offline voice and chatbot."""
    # Start heartbeat to keep lock alive
    asyncio.create_task(update_lock_heartbeat())
    
    print("\n" + "="*60)
    print("🤖 NIRANJAN LOCAL MODE (OFFLINE)")
    print("="*60)
    
    # Security: Face Recognition Login (Robust)
    print("🔒 System Security: Authenticating...")
    auth_success = False
    for attempt in range(3):
        if authenticate_owner(timeout_seconds=15):
            auth_success = True
            break
        else:
            print(f"⚠️ Auth Attempt {attempt+1} failed. Retrying...")
            text_to_speech_tool("Security authentication failed. Please look at the camera, sir.")
            await asyncio.sleep(2)
            
    if not auth_success:
        print("❌ Access Denied: Max authentication attempts reached.")
        text_to_speech_tool("Access Denied. System lockdown initiated.")
        sys.exit(1)
        
    print("✅ Access Granted: Welcome, Niranjan.")
    text_to_speech_tool("Welcome back, sir. Listening mode engaged.")
    
    async def handle_tool_error(error_msg):
        """Autonomous Self-Repair Protocol"""
        if "No module named" in str(error_msg):
            try:
                module_name = str(error_msg).split("'")[-2]
                text_to_speech_tool(f"Sir, it seems {module_name} is missing. Attempting self-repair.")
                subprocess.run([sys.executable, "-m", "pip", "install", module_name], capture_output=True)
                return f"✅ Component '{module_name}' installed. Please repeat the command."
            except:
                return f"⚠️ Self-repair failed for {module_name}."
        return f"⚠️ Diagnostics suggest: {error_msg}"

    while True:
        try:
            command = listen_offline()
            if not command:
                continue
            
            print(f"👤 User: {command}")
            input_val = command.lower()
            
            # Fuzzy Dispatcher for Advanced Tooling
            choices = ["time", "weather", "open", "whatsapp", "email", "security audit", "health check", "architect", "prp generate", "prp execute", "screenshot", "vision scan", "shutdown", "restart", "wifi", "camera", "youtube", "ecommerce"]
            match, score = process.extractOne(input_val, choices)
            
            response = ""
            
            if score > 75:
                if match == "time": response = get_current_datetime()
                elif match == "weather": response = get_weather("current location")
                elif match == "ecommerce":
                    text_to_speech_tool("Naming your store.")
                    name = listen_offline()
                    text_to_speech_tool("What is the store niche?")
                    niche = listen_offline()
                    response = master_ecommerce_builder(name, niche) if name and niche else "Aborted."
                elif match == "whatsapp" or match == "whatsapp":
                    response = system_control_tool("open_whatsapp")
                elif match == "youtube":
                    response = system_control_tool("open_youtube")
                elif match == "shutdown":
                    response = system_control_tool("shutdown")
                elif match == "restart":
                    response = system_control_tool("restart")
                elif match == "wifi":
                    response = system_control_tool("toggle_wifi")
                elif match == "camera":
                    response = system_control_tool("open_camera")
                elif match == "email":
                    text_to_speech_tool("To whom?")
                    to = listen_offline()
                    text_to_speech_tool("Subject?")
                    sub = listen_offline()
                    text_to_speech_tool("Body?")
                    body = listen_offline()
                    response = send_email_tool(to, sub, body) if all([to, sub, body]) else "Aborted."
                elif match == "security audit": 
                    text_to_speech_tool("Niranjan Security Protocol engaged.")
                    response = security_audit_tool()
                elif match == "health check": response = system_health_diagnostic()
                elif match == "architect": 
                    text_to_speech_tool("Architect Mode. What is the task?")
                    desc = listen_offline()
                    response = master_coding_architect(desc) if desc else "No task defined."
                elif match == "prp generate":
                    text_to_speech_tool("Naming the blueprint.")
                    name = listen_offline()
                    text_to_speech_tool("Describe requirements.")
                    req = listen_offline()
                    response = generate_prp_tool(name, req) if name and req else "Aborted."
                elif match == "prp execute":
                    text_to_speech_tool("Which blueprint should I execute?")
                    name = listen_offline()
                    prp_path = f"PRPs/{name.lower().replace(' ', '_')}.md"
                    response = execute_prp_tool(prp_path)
                elif match == "screenshot": response = await screenshot_tool()
                elif match == "vision scan": response = await analyze_screen_content()
                elif match == "open":
                    app = input_val.replace("open", "").strip()
                    response = open(app)
            else:
                response = chatbot_reply(command)
                
                # Handling mode triggers (Bakchodi/Bhakti) or direct tool triggers from chatbot
                if "[TRIGGER_SHUTDOWN]" in str(response): response = system_control_tool("shutdown")
                elif "[TRIGGER_RESTART]" in str(response): response = system_control_tool("restart")
                elif "[TRIGGER_WIFI_TOGGLE]" in str(response): response = system_control_tool("toggle_wifi")
                elif "[TRIGGER_CAMERA]" in str(response): response = system_control_tool("open_camera")
                elif "[TRIGGER_YOUTUBE]" in str(response): response = system_control_tool("open_youtube")
                elif "[TRIGGER_WHATSAPP]" in str(response): response = system_control_tool("open_whatsapp")
                elif "[TRIGGER_ECOMMERCE]" in str(response):
                    text_to_speech_tool("Initializing Master E-commerce Builder. Naming your store.")
                    name = listen_offline()
                    text_to_speech_tool("What is the store niche?")
                    niche = listen_offline()
                    response = master_ecommerce_builder(name, niche) if name and niche else "Aborted."
                elif "[TRIGGER_SECURITY_AUDIT]" in str(response): response = security_audit_tool()
                elif "[TRIGGER_SYSTEM_HEALTH]" in str(response): response = system_health_diagnostic()
                elif "[TRIGGER_SCREEN_VISION]" in str(response): response = await analyze_screen_content()
                elif "[TRIGGER_SCREENSHOT]" in str(response): response = await screenshot_tool()
                
            print(f"🤖 Niranjan: {response}")
            text_to_speech_tool(str(response))
                
        except KeyboardInterrupt:
            print("\n⛔ Local mode stopped by user")
            break
        except Exception as e:
            err_res = await handle_tool_error(e)
            print(f"⚠️ Local mode error: {err_res}")
            text_to_speech_tool(str(err_res))
            await asyncio.sleep(1)


if __name__ == "__main__":
    # Try to start the GUI alongside the agent (runs in a separate process)
    try:
        gui_path = os.path.join(os.path.dirname(__file__), "niranjan_gui.py")
        if os.path.exists(gui_path):
            print(f"🚀 Starting Niranjan HUD at {gui_path}")
            subprocess.Popen([sys.executable, gui_path], stdout=None, stderr=None, stdin=None, close_fds=True)
        else:
            print("niranjan_gui.py not found; GUI will not be started.")
    except Exception as e:
        print("Failed to start GUI subprocess:", e)

    # Pre-flight check for LiveKit credentials
    lk_url = os.getenv("LIVEKIT_URL")
    lk_key = os.getenv("LIVEKIT_API_KEY")
    lk_secret = os.getenv("LIVEKIT_API_SECRET")

    if not all([lk_url, lk_key, lk_secret]):
        print("\n" + "!"*60)
        print("⚠️  MISSING LIVEKIT CREDENTIALS")
        print("!"*60)
        print("Niranjan requires a LiveKit server connection to function.")
        print("Please fill in the following in your .env file:")
        print(f"- LIVEKIT_URL: {'[X] Found' if lk_url else '[ ] MISSING'}")
        print(f"- LIVEKIT_API_KEY: {'[X] Found' if lk_key else '[ ] MISSING'}")
        print(f"- LIVEKIT_API_SECRET: {'[X] Found' if lk_secret else '[ ] MISSING'}")
        print("\nYou can get these from https://cloud.livekit.io for free.")
        print("!"*60 + "\n")
        
        # Fallback to Local Mode instead of exiting
        print("🔄 Falling back to LOCAL MODE...")
        asyncio.run(run_local_mode())
        sys.exit(0)

    # If no command is provided, default to 'dev' for ease of use
    if len(sys.argv) == 1:
        sys.argv.append("dev")

    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
