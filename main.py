"""
Journey of Mankind (Safar-e-Insaan)
An Accessible Audio Survival & Evolution Game for Blind and Visually Impaired Gamers.
Features:
- Primary Language: English (Default) | Secondary Language: Urdu
- Primordial Earth World Map (25 Contiguous Regions, 5x5 Grid)
- 3D Positional Audio & Screen Reader Speech (NVDA / JAWS / SAPI5)
- Vertical Elevation: Page Up (Ascend) & Page Down (Descend)
- Direction Navigation: Arrow Keys (Walk & Face), [ and ] (Turn in place), D (Compass)
- Prehistoric Creatures: Woolly Mammoth, Sabertooth Cat, Cave Bear, Hyenas, Gazelles
- Weapon Crafting: Spears, Obsidian Daggers, Fire Torches, Bone Clubs, Slings
- In-Game Interactive Audio Guide (G / F1) with Step-by-Step Crafting Tutorial
"""

import sys
import os
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

import pygame
from core.audio_manager import AudioManager
from core.speech_manager import SpeechManager
from core.database import Database
from core.localization import loc
from game.character import Character
from game.world import World
from game.prologue import Prologue
from game.crafting import CraftingSystem
from game.creatures import FaunaManager
from game.guide import GuideSystem
from game.bag import BagSystem
from game.tracker import ItemTracker
from game.quests import QuestSystem
from game.menu import AccessibleMenu, prompt_text_input
from core.updater import open_updater_menu

