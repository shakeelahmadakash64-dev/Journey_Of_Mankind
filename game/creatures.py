"""
Journey of Mankind - Prehistoric Fauna & Creature Encounters
Simulates authentic prehistoric beasts inhabiting Primordial Earth during the Pleistocene dawn of humanity:
Woolly Mammoth, Sabertooth Cat, Giant Cave Bear, Dire Hyenas, Woolly Rhinoceros, Cave Lion, Underworld Serpent, and Primordial Gazelles.
Features 3D spatial threat audio, Animal Radar Directory (Key A) with lock-on tracking, and combat hunting mechanics (Key X).
"""

import random
from core.localization import loc
from game.menu import AccessibleMenu

class Creature:
    def __init__(self, creature_id, realm_id, name_key, desc_key, max_health, attack_dmg, is_hostile, sound_type, x, y, elevation=0):
        self.creature_id = creature_id
        self.realm_id = realm_id
        self.name_key = name_key
        self.desc_key = desc_key
        self.max_health = max_health
        self.health = max_health
        self.attack_dmg = attack_dmg
        self.is_hostile = is_hostile
        self.sound_type = sound_type  # 'mammoth', 'predator', 'wolf'
        self.x = x
        self.y = y
        self.elevation = elevation
        self.is_alive = True

    @property
    def name(self):
        return loc.tr(self.name_key)

    @property
    def desc(self):
        return loc.tr(self.desc_key)

