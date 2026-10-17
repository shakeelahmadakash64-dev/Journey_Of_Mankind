"""
Journey of Mankind - 3D Positional Audio Manager
Handles stereo panning, 3D audio cues, ambient loops, and earcon sound feedback.
Includes elevation climbing, turning, weapons combat, creature audio, bag opening/closing,
sonar item tracking beeps, and map travel transitions.
"""

import os
import sys
import random
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
            pygame.mixer.set_num_channels(32)
        
        self.sounds = {}
        self.ambient_channel = pygame.mixer.Channel(0)
        self.creature_channel = pygame.mixer.Channel(1)
        self.tracker_channel = pygame.mixer.Channel(2)
        self.weather_channel = pygame.mixer.Channel(3)
        self.cooking_channel = pygame.mixer.Channel(4)
        
        self.step_counter = 0
        self.last_step_var = 1
        self.current_realm_ambience = None
        self.current_weather_audio = None
        
        self.ambient_volume = 0.4
        self.weather_volume = 0.5
        self.sfx_volume = 1.0
        self.game_volume = 1.0
        self.load_all_sounds()

    def change_ambient_volume(self, delta):
        """Adjusts background ambient volume by delta and updates channel immediately. Returns 0-100 percentage."""
        self.ambient_volume = max(0.0, min(1.0, round(self.ambient_volume + delta, 2)))
        self.ambient_channel.set_volume(self.ambient_volume * self.game_volume, self.ambient_volume * self.game_volume)
        return int(round(self.ambient_volume * 100))

    def change_weather_volume(self, delta):
        """Adjusts weather ambient volume by delta and updates channel immediately. Returns 0-100 percentage."""
        self.weather_volume = max(0.0, min(1.0, round(self.weather_volume + delta, 2)))
        self.weather_channel.set_volume(self.weather_volume * self.game_volume, self.weather_volume * self.game_volume)
        return int(round(self.weather_volume * 100))

    def change_sfx_volume(self, delta):
        """Adjusts sound effects volume by delta. Returns 0-100 percentage."""
        self.sfx_volume = max(0.0, min(1.0, round(self.sfx_volume + delta, 2)))
        return int(round(self.sfx_volume * 100))

    def change_game_volume(self, delta):
        """Adjusts game master SFX volume by delta. Returns 0-100 percentage."""
        self.game_volume = max(0.0, min(1.0, round(self.game_volume + delta, 2)))
        self.ambient_channel.set_volume(self.ambient_volume * self.game_volume, self.ambient_volume * self.game_volume)
        self.weather_channel.set_volume(self.weather_volume * self.game_volume, self.weather_volume * self.game_volume)
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
            
        eff_vol = volume * self.game_volume * self.sfx_volume
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
        """Plays ultra-realistic multi-sample footsteps with round-robin variations, acoustic panning, and gear rustle."""
        self.step_counter += 1
        possible_vars = [1, 2, 3, 4]
        if self.last_step_var in possible_vars:
            possible_vars.remove(self.last_step_var)
        chosen_var = random.choice(possible_vars) if possible_vars else 1
        self.last_step_var = chosen_var

        key = f"footstep_{surface}_{chosen_var}"
        if key not in self.sounds:
            key = f"footstep_{surface}_1"
        if key not in self.sounds:
            key = f"footstep_{surface}"
        if key not in self.sounds:
            key = f"footstep_dirt_{chosen_var}"
        if key not in self.sounds:
            key = "footstep_dirt"
            
        foot_pan_offset = -0.15 if (self.step_counter % 2 == 1) else 0.15
        effective_pan = max(-1.0, min(1.0, pan + foot_pan_offset))
        jitter_vol = random.uniform(0.72, 0.85)
        self.play(key, pan=effective_pan, volume=jitter_vol)

        # Every 3 steps, trigger soft tactile leather/gear rustle
        if self.step_counter % 3 == 0:
            self.play("gear_rustle", pan=0.0, volume=0.32)

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

    # Dynamic Weather Audio (Rain, Roof Muffle, Thunder)
    def play_weather(self, weather_key, volume=None):
        """Play continuous ambient weather audio on dedicated weather channel."""
        if weather_key not in self.sounds:
            return
        if volume is not None:
            self.weather_volume = max(0.0, min(1.0, volume))
        if self.current_weather_audio != weather_key:
            self.current_weather_audio = weather_key
            sound = self.sounds[weather_key]
            eff_vol = self.weather_volume * self.game_volume
            self.weather_channel.set_volume(eff_vol, eff_vol)
            self.weather_channel.play(sound, loops=-1)

    def stop_weather(self):
        self.weather_channel.stop()
        self.current_weather_audio = None

    def play_thunder(self, close=False, pan=0.0):
        key = "thunder_close" if close else "thunder_distant"
        self.play(key, pan=pan, volume=0.95)

    # Cooking & Metallurgy Audio
    def start_meat_sizzle(self):
        if 'meat_sizzle' in self.sounds:
            eff_vol = 0.85 * self.game_volume * self.sfx_volume
            self.cooking_channel.set_volume(eff_vol, eff_vol)
            self.cooking_channel.play(self.sounds['meat_sizzle'], loops=-1)

    def stop_meat_sizzle(self):
        self.cooking_channel.stop()

    def play_metal_quench(self):
        self.play("metal_quench", pan=0.0, volume=0.92)

    # Canine Companion & Wildlife Audio
    def play_whistle(self):
        self.play("whistle", pan=0.0, volume=0.9)

    def play_dog_bark(self, pan=0.0):
        self.play("dog_bark", pan=pan, volume=0.88)

    def play_dog_whimper(self, pan=0.0):
        self.play("dog_whimper", pan=pan, volume=0.8)

    def play_animal_graze(self, pan=0.0):
        self.play("animal_graze", pan=pan, volume=0.75)

    def play_animal_alert(self, pan=0.0):
        self.play("animal_alert", pan=pan, volume=0.85)

    # Human Physiology & Family Audio
    def play_heavy_panting(self):
        self.play("heavy_panting", pan=0.0, volume=0.85)

    def play_yawn(self):
        self.play("yawn", pan=0.0, volume=0.82)

    def play_shiver(self):
        self.play("shiver", pan=0.0, volume=0.85)

    def play_baby_coo(self):
        self.play("baby_coo", pan=0.0, volume=0.9)

