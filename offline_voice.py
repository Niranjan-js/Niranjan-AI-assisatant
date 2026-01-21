import json
import pyaudio
import os
from vosk import Model, KaldiRecognizer

# Configuration
MODEL_PATH = "model"

def download_model():
    """Downloads the small VOSK English model if missing."""
    import urllib.request
    import zipfile
    
    url = "https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip"
    zip_path = "model.zip"
    
    print(f"📥 Model missing. Downloading from {url}...")
    urllib.request.urlretrieve(url, zip_path)
    
    print("📦 Extracting model...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(".")
    
    # Rename extracted folder to 'model'
    extracted_folder = "vosk-model-small-en-us-0.15"
    if os.path.exists(extracted_folder):
        os.rename(extracted_folder, MODEL_PATH)
    
    os.remove(zip_path)
    print("✅ Model ready.")

_model = None

def get_model():
    """Returns the cached VOSK model, downloading it if necessary."""
    global _model
    if _model is not None:
        return _model
        
    if not os.path.exists(MODEL_PATH):
        try:
            download_model()
        except Exception as e:
            print(f"❌ Failed to download model: {e}")
            return None
            
    print("🧠 Loading VOSK Neural Model...")
    _model = Model(MODEL_PATH)
    return _model

def listen_offline(retries=3):
    """Listens for audio input with retry logic for stream recovery."""
    model = get_model()
    if not model:
        return None

    for attempt in range(retries):
        p = None
        stream = None
        try:
            rec = KaldiRecognizer(model, 16000)
            p = pyaudio.PyAudio()
            
            # Check for available devices (vague diagnostic)
            if p.get_device_count() == 0:
                print("❌ No audio input devices found.")
                return None

            stream = p.open(format=pyaudio.paInt16,
                            channels=1,
                            rate=16000,
                            input=True,
                            frames_per_buffer=8000)
            stream.start_stream()

            print("🎤 Listening (Offline)...")
            while True:
                try:
                    data = stream.read(4000, exception_on_overflow=False)
                except Exception as e:
                    print(f"⚠️ Stream read error: {e}")
                    break
                    
                if len(data) == 0:
                    break
                if rec.AcceptWaveform(data):
                    result = json.loads(rec.Result())
                    text = result.get("text", "")
                    if text:
                        print(f"✅ Recognized: {text}")
                        return text
            
            # If we exited the loop without returning, it might be a stream break
            print(f"⚠️ Stream interrupted on attempt {attempt+1}. Retrying...")
            
        except Exception as e:
            print(f"❌ Mic attempt {attempt+1} failed: {e}")
            if attempt < retries - 1:
                time.sleep(1)
            else:
                return None
        finally:
            if stream:
                try: stream.stop_stream(); stream.close()
                except: pass
            if p:
                try: p.terminate()
                except: pass
    return None

if __name__ == "__main__":
    text = listen_offline()
    if text:
        print(f"You said: {text}")
