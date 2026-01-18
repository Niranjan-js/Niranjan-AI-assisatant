from dotenv import load_dotenv

import subprocess, os, sys, asyncio
import logging
import re
from advanced_tools import send_email_tool, play_media_tool, shop_online_tool, download_file_tool, coding_agent_tool
from tech_tools import run_terminal_command, analyze_clipboard_error, search_stackoverflow, github_trending, read_file_content, security_audit_tool, write_file_tool
from vision_tools import detect_objects_tool, analyze_screen_content
from doc_tools import ocr_scan_tool, summarize_doc_tool
from voice_tools import text_to_speech_tool
from physics_tools import solve_physics_problem
from agent_eng_tools import generate_prp_tool, execute_prp_tool
from access_tools import credential_vault_tool, session_audit_report
from skills_manager import publish_to_knowledge_hub, list_available_skills
from mastery_tools import master_coding_architect, programming_guru_advice
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
        sys.exit(1)

    # If no command is provided, default to 'dev' for ease of use
    if len(sys.argv) == 1:
        sys.argv.append("dev")

    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
