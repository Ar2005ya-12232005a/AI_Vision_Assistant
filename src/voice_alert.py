import pyttsx3
import threading

class VoiceAlert:
    def __init__(self):
        self._lock = threading.Lock()

    def speak(self, message):
        def run():
            with self._lock:
                try:
                    engine = pyttsx3.init()
                    engine.setProperty('rate', 150)
                    engine.setProperty('volume', 1.0)
                    engine.say(message)
                    engine.runAndWait()
                    engine.stop()
                except Exception as e:
                    print(f"[VOICE ERROR] {e}")
        threading.Thread(target=run, daemon=True).start()