"""
Journey of Mankind - Screen Reader & TTS Speech Engine
Interfaces directly with NVDA, JAWS, and Windows SAPI5 through accessible_output2.
Provides interruptible speech essential for blind gamers.
"""

import sys

class SpeechManager:
    def __init__(self):
        self.speaker = None
        self.backend_name = "None"
        self._init_speaker()

    def _init_speaker(self):
        try:
            import accessible_output2.outputs.auto
            self.speaker = accessible_output2.outputs.auto.Auto()
            self.backend_name = self.speaker.name or "Auto Output"
        except Exception as e:
            print(f"[SpeechManager Warning] Could not initialize accessible_output2: {e}")
            try:
                import win32com.client
                self.speaker = win32com.client.Dispatch("SAPI.SpVoice")
                self.backend_name = "SAPI5 Direct"
            except Exception as e2:
                print(f"[SpeechManager Warning] Fallback SAPI5 failed: {e2}")
                self.speaker = None
                self.backend_name = "Console Only"

    def speak(self, text, interrupt=True):
        """
        Speak text immediately.
        If interrupt is True, stops any ongoing speech before speaking.
        """
        if not text:
            return
        
        # Always output to console for visual debugging or low-vision assistance
        try:
            print(f"[Voice] {text}")
        except UnicodeEncodeError:
            print(f"[Voice] {text.encode(sys.stdout.encoding or 'utf-8', errors='replace').decode(sys.stdout.encoding or 'utf-8')}")
        
        if not self.speaker:
            return

        try:
            if hasattr(self.speaker, 'speak'):
                # accessible_output2 style
                self.speaker.speak(str(text), interrupt=interrupt)
            elif hasattr(self.speaker, 'Speak'):
                # win32com SAPI style (SVSFlagsAsync = 1, SVSFPurgeBeforeSpeak = 2)
                flags = 1
                if interrupt:
                    flags |= 2
                self.speaker.Speak(str(text), flags)
        except Exception as e:
            print(f"[Speech Error] {e}")

    def silence(self):
        """Immediately silence ongoing speech."""
        if not self.speaker:
            return
        try:
            if hasattr(self.speaker, 'silence'):
                self.speaker.silence()
            elif hasattr(self.speaker, 'Speak'):
                self.speaker.Speak("", 2)
        except Exception:
            pass
