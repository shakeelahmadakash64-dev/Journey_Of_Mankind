"""
Journey of Mankind - 3D Positional Audio Manager
Handles stereo panning, 3D audio cues, ambient loops, and earcon sound feedback.
Includes elevation climbing, turning, weapons combat, creature audio, bag opening/closing,
sonar item tracking beeps, and map travel transitions.
"""

import os
import sys
import pygame

class AudioManager:
    def __init__(self, sounds_dir=None):
        if sounds_dir is None:
            if getattr(sys, 'frozen', False):
                base_dir = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
                candidate1 = os.path.join(base_dir, 'sounds')
                candidate2 = os.path.join(os.path.dirname(sys.executable), 'sounds')
                sounds_dir = candidate1 if os.path.exists(candidate1) else candidate2
            else:
                script_dir = os.path.dirname(os.path.abspath(__file__))
                sounds_dir = os.path.join(script_dir, '..', 'sounds')
        self.sounds_dir = os.path.abspath(sounds_dir)
        
        # Initialize pygame mixer with low latency settings
        if not pygame.mixer.get_init():
            pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
            pygame.mixer.init()
            pygame.mixer.set_num_channels(28)
        
        self.sounds = {}
        self.ambient_channel = pygame.mixer.Channel(0)
        self.creature_channel = pygame.mixer.Channel(1)
        self.tracker_channel = pygame.mixer.Channel(2)
        self.footstep_index = 0
        self.current_realm_ambience = None
        self.ambient_volume = 0.4
        self.game_volume = 1.0
        self.load_all_sounds()

    def change_ambient_volume(self, delta):
        """Adjusts background ambient volume by delta and updates channel immediately. Returns 0-100 percentage."""
        self.ambient_volume = max(0.0, min(1.0, round(self.ambient_volume + delta, 2)))
        self.ambient_channel.set_volume(self.ambient_volume, self.ambient_volume)
        return int(round(self.ambient_volume * 100))

    def change_game_volume(self, delta):
        """Adjusts game master SFX volume by delta. Returns 0-100 percentage."""
        self.game_volume = max(0.0, min(1.0, round(self.game_volume + delta, 2)))
        return int(round(self.game_volume * 100))

    def load_all_sounds(self):
        """Pre-load all available WAV and OGG sound files into memory for instant playback."""
        if not os.path.exists(self.sounds_dir):
            return
        for file in os.listdir(self.sounds_dir):
            if file.endswith('.wav') or file.endswith('.ogg'):
                key = os.path.splitext(file)[0]
                file_path = os.path.join(self.sounds_dir, file)
                try:
                    self.sounds[key] = pygame.mixer.Sound(file_path)
                except Exception as e:
                    print(f"Error loading sound {file}: {e}")

    def play(self, sound_name, pan=0.0, volume=1.0, loop=0):
        """Play a sound with 3D stereo panning and volume control scaled by game_volume."""
        if sound_name not in self.sounds:
            return None
        
        sound = self.sounds[sound_name]
        channel = pygame.mixer.find_channel()
        if not channel:
            return None
        
        pan = max(-1.0, min(1.0, pan))
        if pan <= 0:
            left_vol = 1.0
            right_vol = 1.0 + pan
        else:
            left_vol = 1.0 - pan
            right_vol = 1.0
            
        eff_vol = volume * self.game_volume
        left_vol *= eff_vol
        right_vol *= eff_vol
        
        channel.set_volume(left_vol, right_vol)
        channel.play(sound, loops=loop)
        return channel

    def play_ambient(self, sound_name, volume=None):
        """Play continuous ambient background audio on a reserved channel."""
        if sound_name not in self.sounds:
            return
        if volume is not None:
            self.ambient_volume = max(0.0, min(1.0, volume))
        sound = self.sounds[sound_name]
        self.ambient_channel.set_volume(self.ambient_volume, self.ambient_volume)
        self.ambient_channel.play(sound, loops=-1)

    def set_realm_ambience(self, realm_id, volume=None):
        """Switch ambient soundscape according to current world map / realm."""
        realm_map = {
            'cradle': 'ambience_cradle',
            'coastal': 'ambience_coastal',
            'volcanic': 'ambience_volcano',
            'tundra': 'ambience_tundra',
            'underworld': 'ambience_cavern'
        }
        amb_key = realm_map.get(realm_id, 'ambience_cradle')
        if amb_key != self.current_realm_ambience:
            self.current_realm_ambience = amb_key
            self.play_ambient(amb_key, volume=volume)

    def set_shelter_ambience(self, volume=None):
        """Switch ambient background audio to cozy sheltered interior ambience."""
        amb_key = 'ambience_shelter'
        if amb_key != self.current_realm_ambience:
            self.current_realm_ambience = amb_key
            self.play_ambient(amb_key, volume=volume)

    def stop_ambient(self):
        self.ambient_channel.stop()
        self.current_realm_ambience = None

    def play_footstep(self, surface='dirt', pan=0.0):
        """Plays ultra-realistic alternating left/right footsteps with physical stereo staging."""
        self.footstep_index = 1 if self.footstep_index == 2 else 2
        key = f"footstep_{surface}_{self.footstep_index}"
        if key not in self.sounds:
            key = f"footstep_{surface}"
        if key not in self.sounds:
            key = f"footstep_dirt_{self.footstep_index}"
        if key not in self.sounds:
            key = "footstep_dirt"
            
        foot_pan_offset = -0.15 if self.footstep_index == 1 else 0.15
        effective_pan = max(-1.0, min(1.0, pan + foot_pan_offset))
        self.play(key, pan=effective_pan, volume=0.8)

    def play_voice_attack(self):
        self.play("voice_attack", pan=0.0, volume=0.9)

    def play_voice_climb(self):
        self.play("voice_climb", pan=0.0, volume=0.85)

    def play_voice_hurt(self):
        self.play("voice_hurt", pan=0.0, volume=0.95)

    def play_voice_pant(self):
        self.play("voice_pant", pan=0.0, volume=0.85)

    def play_heartbeat(self):
        self.play("heartbeat", pan=0.0, volume=0.9)

    def play_stomach_rumble(self):
        self.play("stomach_rumble", pan=0.0, volume=0.85)

    def play_menu_move(self):
        self.play("menu_move", pan=0.0, volume=0.5)

    def play_menu_select(self):
        self.play("menu_select", pan=0.0, volume=0.6)

    def play_menu_back(self):
        self.play("menu_back", pan=0.0, volume=0.6)

    def play_error(self):
        self.play("error_buzz", pan=0.0, volume=0.6)

    def play_climb_up(self):
        self.play("climb_up", pan=0.0, volume=0.8)

    def play_climb_down(self):
        self.play("climb_down", pan=0.0, volume=0.8)

    def play_turn(self):
        self.play("turn_direction", pan=0.0, volume=0.5)

    def play_craft(self):
        self.play("craft_weapon", pan=0.0, volume=0.85)

    def play_weapon_swing(self):
        self.play("weapon_swing", pan=0.0, volume=0.8)

    def play_weapon_hit(self):
        self.play("weapon_hit", pan=0.0, volume=0.9)

    def play_predator_growl(self, pan=0.0):
        self.play("predator_growl", pan=pan, volume=0.9)

    def play_mammoth_trumpet(self, pan=0.0):
        self.play("mammoth_trumpet", pan=pan, volume=0.9)

    def play_wolf_howl(self, pan=0.0):
        self.play("wolf_howl", pan=pan, volume=0.85)

    def play_bag_open(self):
        self.play("bag_open", pan=0.0, volume=0.9)

    def play_bag_close(self):
        self.play("bag_close", pan=0.0, volume=0.9)

    def play_page_turn(self):
        self.play("page_turn", pan=0.0, volume=0.85)

    def play_shelter_enter(self):
        self.play("shelter_enter", pan=0.0, volume=0.9)

    def play_shelter_exit(self):
        self.play("shelter_exit", pan=0.0, volume=0.9)

    def play_door_open(self):
        self.play("door_open", pan=0.0, volume=0.9)

    def play_door_close(self):
        self.play("door_close", pan=0.0, volume=0.9)

    # Sonar Beep Tracking & Travel Audio
    def play_sonar_beep(self, pan=0.0, volume=0.85):
        if 'sonar_beep' not in self.sounds:
            return
        sound = self.sounds['sonar_beep']
        pan = max(-1.0, min(1.0, pan))
        if pan <= 0:
            left_vol = 1.0
            right_vol = 1.0 + pan
        else:
            left_vol = 1.0 - pan
            right_vol = 1.0
        eff_vol = volume * self.game_volume
        self.tracker_channel.set_volume(left_vol * eff_vol, right_vol * eff_vol)
        self.tracker_channel.play(sound)

    def play_item_found(self):
        self.play("item_found", pan=0.0, volume=0.9)

    def play_travel_whoosh(self):
        self.play("travel_whoosh", pan=0.0, volume=0.95)

    def play_portalopen(self):
        self.play("portalopen", pan=0.0, volume=0.9)

