
try:
    import livekit
    import livekit.agents
    print("✅ LiveKit is installed successfully.")
except ImportError as e:
    print(f"❌ Verification Failed: {e}")
