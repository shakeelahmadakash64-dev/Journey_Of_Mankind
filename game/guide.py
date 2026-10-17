"""
Journey of Mankind - Interactive In-Game Audio Survival Guide & Prehistoric Encyclopedia
Provides spoken sections covering elevation climbing, directions, prehistoric fauna, and weapons crafting.
"""

from core.localization import loc
from game.menu import AccessibleMenu

class GuideSystem:
    def __init__(self, audio=None, speech=None):
        self.audio = audio
        self.speech = speech

    def open_guide_menu(self, screen=None):
        """Open the interactive guide menu."""
        options = [
            ("1. Navigation, Elevation & Directions", self.read_nav_guide),
            ("2. How to Craft Weapons (Step-by-Step Tutorial)", self.read_weapons_guide),
            ("3. Prehistoric Fauna & Survival Beasts", self.read_fauna_guide),
            ("4. Human Biology & Vitals Guide", self.read_vitals_guide),
            (loc.tr('back'), lambda: "BACK")
        ]
        
        menu = AccessibleMenu(loc.tr('guide_title'), options, self.audio, self.speech)
        menu.run(screen)

    def read_nav_guide(self):
        text = loc.tr('guide_section_nav')
        if self.speech:
            self.speech.speak(text)
        return None

    def read_weapons_guide(self):
        text = loc.tr('guide_section_weapons')
        if self.speech:
            self.speech.speak(text)
        return None

    def read_fauna_guide(self):
        text = loc.tr('guide_section_fauna')
        if self.speech:
            self.speech.speak(text)
        return None

    def read_vitals_guide(self):
        text = loc.tr('guide_section_vitals')
        if self.speech:
            self.speech.speak(text)
        return None
