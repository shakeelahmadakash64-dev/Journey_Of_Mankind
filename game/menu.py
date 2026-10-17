"""
Journey of Mankind - Accessible Audio Menu & User Interface
Designed specifically for blind gamers with instant speech feedback, audio earcons,
wrapping keyboard navigation, and bilingual localization.
"""

import pygame
import sys
from core.localization import loc

class AccessibleMenu:
    def __init__(self, title, options, audio, speech):
        self.title = title
        self.options = options  # List of tuples: [("Label", callback_fn), ...]
        self.audio = audio
        self.speech = speech
        self.selected_index = 0

    def run(self, screen=None):
        """Run the menu loop. Returns when an option callback returns non-None or user exits."""
        # Announce menu title and first item
        if self.speech:
            self.speech.speak(f"{self.title}. {self.options[self.selected_index][0]}")
        
        clock = pygame.time.Clock()
        while True:
            clock.tick(30)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "QUIT"
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected_index = (self.selected_index - 1) % len(self.options)
                        if self.audio:
                            self.audio.play_menu_move()
                        if self.speech:
                            self.speech.speak(self.options[self.selected_index][0])
                            
                    elif event.key == pygame.K_DOWN:
                        self.selected_index = (self.selected_index + 1) % len(self.options)
                        if self.audio:
                            self.audio.play_menu_move()
                        if self.speech:
                            self.speech.speak(self.options[self.selected_index][0])
                            
                    elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                        if self.audio:
                            self.audio.play_menu_select()
                        callback = self.options[self.selected_index][1]
                        if callback:
                            result = callback()
                            if result is not None:
                                return result
                                
                    elif event.key == pygame.K_PAGEUP:
                        mods = pygame.key.get_mods()
                        if mods & pygame.KMOD_SHIFT and self.audio and hasattr(self.audio, 'change_ambient_volume'):
                            new_vol = self.audio.change_ambient_volume(0.1)
                            msg = loc.tr('volume_ambient_changed', val=new_vol)
                            if self.speech:
                                self.speech.speak(msg)

                    elif event.key == pygame.K_PAGEDOWN:
                        mods = pygame.key.get_mods()
                        if mods & pygame.KMOD_SHIFT and self.audio and hasattr(self.audio, 'change_ambient_volume'):
                            new_vol = self.audio.change_ambient_volume(-0.1)
                            msg = loc.tr('volume_ambient_changed', val=new_vol)
                            if self.speech:
                                self.speech.speak(msg)

                    elif event.key == pygame.K_HOME:
                        if self.audio and hasattr(self.audio, 'change_game_volume'):
                            new_vol = self.audio.change_game_volume(0.1)
                            msg = loc.tr('volume_game_changed', val=new_vol)
                            if self.speech:
                                self.speech.speak(msg)
                            self.audio.play_menu_select()

                    elif event.key == pygame.K_END:
                        if self.audio and hasattr(self.audio, 'change_game_volume'):
                            new_vol = self.audio.change_game_volume(-0.1)
                            msg = loc.tr('volume_game_changed', val=new_vol)
                            if self.speech:
                                self.speech.speak(msg)
                            self.audio.play_menu_select()

                    elif event.key == pygame.K_ESCAPE:
                        if self.audio:
                            self.audio.play_menu_back()
                        return "BACK"

def prompt_text_input(prompt_label, audio, speech, max_len=15):
    """Accessible text input that speaks each character as typed, with backspace support."""
    if speech:
        instructions = loc.tr('name_instructions')
        speech.speak(f"{prompt_label}. {instructions}")
        
    clock = pygame.time.Clock()
    buffer = []
    
    while True:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    result = "".join(buffer).strip()
                    if result:
                        if audio:
                            audio.play_menu_select()
                        return result
                    else:
                        if speech:
                            speech.speak(loc.tr('name_empty_err'))
                        if audio:
                            audio.play_error()
                elif event.key == pygame.K_ESCAPE:
                    if audio:
                        audio.play_menu_back()
                    return None
                elif event.key == pygame.K_BACKSPACE:
                    if buffer:
                        removed = buffer.pop()
                        if speech:
                            speech.speak(f"{loc.tr('char_deleted')}: {removed}")
                    else:
                        if audio:
                            audio.play_error()
                else:
                    char = event.unicode
                    if char and char.isprintable() and len(buffer) < max_len:
                        buffer.append(char)
                        if speech:
                            speech.speak(char)
