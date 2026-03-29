import pyttsx3
import threading

class VoiceAlert:
    def __init__(self):
        self.engine = pyttsx3.init()
        self._lock = threading.Lock()

    def speak(self, message):
        def run():
            with self._lock:
                self.engine.say(message)
                self.engine.runAndWait()
        threading.Thread(target=run, daemon=True).start()