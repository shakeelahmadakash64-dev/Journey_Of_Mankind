"""
Journey of Mankind - Prologue: The Genesis & Dawn of Humanity
Immersive audio narrative of the creation of the cosmos and the dawn of humankind on Primordial Earth.
Fully localized for English (primary) and Urdu (secondary).
"""

import time
import pygame
from core.localization import loc

class Prologue:
    def __init__(self, audio, speech):
        self.audio = audio
        self.speech = speech

    def run(self):
        """Run the multi-scene audio prologue. Returns True when finished or skipped."""
        print("[Prologue] Starting Cosmic Genesis...")
        
        scenes = [
            {
                "audio_action": lambda: self.audio.play("cosmic_boom", volume=1.0),
                "text_key": "prologue_scene1",
                "wait": 6.5
            },
            {
                "audio_action": lambda: self.audio.play_ambient("wind_ambient", volume=0.5),
                "text_key": "prologue_scene2",
                "wait": 6.5
            },
            {
                "audio_action": lambda: (self.audio.play_heartbeat(), self.audio.play_footstep("dirt", pan=0.0)),
                "text_key": "prologue_scene3",
                "wait": 7.0
            },
            {
                "audio_action": lambda: self.audio.play("menu_select", volume=0.7),
                "text_key": "prologue_scene4",
                "wait": 7.5
            }
        ]

        if self.speech:
            self.speech.speak(loc.tr('prologue_start'))

        time.sleep(1.5)

        for i, scene in enumerate(scenes):
            # Check if user pressed skip
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.audio.stop_ambient()
                    if self.speech:
                        self.speech.speak(loc.tr('prologue_skipped'))
                    return True

            # Trigger scene audio
            scene["audio_action"]()
            
            # Speak narration in active language
            if self.speech:
                self.speech.speak(loc.tr(scene["text_key"]))
                
            # Wait for narration and audio to play through
            start_wait = time.time()
            while time.time() - start_wait < scene["wait"]:
                pygame.time.delay(50)
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        self.audio.stop_ambient()
                        if self.speech:
                            self.speech.speak(loc.tr('prologue_skipped'))
                        return True

        self.audio.stop_ambient()
        return True
