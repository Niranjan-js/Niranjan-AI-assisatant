
import os
from livekit.agents import function_tool

@function_tool
def media_processing_tool(file_path: str, action: str = "metadata"):
    """
    Processes audio/video files. Actions: 'metadata', 'transcode_sim'.
    Inspired by FFmpeg/PyAV.
    """
    if not os.path.exists(file_path):
        return f"❌ Error: Media file not found at {file_path}"
    
    try:
        import av
        container = av.open(file_path)
        
        if action == "metadata":
            streams = []
            for stream in container.streams:
                streams.append(f"- {stream.type.upper()}: {stream.codec_context.name} ({stream.rate if hasattr(stream, 'rate') else 'N/A'})")
            
            meta = f"🎬 **Media Metadata ({os.path.basename(file_path)}):**\n"
            meta += "\n".join(streams)
            meta += f"\n- Duration: {container.duration / 1000000:.2f}s"
            return meta
            
        elif action == "transcode_sim":
            return f"⚙️ **Transcoding Simulation:** Initiating FFmpeg-style pipe for {file_path} -> output.mp4 (H.264/AAC)."
            
        return "⚠️ Unsupported media action. Use 'metadata' or 'transcode_sim'."
    except Exception as e:
        return f"Media processing error: {e}"
