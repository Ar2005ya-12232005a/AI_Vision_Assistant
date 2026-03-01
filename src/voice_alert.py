import pyttsx3

class VoiceAlert:
    def __init__(self):
        self.engine = pyttsx3.init()

    def speak(self, message):
        self.engine.say(message)
        self.engine.runAndWait()