class JourneyOfMankindGame:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(loc.tr('game_title'))
        self.screen = pygame.display.set_mode((760, 540))
        self.font = pygame.font.SysPlusFont("Arial", 28) if hasattr(pygame.font, 'SysPlusFont') else pygame.font.SysFont("Arial", 28)
        
        sounds_dir = os.path.join(SCRIPT_DIR, 'sounds')
        self.audio = AudioManager(sounds_dir)
        self.speech = SpeechManager()
        self.db = Database()
        self.quest_system = QuestSystem(audio=self.audio, speech=self.speech)
        self.world = World(audio=self.audio, speech=self.speech, quest_system=self.quest_system)
        self.crafting = CraftingSystem(audio=self.audio, speech=self.speech, quest_system=self.quest_system)
        self.fauna = FaunaManager(audio=self.audio, speech=self.speech)
        self.guide = GuideSystem(audio=self.audio, speech=self.speech)
        self.bag = BagSystem(audio=self.audio, speech=self.speech)
        self.tracker = ItemTracker(audio=self.audio, speech=self.speech)
        
        self.current_user = None
        self.character = None
        self.running = True

        # Cyclic Scanner & Lock-On Tracking State
        self.item_scan_list = []
        self.item_scan_index = -1
        self.animal_scan_list = []
        self.animal_scan_index = -1
        self.last_scan_mode = None  # 'item' or 'animal'
        self.last_scan_time = 0.0
        self.last_scan_target = None

    def render_screen(self, title, lines):
        """High-contrast visual display for low-vision users or sighted observers."""
        self.screen.fill((12, 18, 30))
        title_surf = self.font.render(title, True, (255, 215, 0))
        self.screen.blit(title_surf, (30, 20))
        
        y = 70
        small_font = pygame.font.SysFont("Arial", 18)
        for line in lines:
            line_surf = small_font.render(line, True, (225, 225, 225))
            self.screen.blit(line_surf, (30, y))
            y += 26
        pygame.display.flip()

    def run_main_menu(self):
        """Displays and runs the localized main menu."""
        while self.running:
            lang_names = {
                'en': "English",
                'ur': "Roman Urdu",
                'es': "Español",
                'fr': "Français",
                'ar': "Arabic (Al-Arabiya)",
                'hi': "Hindi (Hindustani)"
            }
            cur_lang_str = lang_names.get(loc.lang, loc.lang.upper())
            self.render_screen(loc.tr('game_title'), [
                f"1. {loc.tr('menu_start')}",
                f"2. {loc.tr('menu_new_account')}",
                f"3. {loc.tr('menu_select_account')}",
                f"4. {loc.tr('menu_language')} [{cur_lang_str}]",
                f"5. {loc.tr('menu_updater')}",
                f"6. {loc.tr('menu_help')}",
                f"7. {loc.tr('menu_quit')}",
                "",
                f"{loc.tr('menu_current_account')}: {self.current_user if self.current_user else loc.tr('none')}"
            ])
            
            options = [
                (loc.tr('menu_start'), self.action_start_game),
                (loc.tr('menu_new_account'), self.action_create_account),
                (loc.tr('menu_select_account'), self.action_select_account),
                (f"{loc.tr('menu_language')} ({cur_lang_str})", self.action_toggle_language),
                (loc.tr('menu_updater'), lambda: open_updater_menu(self.screen, self.audio, self.speech)),
                (loc.tr('menu_help'), self.action_show_help),
                (loc.tr('menu_quit'), self.action_quit)
            ]
            
            menu = AccessibleMenu(loc.tr('menu_title'), options, self.audio, self.speech)
            result = menu.run(self.screen)
            if result == "QUIT" or not self.running:
                break

    def action_toggle_language(self):
        loc.toggle_language()
        msg = loc.tr('lang_switched')
        if self.speech:
            self.speech.speak(msg)
        if self.audio:
            self.audio.play("menu_select")
        pygame.display.set_caption(loc.tr('game_title'))

    def action_create_account(self):
        self.render_screen(loc.tr('menu_new_account'), [loc.tr('enter_name_prompt')])
        name = prompt_text_input(loc.tr('enter_name_prompt'), self.audio, self.speech)
        if not name:
            return
        
        ok, _ = self.db.register_player(name)
        if ok:
            msg = loc.tr('account_created', name=name.capitalize())
            if self.speech:
                self.speech.speak(msg)
            if self.audio:
                self.audio.play("menu_select")
            self.current_user = name.capitalize()
            self.speech.speak(loc.tr('account_selected', name=self.current_user))
        else:
            msg = loc.tr('account_exists', name=name.capitalize())
            if self.speech:
                self.speech.speak(msg)
            if self.audio:
                self.audio.play_error()

    def action_select_account(self):
        players = self.db.list_players()
        if not players:
            msg = loc.tr('no_accounts')
            if self.speech:
                self.speech.speak(msg)
            if self.audio:
                self.audio.play_error()
            return

        options = []
        for p in players:
            uname = p[0]
            era = p[1]
            def make_selector(username):
                return lambda: self._select_user(username)
            options.append((f"{uname} (Era {era})", make_selector(uname)))
        
        menu = AccessibleMenu(loc.tr('menu_select_account'), options, self.audio, self.speech)
        menu.run(self.screen)

    def _select_user(self, username):
        self.current_user = username
        msg = loc.tr('account_selected', name=username)
        if self.speech:
            self.speech.speak(msg)
        return "SELECTED"

    def action_show_help(self):
        self.guide.open_guide_menu(self.screen)

    def action_start_game(self):
        if not self.current_user:
            players = self.db.list_players()
            if not players:
                self.action_create_account()
                if not self.current_user:
                    return
            else:
                self.current_user = players[0][0]
                if self.speech:
                    self.speech.speak(loc.tr('account_selected', name=self.current_user))

        player_data = self.db.get_player_data(self.current_user)
        if not player_data:
            return

        if not player_data['prologue_completed']:
            prologue = Prologue(self.audio, self.speech)
            prologue.run()
            self.db.save_player_data(
                self.current_user,
                player_data['stats'],
                player_data['inventory'],
                prologue_completed=True
            )
            player_data['prologue_completed'] = True

        self.character = Character(
            self.current_user,
            stats=player_data['stats'],
            inventory=player_data['inventory'],
            audio=self.audio,
            speech=self.speech
        )
        self.character.quest_system = self.quest_system

        self.run_in_game_loop()

    def run_in_game_loop(self):
        """Primary gameplay loop wrapped with full runtime error recovery."""
        try:
            self._execute_in_game_loop()
        except Exception as e:
            import traceback
            err_msg = traceback.format_exc()
            print(f"[Error in game loop]: {err_msg}")
            log_path = os.path.join(SCRIPT_DIR, "error.log")
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(f"\n--- {time.ctime()} ---\n{err_msg}\n")
            if self.speech:
                self.speech.speak("Runtime error caught and safely recovered. Resuming.")
            self.running = True

    def handle_character_respawn(self):
        """Revives fallen character with 100% vitals at Central Sacred Hearth (0, 0)."""
        self.character.revive()
        cur_tile = self.world.get_tile(0, 0)
        t_name = cur_tile.name if cur_tile else "Sacred Hearth"
        if self.speech:
            self.speech.speak(f"Location: {t_name} (0, 0).")
        self._save_game()

    def action_scan_next_item(self):
        """Called on key 'M': Cycles through all ground resources and water sources in the realm.
        Calculates distance, compass heading, plays stereo pan sonar ping, and speaks the item info."""
        px = self.character.pos_x
        py = self.character.pos_y

        items = []
        for (tx, ty), tile in self.world.grid.items():
            if tile.is_shelter:
                shelter_name = loc.tr('shelter_name')
                items.append({
                    'x': tx,
                    'y': ty,
                    'id': 'shelter',
                    'name': shelter_name,
                    'qty': 1,
                    'is_water': False,
                    'is_shelter': True
                })
            if tile.resources:
                for item_id, tr_key, qty in tile.resources:
                    item_name = loc.tr(tr_key)
                    items.append({
                        'x': tx,
                        'y': ty,
                        'id': item_id,
                        'name': item_name,
                        'qty': qty,
                        'is_water': False,
                        'is_shelter': False
                    })
            if tile.can_drink:
                water_name = "Freshwater Drinking Source" if loc.lang == 'en' else "Meethay Paani ka Chashma"
                items.append({
                    'x': tx,
                    'y': ty,
                    'id': 'water',
                    'name': water_name,
                    'qty': 1,
                    'is_water': True,
                    'is_shelter': False
                })

        if not items:
            msg = loc.tr('item_scan_none')
            if self.speech:
                self.speech.speak(msg)
            if self.audio:
                self.audio.play_error()
            return

        # Sort items primarily by distance from player
        items.sort(key=lambda item: abs(item['x'] - px) + abs(item['y'] - py))

        now = time.time()
        if self.last_scan_mode != 'item' or (now - self.last_scan_time > 20.0) or not self.item_scan_list:
            self.item_scan_list = items
            self.item_scan_index = 0
        else:
            self.item_scan_list = items
            self.item_scan_index = (self.item_scan_index + 1) % len(self.item_scan_list)

        self.last_scan_mode = 'item'
        self.last_scan_time = now

        target = self.item_scan_list[self.item_scan_index]
        self.last_scan_target = target

        dx = target['x'] - px
        dy = target['y'] - py
        dist = abs(dx) + abs(dy)
        dir_name = self.tracker._get_direction_name(dx, dy)
        pan = self.tracker._calc_pan(dx, dy, self.character.facing)

        if self.audio:
            self.audio.play_sonar_beep(pan=pan)

        if target.get('is_shelter'):
            msg = loc.tr('shelter_scan_cycle', dist=dist, dir=dir_name)
        elif target['is_water']:
            msg = loc.tr('item_scan_water_cycle', dist=dist, dir=dir_name)
        else:
            msg = loc.tr('item_scan_cycle', name=target['name'], qty=target['qty'], dist=dist, dir=dir_name)

        if self.speech:
            self.speech.speak(msg)

    def action_scan_next_animal(self):
        """Called on key 'A': Cycles through all live prehistoric beasts in the current realm.
        Calculates distance, compass heading, plays directional animal cue/ping, and speaks beast info."""
        px = self.character.pos_x
        py = self.character.pos_y

        live_beasts = [c for c in self.fauna.creatures if c.realm_id == self.world.current_realm_id and c.is_alive]
        if not live_beasts:
            msg = loc.tr('fauna_no_beasts')
            if self.speech:
                self.speech.speak(msg)
            if self.audio:
                self.audio.play_error()
            return

        # Sort beasts by distance from player
        live_beasts.sort(key=lambda c: abs(c.x - px) + abs(c.y - py))

        now = time.time()
        if self.last_scan_mode != 'animal' or (now - self.last_scan_time > 20.0) or not self.animal_scan_list:
            self.animal_scan_list = live_beasts
            self.animal_scan_index = 0
        else:
            self.animal_scan_list = live_beasts
            self.animal_scan_index = (self.animal_scan_index + 1) % len(self.animal_scan_list)

        self.last_scan_mode = 'animal'
        self.last_scan_time = now

        creature = self.animal_scan_list[self.animal_scan_index]
        self.last_scan_target = creature

        dx = creature.x - px
        dy = creature.y - py
        dist = abs(dx) + abs(dy)
        dir_name = self.tracker._get_direction_name(dx, dy)
        pan = self.tracker._calc_pan(dx, dy, self.character.facing)

        if self.audio:
            if creature.sound_type == 'mammoth':
                self.audio.play_mammoth_trumpet(pan=pan)
            elif creature.sound_type == 'predator':
                self.audio.play_predator_growl(pan=pan)
            elif creature.sound_type == 'wolf':
                self.audio.play_wolf_howl(pan=pan)
            else:
                self.audio.play_sonar_beep(pan=pan)

        danger_tag = loc.tr('fauna_hostile_tag') if creature.is_hostile else loc.tr('fauna_herbivore_tag')
        msg = loc.tr('animal_scan_cycle', name=creature.name, tag=danger_tag, dist=dist, dir=dir_name)
        if self.speech:
            self.speech.speak(msg)

    def action_handle_enter(self, is_shift=False):
        """Handles Enter key:
        - If Shift+Enter:
          * If inside shelter: Exits shelter into wilderness!
          * If standing on shelter tile: Enters shelter!
          * Else: Crosses realm gateway or opens travel menu.
        - Else if active scan target (A or M pressed within 15s): Lock tracking onto that target!
        - Else: Interact with current tile (pick up ground items into bag, or drink water). If empty, speaks tile_interact_empty."""
        if is_shift:
            if getattr(self.character, 'is_inside_shelter', False):
                if getattr(self.character, 'shelter_x', 0) == 0 and getattr(self.character, 'shelter_y', -1) == -2:
                    self.character.exit_shelter(realm_id=self.world.current_realm_id)
                else:
                    msg = loc.tr('shelter_must_walk_to_door')
                    if self.speech:
                        self.speech.speak(msg)
                    if self.audio:
                        self.audio.play_error()
                return

            cur_tile = self.world.get_tile(self.character.pos_x, self.character.pos_y)
            if cur_tile and cur_tile.is_shelter:
                self.character.enter_shelter(self.quest_system)
                return

            self.world.handle_realm_travel(self.character, self.screen)
            return

        now = time.time()
        is_scan_active = (self.last_scan_mode is not None) and (now - self.last_scan_time <= 15.0) and (self.last_scan_target is not None)

        if is_scan_active:
            if self.last_scan_mode == 'animal':
                creature = self.last_scan_target
                if not getattr(creature, 'is_alive', False):
                    self.last_scan_mode = None
                    self.last_scan_target = None
                else:
                    dx = creature.x - self.character.pos_x
                    dy = creature.y - self.character.pos_y
                    dist = abs(dx) + abs(dy)
                    dir_name = self.tracker._get_direction_name(dx, dy)
                    self.tracker.set_creature_target(creature, dist, dir_name)
                    msg = loc.tr('animal_scan_locked', name=creature.name, dist=dist, dir=dir_name)
                    if self.speech:
                        self.speech.speak(msg)
                    if self.audio:
                        self.audio.play_item_found()
                    self.last_scan_mode = None
                    self.last_scan_target = None
                    return

            elif self.last_scan_mode == 'item':
                item_info = self.last_scan_target
                tx, ty = item_info['x'], item_info['y']
                dx = tx - self.character.pos_x
                dy = ty - self.character.pos_y
                dist = abs(dx) + abs(dy)
                if dist == 0:
                    self.last_scan_mode = None
                    self.last_scan_target = None
                    if item_info.get('is_shelter'):
                        self.character.enter_shelter(self.quest_system)
                    else:
                        self.world.interact_current_tile(self.character)
                    return

                dir_name = self.tracker._get_direction_name(dx, dy)
                target_name = item_info['name']
                self.tracker.active_target = (tx, ty, target_name, item_info['id'], 'item', None)
                if self.audio:
                    self.audio.play_item_found()
                msg = loc.tr('item_scan_locked', name=target_name, dist=dist, dir=dir_name)
                if self.speech:
                    self.speech.speak(msg)
                self.last_scan_mode = None
                self.last_scan_target = None
                return

        # Not locking from recent scan: interact with current tile
        tile = self.world.get_tile(self.character.pos_x, self.character.pos_y)
        if tile and (tile.resources or tile.can_drink):
            self.world.interact_current_tile(self.character)
        else:
            if self.speech:
                self.speech.speak(loc.tr('tile_interact_empty'))
            if self.audio:
                self.audio.play("footstep_dirt")

    def action_report_compass(self):
        """Speaks Real Compass Heading (with exact degrees), GPS coordinates, elevation, region, and surrounding 4 tiles."""
        if getattr(self.character, 'is_inside_shelter', False):
            sx = getattr(self.character, 'shelter_x', 0)
            sy = getattr(self.character, 'shelter_y', -1)
            facing_dir = loc.tr(self.character.facing.lower())
            deg = self.character.facing_degrees
            cur_desc = self.character.get_shelter_tile_desc(sx, sy)
            n_desc = self.character.get_shelter_tile_desc(sx, sy + 1)
            s_desc = self.character.get_shelter_tile_desc(sx, sy - 1)
            e_desc = self.character.get_shelter_tile_desc(sx + 1, sy)
            w_desc = self.character.get_shelter_tile_desc(sx - 1, sy)
            if self.audio:
                self.audio.play_turn()
            report_msg = (
                f"{cur_desc}. Facing: {facing_dir} ({deg} deg). "
                f"North: {n_desc}. South: {s_desc}. East: {e_desc}. West: {w_desc}."
            )
            if self.speech:
                self.speech.speak(report_msg)
            return report_msg

        x = self.character.pos_x
        y = self.character.pos_y
        elev_str = self.world.get_elevation_name(self.character.elevation)
        cur_tile = self.world.get_tile(x, y)
        area_name = cur_tile.name if cur_tile else "Wilderness"
        realm_name = self.world.get_realm_display_name(self.world.current_realm_id)

        facing_dir = loc.tr(self.character.facing.lower())
        deg = self.character.facing_degrees

        tile_n = self.world.get_tile(x, y + 1)
        tile_s = self.world.get_tile(x, y - 1)
        tile_e = self.world.get_tile(x + 1, y)
        tile_w = self.world.get_tile(x - 1, y)

        north_str = tile_n.name if tile_n else ("Border / Edge" if loc.lang == 'en' else "Map ka Kinara")
        south_str = tile_s.name if tile_s else ("Border / Edge" if loc.lang == 'en' else "Map ka Kinara")
        east_str = tile_e.name if tile_e else ("Border / Edge" if loc.lang == 'en' else "Map ka Kinara")
        west_str = tile_w.name if tile_w else ("Border / Edge" if loc.lang == 'en' else "Map ka Kinara")

        if self.audio:
            self.audio.play_turn()

        report_msg = (
            f"{loc.tr('compass_title')}. "
            f"{loc.tr('compass_coords', x=x, y=y, elev=elev_str)} "
            f"{loc.tr('compass_region', area=area_name, realm=realm_name)} "
            f"{loc.tr('compass_heading', facing=facing_dir, deg=deg)} "
            f"{loc.tr('compass_surroundings', north=north_str, south=south_str, east=east_str, west=west_str)}"
        )

        if self.tracker.active_target:
            tx, ty, t_name, _, t_type, extra = self.tracker.active_target
            if t_type == 'creature' and extra:
                tx, ty = extra.x, extra.y
            dist = abs(tx - x) + abs(ty - y)
            d_str = self.tracker._get_direction_name(tx - x, ty - y)
            report_msg += f" {loc.tr('compass_target_active', name=t_name, dist=dist, dir=d_str)}"
        else:
            report_msg += f" {loc.tr('compass_target_none')}"

        if cur_tile and cur_tile.travel_point_to:
            dest_name = self.world.get_realm_display_name(cur_tile.travel_point_to)
            portal_hint = f" Standing at Border Gateway to {dest_name}. Press Shift + Enter to cross." if loc.lang == 'en' else f" {dest_name} ke Travel Gateway par kharay hain. Shift + Enter dabayein."
            report_msg += portal_hint

        if self.speech:
            self.speech.speak(report_msg)
        return report_msg

    def action_use_weapon(self):
        """Called on Spacebar and Key X: Uses the equipped weapon or item currently held in hand.
        If a prehistoric creature is nearby (on same tile or adjacent within 2 steps), attacks it.
        If no creature is within range, swings the weapon into the air with audio and spoken feedback."""
        creature = self.fauna.get_creature_at(self.world.current_realm_id, self.character.pos_x, self.character.pos_y, self.character.elevation)
        if not creature:
            creature = self.fauna.check_nearby_cues(self.world.current_realm_id, self.character.pos_x, self.character.pos_y, self.character.elevation)

        if creature and creature.is_alive:
            self.fauna.attack_creature(self.character, creature, self.tracker)
        else:
            w_name = getattr(self.character, 'equipped_weapon_name', 'Hands/Fists')
            w_dmg = getattr(self.character, 'weapon_damage', 10)
            if self.audio:
                self.audio.play_weapon_swing()
            msg = loc.tr('weapon_swung_empty', weapon=w_name, dmg=w_dmg)
            if self.speech:
                self.speech.speak(msg)

    def action_tame_nearby_creature(self):
        """Called on Key T: Tames a nearby wild animal using raw meat or berries."""
        creature = self.fauna.get_creature_at(self.world.current_realm_id, self.character.pos_x, self.character.pos_y, self.character.elevation)
        if not creature:
            creature = self.fauna.check_nearby_cues(self.world.current_realm_id, self.character.pos_x, self.character.pos_y, self.character.elevation)
        if not creature:
            px = self.character.pos_x
            py = self.character.pos_y
            for c in self.fauna.creatures:
                if c.realm_id == self.world.current_realm_id and c.is_alive:
                    if abs(c.x - px) + abs(c.y - py) <= 2:
                        creature = c
                        break
        if creature and creature.is_alive:
            self.character.tame_creature(creature, self.quest_system)
        else:
            msg = loc.tr('tame_no_beast')
            if self.speech:
                self.speech.speak(msg)
            if self.audio:
                self.audio.play_error()

    def action_handle_shelter(self):
        """Called on Key B: Rests in shelter if present, or builds a Lean-to shelter."""
        tile = self.world.get_tile(self.character.pos_x, self.character.pos_y)
        if tile and tile.is_shelter:
            self.world.rest_in_shelter(self.character, self.quest_system)
        else:
            self.world.build_shelter_at(self.character, self.quest_system)

    def action_open_tab_menu(self):
        """Called on Key TAB: In-game Quick Hub containing Quests & Epoch Journal, Language Switcher, Journey Diary, and Time/Weather."""
        options = [
            (loc.tr('tab_menu_quests'), self._open_quests_menu),
            (loc.tr('tab_menu_lang'), self._open_language_menu),
            (loc.tr('tab_menu_diary'), lambda: self.quest_system.read_diary(self.character, self.screen)),
            (loc.tr('tab_menu_updater'), lambda: open_updater_menu(self.screen, self.audio, self.speech)),
            (loc.tr('tab_menu_weather'), lambda: self.world.report_time_and_weather(self.character)),
            (loc.tr('tab_menu_resume'), lambda: "RESUME")
        ]
        menu = AccessibleMenu(loc.tr('tab_menu_title'), options, self.audio, self.speech)
        menu.run(self.screen)

    def _open_quests_menu(self):
        """Displays interactive Epoch progression and active/completed milestones."""
        era_num = self.quest_system.current_era
        era_name = self.quest_system.get_era_name(era_num)
        era_desc = self.quest_system.get_era_desc(era_num)

        options = []
        summary_label = f"[{era_name}] - {era_desc}"
        def make_era_reader(txt=summary_label):
            return lambda: self.speech.speak(txt) if self.speech else None
        options.append((summary_label, make_era_reader()))

        current_quests = [q for q in self.quest_system.quests.values() if q.era == era_num]
        for q in current_quests:
            is_done = (q.quest_id in self.quest_system.completed_quests)
            tag = "[COMPLETED / MUKAMMAL]" if is_done else "[ACTIVE GOAL / MAQSAD]"
            label = f"{tag} {q.title} - {q.desc}"
            def make_quest_reader(desc_text=f"{q.title}: {q.desc}. Status: {tag}"):
                return lambda: self.speech.speak(desc_text) if self.speech else None
            options.append((label, make_quest_reader()))

        options.append((loc.tr('back'), lambda: "BACK"))
        menu = AccessibleMenu(f"{loc.tr('tab_menu_quests')} - {era_name}", options, self.audio, self.speech)
        menu.run(self.screen)

    def _open_language_menu(self):
        """Allows instant live switching between all 6 supported languages in-game."""
        lang_list = [
            ('en', "1. English (Primary International)"),
            ('ur', "2. Roman Urdu (Asaan Urdu)"),
            ('es', "3. Español (Spanish)"),
            ('fr', "4. Français (French)"),
            ('ar', "5. Al-Arabiya (Arabic transliterated)"),
            ('hi', "6. Hindustani (Hindi transliterated)")
        ]
        options = []
        for code, display in lang_list:
            is_cur = (loc.lang == code)
            lbl = f"{display} [Active]" if is_cur else display
            def make_lang_setter(c=code):
                def set_lang_action():
                    loc.set_language(c)
                    msg = loc.tr('lang_switched')
                    if self.speech:
                        self.speech.speak(msg)
                    if self.audio:
                        self.audio.play("menu_select")
                    pygame.display.set_caption(loc.tr('game_title'))
                    return "CHANGED"
                return set_lang_action
            options.append((lbl, make_lang_setter()))

        options.append((loc.tr('back'), lambda: "BACK"))
        menu = AccessibleMenu(loc.tr('tab_menu_lang'), options, self.audio, self.speech)
        menu.run(self.screen)

    def _execute_in_game_loop(self):
        """Primary gameplay loop on Primordial Earth with Elevation, Creatures, and Crafting."""
        self.audio.set_realm_ambience(self.world.current_realm_id, volume=0.35)
        
        current_tile = self.world.get_tile(self.character.pos_x, self.character.pos_y)
        tile_name = current_tile.name if current_tile else "Primordial Earth"
        elev_str = self.world.get_elevation_name(self.character.elevation)
        self.speech.speak(f"{tile_name} ({elev_str}). {current_tile.desc if current_tile else ''}")
        
        clock = pygame.time.Clock()
        last_vital_tick = time.time()
        last_audio_cue_tick = time.time()
        last_tracker_tick = time.time()
        in_game = True

        while in_game:
            clock.tick(30)
            now = time.time()

            # Life / Respawn check
            if not self.character.is_alive or self.character.health <= 0.0:
                self.handle_character_respawn()

            # Vitals and World Time progression tick (every 1 second)
            if now - last_vital_tick >= 1.0:
                elapsed = now - last_vital_tick
                last_vital_tick = now
                self.character.update_vitals(elapsed)
                self.world.update_time(elapsed)

            # Audio cues & nearby creature sounds tick
            if now - last_audio_cue_tick >= 5.0:
                last_audio_cue_tick = now
                self.character.check_audio_cues()
                self.fauna.check_nearby_cues(self.world.current_realm_id, self.character.pos_x, self.character.pos_y, self.character.elevation)

            # Sonar tracker ping tick (every 2.0 seconds)
            if now - last_tracker_tick >= 2.0:
                last_tracker_tick = now
                self.tracker.update_ping(self.world, self.character)

            # High-contrast screen render
            cur_tile = self.world.get_tile(self.character.pos_x, self.character.pos_y)
            elev_str = self.world.get_elevation_name(self.character.elevation)
            creature_here = self.fauna.get_creature_at(self.world.current_realm_id, self.character.pos_x, self.character.pos_y, self.character.elevation)
            creature_str = f"Beast Nearby: {creature_here.name} (HP: {creature_here.health})" if creature_here else "Wild Area (Clear)"
            
            pet_str = f" | Companion: {self.character.pet['name']}" if getattr(self.character, 'pet', None) else ""
            era_str = self.quest_system.get_era_name()
            hour, phase, _ = self.world.get_time_of_day()
            weather_str = self.world.get_weather_name()

            portal_str = f" | [PORTAL: {self.world.get_realm_display_name(cur_tile.travel_point_to)} - Shift+Enter]" if (cur_tile and cur_tile.travel_point_to) else ""
            shelter_status = " [SHELTERED - Shift+Enter to Exit]" if getattr(self.character, 'is_inside_shelter', False) else ""
            self.render_screen(f"{loc.tr('game_title')} - {self.current_user} [{era_str}]{shelter_status}", [
                f"Realm: {self.world.current_realm_id.upper()} | Area: {cur_tile.name if cur_tile else 'Wilderness'} ({self.character.pos_x}, {self.character.pos_y}) | Elevation: {elev_str}{portal_str}",
                f"Facing: {self.character.facing} ({self.character.facing_degrees}°) | Time: {hour:02d}:00 ({phase}) | Weather: {weather_str}",
                f"Health: {int(self.character.health)}% | Hunger: {int(self.character.hunger)}% | Thirst: {int(self.character.thirst)}% | Stamina: {int(self.character.stamina)}%{pet_str}",
                f"Creature: {creature_str}",
                "[Arrows]=Walk | [Shift+Arrows]=Turn Face | [C/D]=Compass & GPS | [N]=Time/Weather",
                "[Shift+Page Up/Down]=BG Vol | [Home/End]=Game Vol | [Shift+C/F]=Campfire",
                "[Space]=Attack/Use | [Enter]=Lock/Pick | [Shift+Enter]=Shelter In/Out | [B]=Shelter",
                "[Tab]=Quick Hub (Quests & Lang) | [J]=Diary | [I]=Satchel Bag (Textbooks) | [1]=Eat",
                "[M]=Cycle Items & Shelters | [A]=Cycle Animals | [K]=Travel Gateways | [O]=Target Status"
            ])

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._save_game()
                    self.running = False
                    in_game = False

                elif event.type == pygame.KEYDOWN:
                    mods = pygame.key.get_mods()
                    is_shift = bool(mods & pygame.KMOD_SHIFT)

                    # If inside spacious shelter: allow free exploration of interior!
                    if getattr(self.character, 'is_inside_shelter', False):
                        if event.key == pygame.K_UP:
                            if is_shift:
                                self.character.set_facing('North')
                            else:
                                self.character.facing = 'North'
                                self.character.move_inside_shelter(0, 1, realm_id=self.world.current_realm_id)
                        elif event.key == pygame.K_DOWN:
                            if is_shift:
                                self.character.set_facing('South')
                            else:
                                self.character.facing = 'South'
                                self.character.move_inside_shelter(0, -1, realm_id=self.world.current_realm_id)
                        elif event.key == pygame.K_RIGHT:
                            if is_shift:
                                self.character.set_facing('East')
                            else:
                                self.character.facing = 'East'
                                self.character.move_inside_shelter(1, 0, realm_id=self.world.current_realm_id)
                        elif event.key == pygame.K_LEFT:
                            if is_shift:
                                self.character.set_facing('West')
                            else:
                                self.character.facing = 'West'
                                self.character.move_inside_shelter(-1, 0, realm_id=self.world.current_realm_id)
                        elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                            self.action_handle_enter(is_shift)
                        elif event.key in (pygame.K_c, pygame.K_d):
                            self.action_report_compass()
                        elif event.key == pygame.K_TAB:
                            self.action_open_tab_menu()
                        elif event.key == pygame.K_i:
                            self.bag.open_bag(self.character, self.screen)
                        elif event.key == pygame.K_h:
                            self.character.report_health()
                        elif event.key == pygame.K_j:
                            self.character.report_hunger()
                        elif event.key == pygame.K_u:
                            self.character.report_thirst()
                        elif event.key == pygame.K_y:
                            self.character.report_stamina()
                        elif event.key == pygame.K_b:
                            self.character.stamina = min(100.0, self.character.stamina + 40.0)
                            self.character.health = min(100.0, self.character.health + 20.0)
                            self.character.temperature = 37.0
                            if self.audio: self.audio.play("menu_select")
                            if self.speech: self.speech.speak(loc.tr('shelter_rested'))
                        continue

                    # Directional Movement & In-Place Facing
                    moved = False
                    if event.key == pygame.K_UP:
                        if is_shift:
                            self.character.set_facing('North')
                        else:
                            self.character.facing = 'North'
                            moved = self.world.move_player(self.character, 0, 1)

                    elif event.key == pygame.K_DOWN:
                        if is_shift:
                            self.character.set_facing('South')
                        else:
                            self.character.facing = 'South'
                            moved = self.world.move_player(self.character, 0, -1)

                    elif event.key == pygame.K_RIGHT:
                        if is_shift:
                            self.character.set_facing('East')
                        else:
                            self.character.facing = 'East'
                            moved = self.world.move_player(self.character, 1, 0)

                    elif event.key == pygame.K_LEFT:
                        if is_shift:
                            self.character.set_facing('West')
                        else:
                            self.character.facing = 'West'
                            moved = self.world.move_player(self.character, -1, 0)

                    # Enter / Return / Keypad Enter: Lock tracking or Pick Up ground items / Drink water (Shift+Enter for Realm Travel)
                    elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        self.action_handle_enter(is_shift)

                    if moved:
                        self.tracker.update_ping(self.world, self.character)

                    # Elevation (Page Up / Page Down) OR Shift + Page Up / Page Down for Background Volume
                    elif event.key == pygame.K_PAGEUP:
                        if is_shift:
                            new_vol = self.audio.change_ambient_volume(0.1)
                            msg = loc.tr('volume_ambient_changed', val=new_vol)
                            if self.speech:
                                self.speech.speak(msg)
                        else:
                            self.world.climb_up(self.character)

                    elif event.key == pygame.K_PAGEDOWN:
                        if is_shift:
                            new_vol = self.audio.change_ambient_volume(-0.1)
                            msg = loc.tr('volume_ambient_changed', val=new_vol)
                            if self.speech:
                                self.speech.speak(msg)
                        else:
                            self.world.climb_down(self.character)

                    # Game Master Sound Volume (Home to increase, End to decrease)
                    elif event.key == pygame.K_HOME:
                        new_vol = self.audio.change_game_volume(0.1)
                        msg = loc.tr('volume_game_changed', val=new_vol)
                        if self.speech:
                            self.speech.speak(msg)
                        self.audio.play_menu_select()

                    elif event.key == pygame.K_END:
                        new_vol = self.audio.change_game_volume(-0.1)
                        msg = loc.tr('volume_game_changed', val=new_vol)
                        if self.speech:
                            self.speech.speak(msg)
                        self.audio.play_menu_select()

                    # Turning in place with brackets
                    elif event.key == pygame.K_LEFTBRACKET:
                        self.character.turn_left()
                    elif event.key == pygame.K_RIGHTBRACKET:
                        self.character.turn_right()

                    # Real Compass & GPS Position (C and D Key) OR Shift + C for Campfire
                    elif event.key == pygame.K_c:
                        if is_shift:
                            self.character.make_fire(self.quest_system)
                        else:
                            self.action_report_compass()

                    elif event.key == pygame.K_d:
                        self.action_report_compass()

                    # Campfire (F Key)
                    elif event.key == pygame.K_f:
                        self.character.make_fire(self.quest_system)

                    # Use Weapon / Attack Nearby Creatures (Spacebar or Key X)
                    elif event.key in (pygame.K_SPACE, pygame.K_x):
                        self.action_use_weapon()

                    # Prehistoric Animal Scanner & Cycle (A Key)
                    elif event.key == pygame.K_a:
                        self.action_scan_next_animal()

                    # Travel Gateways Directory (K Key)
                    elif event.key == pygame.K_k:
                        self.world.open_travel_points_menu(self.character, self.tracker, self.screen)

                    # Target Orientation & Distance (O Key)
                    elif event.key == pygame.K_o:
                        self.tracker.report_target_status(self.world, self.character)

                    # Weapon & Tool Crafting Menu (V Key)
                    elif event.key == pygame.K_v:
                        self.crafting.open_crafting_menu(self.character, self.screen)

                    # Survival Audio Guide & Crafting Book Hint (G / F1)
                    elif event.key in (pygame.K_g, pygame.K_F1):
                        hint = loc.tr('guide_hint_bag')
                        if self.speech:
                            self.speech.speak(hint)
                        if self.audio:
                            self.audio.play("menu_select")

                    # Vitals status checks
                    elif event.key == pygame.K_h:
                        self.character.report_health()
                    elif event.key == pygame.K_u:
                        self.character.report_hunger()
                    elif event.key == pygame.K_w and not is_shift:
                        self.character.report_thirst()
                    elif event.key == pygame.K_s:
                        self.character.report_stamina()

                    # Animal Taming (T Key) OR Shift + T for Temperature
                    elif event.key == pygame.K_t:
                        if is_shift:
                            self.character.report_temperature()
                        else:
                            self.action_tame_nearby_creature()

                    # Primitive Lean-to Shelter / Rest (B Key)
                    elif event.key == pygame.K_b:
                        self.action_handle_shelter()

                    # Time & Weather Report (N Key)
                    elif event.key == pygame.K_n:
                        self.world.report_time_and_weather(self.character)

                    # Personal Journey Diary (J Key)
                    elif event.key == pygame.K_j:
                        self.quest_system.read_diary(self.character, self.screen)

                    # In-Game Survival Quick Hub (TAB Key): Quests Journal, Language Switcher, Diary
                    elif event.key == pygame.K_TAB:
                        self.action_open_tab_menu()

                    # Satchel Bag (I Key)
                    elif event.key == pygame.K_i:
                        self.bag.open_bag(self.character, self.screen)
                    
                    # Eat food
                    elif event.key in (pygame.K_1, pygame.K_KP1):
                        if not self.character.eat_item('meat'):
                            self.character.eat_item('wild_berries')
                    
                    # Ground Items & Resources Scanner & Cycle (M Key)
                    elif event.key == pygame.K_m:
                        self.action_scan_next_item()
                    
                    # Look around (L Key)
                    elif event.key == pygame.K_l:
                        self.world.look_around(self.character)
                    
                    # Save & Exit
                    elif event.key in (pygame.K_q, pygame.K_ESCAPE):
                        self._save_game()
                        save_msg = "Progress saved. Returning to Main Menu." if loc.lang == 'en' else "Game mehfooz kar li gayi hai. Main Menu par wapsi."
                        if self.speech:
                            self.speech.speak(save_msg)
                        if self.audio:
                            self.audio.play("menu_back")
                        in_game = False

        self.audio.stop_ambient()

    def _save_game(self):
        if self.current_user and self.character:
            self.db.save_player_data(
                self.current_user,
                self.character.get_stats_dict(),
                self.character.inventory
            )
            print(f"[Save] Progress saved for player: {self.current_user}")

    def action_quit(self):
        if self.speech:
            self.speech.speak(loc.tr('quit_farewell'))
        time.sleep(1.2)
        self.running = False
        pygame.quit()
        sys.exit(0)

if __name__ == '__main__':
    game = JourneyOfMankindGame()
    game.run_main_menu()