class FaunaManager:
    def __init__(self, audio=None, speech=None):
        self.audio = audio
        self.speech = speech
        self.creatures = self._init_world_fauna()

    def _init_world_fauna(self):
        """Spawns authentic prehistoric fauna across all 5 realms on the expanded 11x11 continents."""
        creatures = [
            # 1. East African Rift Valley (Cradle of Humankind)
            Creature('mammoth_cradle', 'cradle', 'creature_mammoth_name', 'creature_mammoth_desc', 220, 20, False, 'mammoth', 2, 2, elevation=0),
            Creature('sabertooth_cradle', 'cradle', 'creature_sabertooth_name', 'creature_sabertooth_desc', 85, 22, True, 'predator', -2, 3, elevation=1),
            Creature('cave_bear_cradle', 'cradle', 'creature_cave_bear_name', 'creature_cave_bear_desc', 160, 30, True, 'predator', -3, -3, elevation=-1),
            Creature('hyena_cradle', 'cradle', 'creature_hyena_name', 'creature_hyena_desc', 60, 14, True, 'wolf', 3, -2, elevation=0),
            Creature('gazelle_cradle', 'cradle', 'creature_gazelle_name', 'creature_gazelle_desc', 40, 0, False, None, 1, 1, elevation=0),

            # 2. Prehistoric Red Sea Coast & Bab-el-Mandeb
            Creature('sabertooth_coast', 'coastal', 'creature_sabertooth_name', 'creature_sabertooth_desc', 85, 22, True, 'predator', -3, 2, elevation=1),
            Creature('hyena_coast', 'coastal', 'creature_hyena_name', 'creature_hyena_desc', 60, 14, True, 'wolf', 2, -3, elevation=0),
            Creature('gazelle_coast', 'coastal', 'creature_gazelle_name', 'creature_gazelle_desc', 40, 0, False, None, 1, 3, elevation=0),
            Creature('cave_bear_coast', 'coastal', 'creature_cave_bear_name', 'creature_cave_bear_desc', 150, 28, True, 'predator', -2, -3, elevation=-1),

            # 3. Sinai Peninsula & Arabian Desert Crossroads
            Creature('sabertooth_volc', 'volcanic', 'creature_sabertooth_name', 'creature_sabertooth_desc', 90, 24, True, 'predator', 3, 2, elevation=1),
            Creature('serpent_volc', 'volcanic', 'creature_serpent_name', 'creature_serpent_desc', 75, 20, True, 'predator', -3, 1, elevation=-1),
            Creature('hyena_volc', 'volcanic', 'creature_hyena_name', 'creature_hyena_desc', 65, 15, True, 'wolf', -2, -3, elevation=0),
            Creature('gazelle_volc', 'volcanic', 'creature_gazelle_name', 'creature_gazelle_desc', 40, 0, False, None, 2, -2, elevation=0),

            # 4. Fertile Crescent & Mammoth Steppe
            Creature('mammoth_steppe', 'tundra', 'creature_mammoth_name', 'creature_mammoth_desc', 260, 24, False, 'mammoth', 0, 3, elevation=0),
            Creature('rhino_steppe', 'tundra', 'creature_rhino_name', 'creature_rhino_desc', 190, 28, True, 'mammoth', 3, -2, elevation=1),
            Creature('lion_steppe', 'tundra', 'creature_lion_name', 'creature_lion_desc', 105, 26, True, 'predator', -3, 2, elevation=1),
            Creature('hyena_steppe', 'tundra', 'creature_hyena_name', 'creature_hyena_desc', 65, 15, True, 'wolf', -2, -2, elevation=0),
            Creature('gazelle_steppe', 'tundra', 'creature_gazelle_name', 'creature_gazelle_desc', 40, 0, False, None, 2, 1, elevation=0),

            # 5. Deep Subterranean Caverns & Sacred Caves
            Creature('cave_bear_under', 'underworld', 'creature_cave_bear_name', 'creature_cave_bear_desc', 180, 32, True, 'predator', 0, -1, elevation=-1),
            Creature('serpent_under', 'underworld', 'creature_serpent_name', 'creature_serpent_desc', 85, 22, True, 'predator', -2, 2, elevation=-1),
            Creature('hyena_under', 'underworld', 'creature_hyena_name', 'creature_hyena_desc', 65, 15, True, 'wolf', 2, -2, elevation=-1),
            Creature('cave_bear_under2', 'underworld', 'creature_cave_bear_name', 'creature_cave_bear_desc', 170, 30, True, 'predator', 3, 3, elevation=-1)
        ]
        return creatures

    def get_creature_at(self, realm_id, x, y, elevation=0):
        """Returns the first live creature present at the given coordinate and elevation in the realm."""
        for c in self.creatures:
            if c.is_alive and c.realm_id == realm_id and c.x == x and c.y == y and c.elevation == elevation:
                return c
        return None

    def check_nearby_cues(self, realm_id, player_x, player_y, elevation=0):
        """Play spatial sound warnings if a creature is adjacent to the player."""
        if not self.audio:
            return None

        for c in self.creatures:
            if not c.is_alive or c.realm_id != realm_id or c.elevation != elevation:
                continue
            dx = c.x - player_x
            dy = c.y - player_y
            dist = abs(dx) + abs(dy)
            if dist <= 2:
                pan = -0.7 if dx < 0 else (0.7 if dx > 0 else 0.0)
                if c.sound_type == 'mammoth':
                    self.audio.play_mammoth_trumpet(pan=pan)
                elif c.sound_type == 'predator':
                    self.audio.play_predator_growl(pan=pan)
                elif c.sound_type == 'wolf':
                    self.audio.play_wolf_howl(pan=pan)
                return c
        return None

    def open_fauna_tracking_menu(self, player_x, player_y, current_realm, tracker, screen=None):
        """Called on Key A: Opens Prehistoric Animal Radar directory.
        Allows player to browse all live beasts in current realm and lock tracking on Enter."""
        live_beasts = [c for c in self.creatures if c.realm_id == current_realm and c.is_alive]

        if not live_beasts:
            msg = loc.tr('fauna_no_beasts')
            if self.speech:
                self.speech.speak(msg)
            if self.audio:
                self.audio.play_error()
            return

        # Sort beasts by distance from player
        def beast_distance(c):
            return abs(c.x - player_x) + abs(c.y - player_y)

        live_beasts.sort(key=beast_distance)

        options = []
        for c in live_beasts:
            dx = c.x - player_x
            dy = c.y - player_y
            dist = abs(dx) + abs(dy)
            dir_name = self._get_direction_name(dx, dy)
            danger_tag = loc.tr('fauna_hostile_tag') if c.is_hostile else loc.tr('fauna_herbivore_tag')
            
            def make_selector(target_creature, d_val, d_name):
                def select_action():
                    tracker.set_creature_target(target_creature, d_val, d_name)
                    msg = loc.tr('fauna_locked', name=target_creature.name, dist=d_val, dir=d_name)
                    if self.speech:
                        self.speech.speak(msg)
                    return "LOCKED"
                return select_action

            label = f"{c.name} - {dist} steps {dir_name} {danger_tag}"
            options.append((label, make_selector(c, dist, dir_name)))

        options.append((loc.tr('back'), lambda: "BACK"))

        menu = AccessibleMenu(loc.tr('fauna_radar_title'), options, self.audio, self.speech)
        menu.run(screen)

    def attack_creature(self, character, creature, tracker=None):
        """Player engages creature with equipped weapon (Key X)."""
        if not creature or not creature.is_alive:
            if self.speech:
                self.speech.speak(loc.tr('no_creature_near'))
            return

        weapon_id = getattr(character, 'equipped_weapon', 'fists')
        weapon_dmg = getattr(character, 'weapon_damage', 10)
        weapon_name = getattr(character, 'equipped_weapon_name', 'Hands/Fists')

        if self.audio:
            self.audio.play_voice_attack()
            self.audio.play_weapon_swing()

        # Inflict player damage
        creature.health -= weapon_dmg
        if self.audio:
            self.audio.play_weapon_hit()

        msg = loc.tr('player_attack_hit', weapon=weapon_name, name=creature.name, dmg=weapon_dmg)
        if self.speech:
            self.speech.speak(msg)

        # Companion pet assist in combat
        if getattr(character, 'pet', None):
            pet_dmg = 15
            creature.health -= pet_dmg
            if self.audio:
                self.audio.play_wolf_howl()
            pet_name = character.pet.get('name', 'Hunting Companion')
            pet_msg = f"Your {pet_name} leaps into combat dealing {pet_dmg} companion damage!" if loc.lang == 'en' else f"Aap ke {pet_name} ne hamla kar ke mazeed {pet_dmg} damage diya!"
            if self.speech:
                self.speech.speak(pet_msg)

        # Milestone: hunt
        qs = getattr(character, 'quest_system', None)
        if qs:
            qs.check_milestone(character, 'hunt')

        # Check if creature died
        if creature.health <= 0:
            creature.is_alive = False
            # Reward player with meat and bones
            character.add_item('meat', loc.tr('item_meat'), 2)
            character.add_item('animal_bone', loc.tr('item_animal_bone'), 1)
            slain_msg = loc.tr('creature_slain', name=creature.name)
            if self.speech:
                self.speech.speak(slain_msg)
            if self.audio:
                self.audio.play("menu_select")
            if tracker and tracker.active_target and tracker.active_target[4] == 'creature':
                if tracker.active_target[5] == creature:
                    tracker.active_target = None
            return

        # Hostile creature counter-attacks unless repelled by a fire torch
        if creature.is_hostile:
            has_torch = any(i['id'] == 'torch' for i in character.inventory)
            if has_torch and random.random() < 0.6:
                torch_repel = f"The {creature.name} recoils in terror from your blazing fire torch!"
                if self.speech:
                    self.speech.speak(torch_repel)
            else:
                character.health = max(0.0, character.health - creature.attack_dmg)
                if self.audio:
                    self.audio.play_predator_growl()
                    self.audio.play_voice_hurt()
                    self.audio.play_heartbeat()
                dmg_msg = loc.tr('creature_attacked_player', name=creature.name, dmg=creature.attack_dmg)
                if self.speech:
                    self.speech.speak(dmg_msg)
                if character.health <= 0:
                    character.die(loc.tr('death_reason_predator'))

    def _get_direction_name(self, dx, dy):
        """Returns human-friendly cardinal/diagonal direction string."""
        ns = ""
        ew = ""
        if dy > 0:
            ns = "North" if loc.lang == 'en' else "Shumal"
        elif dy < 0:
            ns = "South" if loc.lang == 'en' else "Janoob"

        if dx > 0:
            ew = "East" if loc.lang == 'en' else "Mashriq"
        elif dx < 0:
            ew = "West" if loc.lang == 'en' else "Maghrib"

        if ns and ew:
            return f"{ns}-{ew}"
        return ns or ew or ("Here" if loc.lang == 'en' else "Yahan")
