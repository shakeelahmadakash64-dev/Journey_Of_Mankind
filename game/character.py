"""
Journey of Mankind - Realistic Human Character & Biological Survival
Simulates health, hunger, thirst, stamina, body temperature, elevation, facing direction,
and equipped weapons for prehistoric combat.
"""

import time
from core.localization import loc

DIRECTIONS = ['North', 'East', 'South', 'West']

class Character:
    def __init__(self, username, stats=None, inventory=None, audio=None, speech=None):
        self.username = username
        self.audio = audio
        self.speech = speech
        
        # Core biological survival attributes
        if stats:
            self.health = float(stats.get('health', 100.0))
            self.hunger = float(stats.get('hunger', 100.0))
            self.thirst = float(stats.get('thirst', 100.0))
            self.stamina = float(stats.get('stamina', 100.0))
            self.temperature = float(stats.get('temperature', 37.0))
            self.pos_x = int(stats.get('pos_x', 0))
            self.pos_y = int(stats.get('pos_y', 0))
            self.elevation = int(stats.get('elevation', 0))
            self.facing = str(stats.get('facing', 'North'))
        else:
            self.health = 100.0
            self.hunger = 100.0
            self.thirst = 100.0
            self.stamina = 100.0
            self.temperature = 37.0
            self.pos_x = 0
            self.pos_y = 0
            self.elevation = 0
            self.facing = 'North'
            
        self.inventory = inventory if inventory is not None else []
        self._ensure_starting_books()
        self.equipped_weapon = 'fists'
        self.equipped_weapon_name = 'Fists'
        self.weapon_damage = 10
        self.last_update_time = time.time()
        self.has_fire = False
        self.is_alive = True
        self.pet = None
        self.is_inside_shelter = False
        self.shelter_x = 0
        self.shelter_y = -1
        
        self._check_equipped_weapon()

    def _ensure_starting_books(self):
        """Ensures the player always possesses their Survival Guide Book, Crafting Recipe Book, and Journey Diary in their satchel."""
        starting_books = [
            ('diary', 'item_diary'),
            ('guide_book', 'item_guide_book'),
            ('crafting_book', 'item_crafting_book')
        ]
        for b_id, name_key in starting_books:
            if not any(i['id'] == b_id for i in self.inventory):
                self.inventory.insert(0, {'id': b_id, 'name': loc.tr(name_key), 'quantity': 1})

    def _check_equipped_weapon(self):
        """Auto-detect weapon if none manually equipped or if currently equipped item was removed."""
        if self.equipped_weapon != 'fists' and any(i['id'] == self.equipped_weapon and i.get('quantity', 0) > 0 for i in self.inventory):
            return

        weapon_priority = [
            ('obsidian_dagger', 'item_obsidian_dagger', 35),
            ('bone_club', 'item_bone_club', 30),
            ('spear', 'item_spear', 25),
            ('sling', 'item_sling', 18),
            ('torch', 'item_torch', 15)
        ]
        for w_id, name_key, dmg in weapon_priority:
            if any(i['id'] == w_id and i.get('quantity', 0) > 0 for i in self.inventory):
                self.equipped_weapon = w_id
                self.equipped_weapon_name = loc.tr(name_key)
                self.weapon_damage = dmg
                return

        self.equipped_weapon = 'fists'
        self.equipped_weapon_name = "Bare Hands" if loc.lang == 'en' else "Khaali Haath"
        self.weapon_damage = 10

    def hold_item(self, item_id, item_name, damage=None):
        """Holds the selected item in the character's hand as their active tool/weapon."""
        self.equipped_weapon = item_id
        self.equipped_weapon_name = item_name

        standard_damages = {
            'obsidian_dagger': 35,
            'bone_club': 30,
            'spear': 25,
            'sling': 18,
            'torch': 15,
            'obsidian_shard': 18,
            'animal_bone': 16,
            'flint_stone': 15,
            'wood_stick': 14,
            'wild_berries': 10,
            'meat': 10,
            'reed_fiber': 10,
            'fists': 10
        }
        if damage is not None:
            self.weapon_damage = damage
        else:
            self.weapon_damage = standard_damages.get(item_id, 10)
        return self.weapon_damage

    def get_stats_dict(self):
        return {
            'health': round(self.health, 1),
            'hunger': round(self.hunger, 1),
            'thirst': round(self.thirst, 1),
            'stamina': round(self.stamina, 1),
            'temperature': round(self.temperature, 1),
            'pos_x': self.pos_x,
            'pos_y': self.pos_y,
            'elevation': self.elevation,
            'facing': self.facing
        }

    @property
    def facing_degrees(self):
        deg_map = {'North': 0, 'East': 90, 'South': 180, 'West': 270}
        return deg_map.get(self.facing, 0)

    def set_facing(self, new_facing):
        """Set facing direction directly (North, South, East, West) via Shift + Arrows."""
        if new_facing not in DIRECTIONS:
            return self.facing
        self.facing = new_facing
        if self.audio:
            self.audio.play_turn()
        dir_name = loc.tr(self.facing.lower())
        deg = self.facing_degrees
        msg = loc.tr('turned_to', dir=dir_name, deg=deg)
        if self.speech:
            self.speech.speak(msg)
        return self.facing

    def turn_left(self):
        """Turn 90 degrees to the left."""
        idx = DIRECTIONS.index(self.facing)
        self.facing = DIRECTIONS[(idx - 1) % len(DIRECTIONS)]
        if self.audio:
            self.audio.play_turn()
        dir_name = loc.tr(self.facing.lower())
        deg = self.facing_degrees
        msg = loc.tr('turned_to', dir=dir_name, deg=deg)
        if self.speech:
            self.speech.speak(msg)
        return self.facing

    def turn_right(self):
        """Turn 90 degrees to the right."""
        idx = DIRECTIONS.index(self.facing)
        self.facing = DIRECTIONS[(idx + 1) % len(DIRECTIONS)]
        if self.audio:
            self.audio.play_turn()
        dir_name = loc.tr(self.facing.lower())
        deg = self.facing_degrees
        msg = loc.tr('turned_to', dir=dir_name, deg=deg)
        if self.speech:
            self.speech.speak(msg)
        return self.facing

    def report_facing(self):
        """Speak current compass heading."""
        dir_name = loc.tr(self.facing.lower())
        deg = self.facing_degrees
        msg = loc.tr('facing_report', dir=dir_name, deg=deg)
        if self.speech:
            self.speech.speak(msg)
        return msg

    def update_vitals(self, elapsed_seconds=1.0):
        """Simulate real human biological depletion over time."""
        if not self.is_alive:
            return

        thirst_drain = 0.15 * elapsed_seconds
        hunger_drain = 0.08 * elapsed_seconds
        
        self.thirst = max(0.0, self.thirst - thirst_drain)
        self.hunger = max(0.0, self.hunger - hunger_drain)
        
        if self.is_inside_shelter:
            self.temperature = 37.0
            if self.stamina < 100.0:
                self.stamina = min(100.0, self.stamina + (5.0 * elapsed_seconds))
            if self.health < 100.0:
                self.health = min(100.0, self.health + (1.0 * elapsed_seconds))
        else:
            if self.stamina < 100.0:
                self.stamina = min(100.0, self.stamina + (2.0 * elapsed_seconds))

            ideal_temp = 37.0 if self.has_fire else 36.6
            if self.temperature > ideal_temp:
                self.temperature = max(ideal_temp, self.temperature - 0.02 * elapsed_seconds)
            elif self.temperature < ideal_temp:
                self.temperature = min(ideal_temp, self.temperature + 0.02 * elapsed_seconds)

        if self.thirst <= 0.0 or self.hunger <= 0.0:
            damage = 0.3 * elapsed_seconds
            self.health = max(0.0, self.health - damage)
            if self.health <= 0.0:
                self.die(loc.tr('death_reason_starve'))

    def check_audio_cues(self):
        """Play autonomous sound alerts when body is under distress."""
        if not self.is_alive:
            return

        if self.health <= 25.0 and self.audio:
            self.audio.play_heartbeat()
        elif self.stamina <= 20.0 and self.audio:
            self.audio.play_voice_pant()
        elif self.hunger <= 25.0 and self.audio:
            self.audio.play_stomach_rumble()

    def report_health(self):
        txt = loc.tr('health_report', val=int(self.health))
        if self.health < 30:
            txt += " " + loc.tr('health_critical')
            if self.audio:
                self.audio.play_heartbeat()
        if self.speech:
            self.speech.speak(txt)
        return txt

    def report_hunger(self):
        txt = loc.tr('hunger_report', val=int(self.hunger))
        if self.hunger < 25:
            txt += " " + loc.tr('hunger_alert')
            if self.audio:
                self.audio.play_stomach_rumble()
        if self.speech:
            self.speech.speak(txt)
        return txt

    def report_thirst(self):
        txt = loc.tr('thirst_report', val=int(self.thirst))
        if self.thirst < 25:
            txt += " " + loc.tr('thirst_alert')
        if self.speech:
            self.speech.speak(txt)
        return txt

    def report_stamina(self):
        txt = loc.tr('stamina_report', val=int(self.stamina))
        if self.speech:
            self.speech.speak(txt)
        return txt

    def report_temperature(self):
        txt = loc.tr('temp_report', val=f"{self.temperature:.1f}")
        if self.has_fire:
            txt += " " + loc.tr('temp_warm_alert')
        elif self.temperature < 36.5:
            txt += " " + loc.tr('temp_cold_alert')
        if self.speech:
            self.speech.speak(txt)
        return txt

    def report_full_status(self):
        txt = loc.tr('status_report',
            health=int(self.health),
            hunger=int(self.hunger),
            thirst=int(self.thirst),
            stamina=int(self.stamina),
            temp=f"{self.temperature:.1f}"
        )
        if self.speech:
            self.speech.speak(txt)
        return txt

    def drink_water(self):
        if self.thirst >= 99.0:
            if self.speech:
                self.speech.speak(loc.tr('thirst_quenched'))
            return False

        self.thirst = min(100.0, self.thirst + 45.0)
        if self.audio:
            self.audio.play("drink")
        if self.speech:
            self.speech.speak(loc.tr('drank_water', val=int(self.thirst)))
        return True

    def eat_item(self, item_id):
        item = next((i for i in self.inventory if i['id'] == item_id), None)
        if not item or item['quantity'] <= 0:
            if self.speech:
                self.speech.speak(loc.tr('item_not_in_inv'))
            if self.audio:
                self.audio.play_error()
            return False

        if item_id == 'wild_berries':
            self.hunger = min(100.0, self.hunger + 25.0)
            self.health = min(100.0, self.health + 5.0)
            item['quantity'] -= 1
            if item['quantity'] <= 0:
                self.inventory.remove(item)
            if self.audio:
                self.audio.play("eat")
            if self.speech:
                self.speech.speak(loc.tr('ate_berries', val=int(self.hunger)))
            return True
        elif item_id == 'meat':
            self.hunger = min(100.0, self.hunger + 40.0)
            self.health = min(100.0, self.health + 15.0)
            item['quantity'] -= 1
            if item['quantity'] <= 0:
                self.inventory.remove(item)
            if self.audio:
                self.audio.play("eat")
            if self.speech:
                self.speech.speak(f"Ate nutritious meat. Hunger is now {int(self.hunger)}%." if loc.lang == 'en' else f"Kacha gosht khaya. Bhook ab {int(self.hunger)}% hai.")
            return True
        elif item_id == 'cooked_meat':
            self.hunger = min(100.0, self.hunger + 65.0)
            self.health = min(100.0, self.health + 30.0)
            item['quantity'] -= 1
            if item['quantity'] <= 0:
                self.inventory.remove(item)
            if self.audio:
                self.audio.play("eat")
            if self.speech:
                self.speech.speak(f"Ate savory roasted meat steak! Hunger is {int(self.hunger)}%, Health is {int(self.health)}%." if loc.lang == 'en' else f"Mazaydar bhuna hua gosht khaya! Bhook {int(self.hunger)}%, Sehat {int(self.health)}% ho gayi.")
            return True
        return False

    def roast_meat(self, quest_system=None):
        """Roasts raw meat over an active campfire."""
        if not self.has_fire:
            msg = loc.tr('roast_no_fire')
            if self.speech:
                self.speech.speak(msg)
            if self.audio:
                self.audio.play_error()
            return False

        raw_item = next((i for i in self.inventory if i['id'] == 'meat' and i.get('quantity', 0) > 0), None)
        if not raw_item:
            msg = loc.tr('roast_no_meat')
            if self.speech:
                self.speech.speak(msg)
            if self.audio:
                self.audio.play_error()
            return False

        raw_item['quantity'] -= 1
        if raw_item['quantity'] <= 0:
            self.inventory.remove(raw_item)

        self.add_item('cooked_meat', loc.tr('item_cooked_meat'), 1)
        if self.audio:
            self.audio.play("flint_strike")
        msg = loc.tr('roast_success')
        if self.speech:
            self.speech.speak(msg)
        if quest_system:
            quest_system.check_milestone(self, 'roast')
        return True

    def tame_creature(self, creature, quest_system=None):
        """Tames a nearby beast by feeding it meat or berries."""
        if not creature or not creature.is_alive:
            msg = loc.tr('tame_no_beast')
            if self.speech:
                self.speech.speak(msg)
            return False

        food_item = next((i for i in self.inventory if i['id'] in ('meat', 'cooked_meat', 'wild_berries') and i.get('quantity', 0) > 0), None)
        if not food_item:
            msg = loc.tr('tame_no_food')
            if self.speech:
                self.speech.speak(msg)
            if self.audio:
                self.audio.play_error()
            return False

        food_item['quantity'] -= 1
        if food_item['quantity'] <= 0:
            self.inventory.remove(food_item)

        self.pet = {
            'name': creature.name,
            'id': creature.creature_id,
            'damage': 15
        }
        creature.is_alive = False

        if self.audio:
            self.audio.play_item_found()
        msg = loc.tr('tame_success', name=creature.name)
        if self.speech:
            self.speech.speak(msg)
        if quest_system:
            quest_system.check_milestone(self, 'tame_wolf')
        return True

    def enter_shelter(self, quest_system=None):
        """Enters Lean-to shelter (called on Shift + Enter). Shelters from storm, regenerates stats, and allows free indoor exploration."""
        self.is_inside_shelter = True
        self.shelter_x = 0
        self.shelter_y = -1
        if self.audio:
            if hasattr(self.audio, 'play_door_open'):
                self.audio.play_door_open()
            self.audio.play_shelter_enter()
            if hasattr(self.audio, 'play_door_close'):
                self.audio.play_door_close()
            if hasattr(self.audio, 'set_shelter_ambience'):
                self.audio.set_shelter_ambience()
        msg = loc.tr('shelter_entered')
        if self.speech:
            self.speech.speak(msg)
        qs = quest_system or getattr(self, 'quest_system', None)
        if qs:
            qs.check_milestone(self, 'rest_shelter')
        return True

    def exit_shelter(self, realm_id=None):
        """Exits Lean-to shelter back into the open world (called on Shift + Enter or walking out door)."""
        self.is_inside_shelter = False
        if self.audio:
            if hasattr(self.audio, 'play_door_open'):
                self.audio.play_door_open()
            self.audio.play_shelter_exit()
            if hasattr(self.audio, 'play_door_close'):
                self.audio.play_door_close()
            if realm_id and hasattr(self.audio, 'set_realm_ambience'):
                self.audio.set_realm_ambience(realm_id)
        msg = loc.tr('shelter_exited')
        if self.speech:
            self.speech.speak(msg)
        return True

    def move_inside_shelter(self, dx, dy, realm_id=None):
        """Allows free movement inside the spacious 5x5 shelter interior."""
        # If at door (0, -2) and walking South (dy < 0): DO NOT exit automatically; must press Shift + Enter!
        if self.shelter_x == 0 and self.shelter_y == -2 and dy < 0:
            if self.audio:
                self.audio.play("weapon_hit")
            msg = loc.tr('shelter_door_closed_hint')
            if self.speech:
                self.speech.speak(msg)
            return False

        new_x = self.shelter_x + dx
        new_y = self.shelter_y + dy

        # Boundary check (-2 to 2 in both x and y)
        if new_x < -2 or new_x > 2 or new_y < -2 or new_y > 2:
            if self.audio:
                self.audio.play("weapon_hit")
            msg = loc.tr('shelter_wall_hit')
            if self.speech:
                self.speech.speak(msg)
            return False

        self.shelter_x = new_x
        self.shelter_y = new_y

        if self.audio:
            pan = max(-0.8, min(0.8, self.shelter_x * 0.4))
            self.audio.play_footstep('wood', pan=pan)

        tile_desc = self.get_shelter_tile_desc(new_x, new_y)
        if self.speech:
            self.speech.speak(tile_desc)
        return True

    def get_shelter_tile_desc(self, x, y):
        coords_map = {
            (0, -2): loc.tr('shelter_loc_door'),
            (0, -1): loc.tr('shelter_loc_entry'),
            (0, 0): loc.tr('shelter_loc_hearth'),
            (0, 1): loc.tr('shelter_loc_bedroll'),
            (0, 2): loc.tr('shelter_loc_meat_rack'),
            (-1, 0): loc.tr('shelter_loc_workbench'),
            (1, 0): loc.tr('shelter_loc_herbs'),
            (-2, 0): loc.tr('shelter_loc_wall_west'),
            (2, 0): loc.tr('shelter_loc_wall_east'),
            (-1, 1): loc.tr('shelter_loc_nw'),
            (1, 1): loc.tr('shelter_loc_ne'),
            (-1, -1): loc.tr('shelter_loc_sw'),
            (1, -1): loc.tr('shelter_loc_se'),
        }
        if (x, y) in coords_map:
            return coords_map[(x, y)]
        return f"Shelter Interior ({x}, {y})" if loc.lang == 'en' else f"Panahgah ke Andar ({x}, {y})"

    def add_item(self, item_id, item_name, quantity=1):
        for item in self.inventory:
            if item['id'] == item_id:
                item['quantity'] += quantity
                self._check_equipped_weapon()
                return
        self.inventory.append({'id': item_id, 'name': item_name, 'quantity': quantity})
        self._check_equipped_weapon()

    def get_item_quantity(self, item_id):
        for item in self.inventory:
            if item['id'] == item_id:
                return item.get('quantity', 0)
        return 0

    def remove_item(self, item_id, quantity=1):
        for item in self.inventory:
            if item['id'] == item_id:
                item['quantity'] -= quantity
                if item['quantity'] <= 0:
                    self.inventory.remove(item)
                self._check_equipped_weapon()
                return True
        return False

    def list_inventory(self):
        if not self.inventory:
            msg = loc.tr('inv_empty')
            if self.speech:
                self.speech.speak(msg)
            return msg
        
        items_text = ", ".join([f"{item['name']}: {item['quantity']}" for item in self.inventory])
        equipped_str = f" Equipped Weapon: {self.equipped_weapon_name} (Damage: {self.weapon_damage})."
        msg = loc.tr('inv_list', items=items_text) + equipped_str
        if self.speech:
            self.speech.speak(msg)
        return msg

    def make_fire(self, quest_system=None):
        has_flint = any(i['id'] == 'flint_stone' and i['quantity'] >= 2 for i in self.inventory)
        has_wood = any(i['id'] == 'wood_stick' and i['quantity'] >= 2 for i in self.inventory)
        
        if not (has_flint and has_wood):
            msg = loc.tr('fire_req_err')
            if self.speech:
                self.speech.speak(msg)
            if self.audio:
                self.audio.play_error()
            return False
            
        if self.audio:
            self.audio.play("flint_strike")
        time.sleep(0.3)
        if self.audio:
            self.audio.play("flint_strike")
            
        self.has_fire = True
        self.temperature = 37.2
        for i in self.inventory:
            if i['id'] == 'wood_stick':
                i['quantity'] -= 1
                if i['quantity'] <= 0:
                    self.inventory.remove(i)
                break
                
        msg = loc.tr('fire_made')
        if self.speech:
            self.speech.speak(msg)
        if quest_system:
            quest_system.check_milestone(self, 'fire')
        return True

    def revive(self):
        """Immediately and automatically revives the character with 100% vitals at Central Sacred Hearth."""
        self.is_alive = True
        self.health = 100.0
        self.hunger = 100.0
        self.thirst = 100.0
        self.stamina = 100.0
        self.temperature = 37.0
        self.pos_x = 0
        self.pos_y = 0
        self.elevation = 0
        self.facing = 'North'
        self.is_inside_shelter = False

        if self.audio:
            self.audio.play_portalopen()
            self.audio.play_heartbeat()

        msg = loc.tr('auto_revived')
        if self.speech:
            self.speech.speak(msg)

    def die(self, reason=""):
        """Called upon vital depletion or fatal predator strike: automatically self-revives."""
        self.revive()
