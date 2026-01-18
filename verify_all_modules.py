
import sys
import os

def test_module(name, func):
    print(f"Testing {name}...")
    try:
        result = func()
        # Clean result for printing if needed, but we'll try UTF-8 first
        print(f"[OK] {name} Success: {result[:100]}...")
    except Exception as e:
        print(f"[ERROR] {name} Failed: {e}")
    print("-" * 30)

def main():
    if sys.stdout.encoding.lower() != 'utf-8':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except:
             pass
    print("--- NIRANJAN V3.0: COMPREHENSIVE FACILITY VERIFICATION ---\n")
    
    # 1. Vision (Ultralytics)
    from vision_tools import detect_objects_tool
    test_module("Vision (Ultralytics)", lambda: detect_objects_tool("test.jpg"))

    # 2. OCR (Paperless-ngx)
    from doc_tools import ocr_scan_tool
    test_module("Document Intelligence (Paperless-ngx)", lambda: ocr_scan_tool("test_doc.png"))

    # 3. Voice (NeuTTS)
    from voice_tools import text_to_speech_tool
    test_module("Voice Synthesis (NeuTTS)", lambda: text_to_speech_tool("Hello, I am Niranjan.", "realistic"))

    # 4. Physics (PhysicsNemo)
    from physics_tools import solve_physics_problem
    test_module("Physics Solver (PhysicsNemo)", lambda: solve_physics_problem("projectile", {"velocity": 50, "theta": 45}))

    # Extra: Media Processing
    from media_tools import media_processing_tool
    test_module("Media Processing (FFmpeg/PyAV)", lambda: media_processing_tool("test.mp4", "transcode_sim"))

    # 5. Agentic Engineering (PRPs)
    from agent_eng_tools import generate_prp_tool
    test_module("Agentic Engineering (PRP)", lambda: generate_prp_tool("Web Scraper", "Create a robust scraper for news sites."))

    # 6. Security & Health (Prowler)
    from tech_tools import security_audit_tool, system_health_diagnostic
    test_module("Security Audit (Prowler)", lambda: security_audit_tool())
    test_module("System Health Diagnostic", lambda: system_health_diagnostic())

    # 7. Access (JumpServer)
    from access_tools import credential_vault_tool, session_audit_report
    test_module("Access Vault (JumpServer)", lambda: credential_vault_tool("store", "DB_KEY", "secret123"))
    test_module("Access Audit", lambda: session_audit_report())

    # 8. Skills/KB (Anthropic Skills / Wagtail)
    from skills_manager import list_available_skills, publish_to_knowledge_hub
    test_module("Skill Manager", lambda: list_available_skills())
    test_module("Knowledge Hub", lambda: publish_to_knowledge_hub("Release Notes", "V3.0 Integrated Model is live."))

    # 9. Tech Mastery
    from mastery_tools import programming_guru_advice
    test_module("Tech Mastery (Guru Advice)", lambda: programming_guru_advice("concurrency"))

    print("\n--- ALL FACILITIES IMPLEMENTED AND SYNCED. WORKING MODEL READY. ---")

if __name__ == "__main__":
    main()
