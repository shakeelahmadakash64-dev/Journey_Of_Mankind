"""
Journey of Mankind - Multi-Realm World Architecture (5 Expansive Continents / Maps)
Contains over 125 distinct regions across 5 distinct prehistoric realms:
1. The Primordial Cradle & Rift Valley (Birthplace of Mankind)
2. The Great Prehistoric Ocean & Coastal Archipelago (Beaches & Coral Reefs)
3. The Volcanic Obsidian Badlands (Lava & Volcanic Minerals)
4. The Mammoth Steppe & Ice Age Glaciers (Frozen Tundra)
5. The Deep Underground Cavern Underworld (Subterranean World)
Supports Shift + Enter command to travel between realms with audio transit whoosh.
"""

from core.localization import loc
from game.menu import AccessibleMenu

class WorldTile:
    def __init__(self, key_prefix, surface='dirt', resources=None, is_shelter=False, can_drink=False, default_elevation=0, max_elevation=1, min_elevation=0, travel_point_to=None, travel_target_pos=(0, 0)):
        self.key_prefix = key_prefix
        self.surface = surface  # 'dirt', 'stone', 'water', 'sand', 'snow', 'grass'
        self.resources = resources if resources is not None else []
        self.is_shelter = is_shelter
        self.can_drink = can_drink
        self.default_elevation = default_elevation
        self.max_elevation = max_elevation
        self.min_elevation = min_elevation
        self.travel_point_to = travel_point_to
        self.travel_target_pos = travel_target_pos

    @property
    def name(self):
        return loc.tr(f"tile_{self.key_prefix}_name")

    @property
    def desc(self):
        return loc.tr(f"tile_{self.key_prefix}_desc")

class World:
    def __init__(self, audio=None, speech=None, quest_system=None):
        self.audio = audio
        self.speech = speech
        self.quest_system = quest_system
        self.current_realm_id = 'cradle'
        self.realms = {}
        self.world_time_seconds = 8 * 60.0  # 8:00 AM start
        self.weather = 'clear'
        self.weather_timer = 0.0
        self._build_all_realms()

    @property
    def grid(self):
        return self.realms.get(self.current_realm_id, {})

    def get_realm_display_name(self, realm_id):
        realms_names = {
            'cradle': ("East African Rift Valley (Cradle of Humankind)", "Mashriqi Africa ki Wadi (Insaniyat ki Ibteda)"),
            'coastal': ("Prehistoric Red Sea Coast & Bab-el-Mandeb", "Qadeem Bahira-e-Ahmar aur Bab-el-Mandeb ka Sahil"),
            'volcanic': ("Sinai Peninsula & Arabian Desert Crossroads", "Jazeera-e-Numa Sinai aur Qadeem Sehra"),
            'tundra': ("Fertile Crescent, Zagros & Mammoth Steppe", "Zarkhez Halal, Pahaad aur Mammoth ke Maidan"),
            'underworld': ("Deep Subterranean Caverns & Sacred Caves", "Zameen-doz Muqaddas Ghaar aur Tareek Dunya")
        }
        pair = realms_names.get(realm_id, ("Prehistoric World", "Qadeem Dunya"))
        return pair[0] if loc.lang == 'en' else pair[1]

    def _build_all_realms(self):
        """Constructs 5 massive authentic prehistoric realms, each with a full 11x11 grid (-5 to +5, 121 tiles each, 605 total authentic regions)."""
        self.realms['cradle'] = self._build_cradle_realm()
        self.realms['coastal'] = self._build_coastal_realm()
        self.realms['volcanic'] = self._build_volcanic_realm()
        self.realms['tundra'] = self._build_tundra_realm()
        self.realms['underworld'] = self._build_underworld_realm()

    def _build_cradle_realm(self):
        """Realm 1: East African Rift Valley (121 authentic regions, 11x11 grid -5..5)."""
        grid = {}
        for x in range(-5, 6):
            for y in range(-5, 6):
                if y >= 4:
                    if x == 0:
                        grid[(x, y)] = WorldTile('omo_valley', 'water', [('reed_fiber', 'item_reed_fiber', 4)], can_drink=True, default_elevation=0, max_elevation=0, min_elevation=0)
                    elif x < 0:
                        grid[(x, y)] = WorldTile('turkana_lake', 'water', [('driftwood', 'item_wood_stick', 2)], can_drink=True, default_elevation=0, max_elevation=0, min_elevation=0)
                    else:
                        grid[(x, y)] = WorldTile('rift_highlands', 'stone', [('flint_stone', 'item_flint_stone', 3), ('wood_stick', 'item_wood_stick', 2)], default_elevation=1, max_elevation=1, min_elevation=0)
                elif y <= -4:
                    if x == 0:
                        grid[(x, y)] = WorldTile('deep_cave', 'stone', is_shelter=True, can_drink=True, default_elevation=-1, max_elevation=0, min_elevation=-1)
                    elif x < 0:
                        grid[(x, y)] = WorldTile('crystal_grotto', 'stone', [('flint_stone', 'item_flint_stone', 2)], is_shelter=True, can_drink=True, default_elevation=-1, max_elevation=0, min_elevation=-1)
                    else:
                        grid[(x, y)] = WorldTile('graveyard', 'dirt', [('animal_bone', 'item_animal_bone', 4)], default_elevation=0, max_elevation=1, min_elevation=0)
                elif x <= -4:
                    if y == 0:
                        grid[(x, y)] = WorldTile('canyon', 'stone', [('flint_stone', 'item_flint_stone', 3)], default_elevation=-1, max_elevation=0, min_elevation=-1)
                    elif y > 0:
                        grid[(x, y)] = WorldTile('olduvai_gorge', 'dirt', [('flint_stone', 'item_flint_stone', 4), ('wood_stick', 'item_wood_stick', 2)], default_elevation=0, max_elevation=1, min_elevation=0)
                    else:
                        grid[(x, y)] = WorldTile('lava_tube', 'stone', [('obsidian_shard', 'item_obsidian_shard', 2)], is_shelter=True, default_elevation=-1, max_elevation=0, min_elevation=-1)
                elif x >= 4:
                    if y == 0:
                        grid[(x, y)] = WorldTile('bab_el_mandeb', 'sand', [('driftwood', 'item_wood_stick', 3), ('reed_fiber', 'item_reed_fiber', 2)], default_elevation=0, max_elevation=1, min_elevation=0)
                    elif y > 0:
                        grid[(x, y)] = WorldTile('deep_jungle', 'grass', [('wood_stick', 'item_wood_stick', 4), ('wild_berries', 'item_wild_berries', 3)], default_elevation=0, max_elevation=1, min_elevation=0)
                    else:
                        grid[(x, y)] = WorldTile('dunes', 'sand', default_elevation=0, max_elevation=1, min_elevation=0)
                else:
                    if x == 0 and y == 0:
                        grid[(x, y)] = WorldTile('cradle', 'dirt', [('wood_stick', 'item_wood_stick', 4)], default_elevation=0, max_elevation=1, min_elevation=0)
                    elif x > 0 and y >= 0:
                        rem = (x + y) % 3
                        if rem == 0:
                            grid[(x, y)] = WorldTile('rainforest', 'grass', [('wild_berries', 'item_wild_berries', 3), ('wood_stick', 'item_wood_stick', 3)], default_elevation=0, max_elevation=1, min_elevation=0)
                        elif rem == 1:
                            grid[(x, y)] = WorldTile('woodland', 'grass', [('wood_stick', 'item_wood_stick', 3)], default_elevation=0, max_elevation=1, min_elevation=0)
                        else:
                            grid[(x, y)] = WorldTile('steppes', 'grass', [('wild_berries', 'item_wild_berries', 3)], default_elevation=0, max_elevation=1, min_elevation=0)
                    elif x <= 0 and y > 0:
                        if x == 0:
                            grid[(x, y)] = WorldTile('lake', 'water', [('wood_stick', 'item_wood_stick', 2)], can_drink=True, default_elevation=0, max_elevation=0, min_elevation=0)
                        elif (x + y) % 2 == 0:
                            grid[(x, y)] = WorldTile('serengeti_plains', 'grass', [('wild_berries', 'item_wild_berries', 3)], default_elevation=0, max_elevation=1, min_elevation=0)
                        else:
                            grid[(x, y)] = WorldTile('ridge', 'stone', [('flint_stone', 'item_flint_stone', 3), ('obsidian_shard', 'item_obsidian_shard', 2)], default_elevation=1, max_elevation=1, min_elevation=0)
                    elif x > 0 and y < 0:
                        rem = (x - y) % 3
                        if rem == 0:
                            grid[(x, y)] = WorldTile('savannah', 'grass', [('wild_berries', 'item_wild_berries', 4)], default_elevation=0, max_elevation=1, min_elevation=0)
                        elif rem == 1:
                            grid[(x, y)] = WorldTile('predator', 'stone', [('animal_bone', 'item_animal_bone', 3)], default_elevation=1, max_elevation=1, min_elevation=0)
                        else:
                            grid[(x, y)] = WorldTile('shrubland', 'dirt', [('wood_stick', 'item_wood_stick', 2)], default_elevation=0, max_elevation=1, min_elevation=0)
                    else:
                        rem = (abs(x) + abs(y)) % 3
                        if rem == 0:
                            grid[(x, y)] = WorldTile('cavern', 'stone', [('flint_stone', 'item_flint_stone', 2)], is_shelter=True, default_elevation=0, max_elevation=1, min_elevation=-1)
                        elif rem == 1:
                            grid[(x, y)] = WorldTile('petrified', 'stone', [('flint_stone', 'item_flint_stone', 2)], default_elevation=1, max_elevation=1, min_elevation=0)
                        else:
                            grid[(x, y)] = WorldTile('ash_plains', 'stone', [('obsidian_shard', 'item_obsidian_shard', 2)], default_elevation=0, max_elevation=1, min_elevation=0)

        # Gateways
        grid[(0, 5)]  = WorldTile('omo_valley', 'water', [('reed_fiber', 'item_reed_fiber', 4)], can_drink=True, default_elevation=0, max_elevation=0, min_elevation=0, travel_point_to='volcanic', travel_target_pos=(0, -5))
        grid[(0, -5)] = WorldTile('deep_cave', 'stone', is_shelter=True, can_drink=True, default_elevation=-1, max_elevation=0, min_elevation=-1, travel_point_to='underworld', travel_target_pos=(0, 5))
        grid[(5, 0)]  = WorldTile('bab_el_mandeb', 'sand', [('driftwood', 'item_wood_stick', 3), ('reed_fiber', 'item_reed_fiber', 2)], default_elevation=0, max_elevation=1, min_elevation=0, travel_point_to='coastal', travel_target_pos=(-5, 0))
        grid[(-5, 0)] = WorldTile('canyon', 'stone', [('flint_stone', 'item_flint_stone', 3)], default_elevation=-1, max_elevation=0, min_elevation=-1, travel_point_to='tundra', travel_target_pos=(5, 0))
        return grid

    def _build_coastal_realm(self):
        """Realm 2: Prehistoric Red Sea Coast & Bab-el-Mandeb (121 authentic regions, 11x11 grid -5..5)."""
        grid = {}
        for x in range(-5, 6):
            for y in range(-5, 6):
                if y >= 4:
                    if x == 0:
                        grid[(x, y)] = WorldTile('mangrove_bay', 'water', [('reed_fiber', 'item_reed_fiber', 4)], default_elevation=0, max_elevation=0, min_elevation=0)
                    elif x < 0:
                        grid[(x, y)] = WorldTile('delta', 'water', [('driftwood', 'item_wood_stick', 3)], can_drink=True, default_elevation=0, max_elevation=0, min_elevation=0)
                    else:
                        grid[(x, y)] = WorldTile('coastal_cliffs', 'stone', [('flint_stone', 'item_flint_stone', 2)], default_elevation=1, max_elevation=1, min_elevation=0)
                elif y <= -4:
                    if x == 0:
                        grid[(x, y)] = WorldTile('deep_cave', 'stone', is_shelter=True, default_elevation=-1, max_elevation=0, min_elevation=-1)
                    elif x < 0:
                        grid[(x, y)] = WorldTile('cavern', 'stone', [('flint_stone', 'item_flint_stone', 2)], is_shelter=True, default_elevation=0, max_elevation=1, min_elevation=-1)
                    else:
                        grid[(x, y)] = WorldTile('canyon', 'stone', [('flint_stone', 'item_flint_stone', 2)], default_elevation=-1, max_elevation=0, min_elevation=-1)
                elif x <= -4:
                    if y == 0:
                        grid[(x, y)] = WorldTile('bab_el_mandeb', 'sand', [('driftwood', 'item_wood_stick', 3)], default_elevation=0, max_elevation=1, min_elevation=0)
                    elif y > 0:
                        grid[(x, y)] = WorldTile('dahlak_reefs', 'water', default_elevation=0, max_elevation=0, min_elevation=0)
                    else:
                        grid[(x, y)] = WorldTile('shell_beach', 'sand', [('driftwood', 'item_wood_stick', 2)], default_elevation=0, max_elevation=1, min_elevation=0)
                elif x >= 4:
                    if y == 0:
                        grid[(x, y)] = WorldTile('coastal_cliffs', 'stone', [('flint_stone', 'item_flint_stone', 3)], default_elevation=1, max_elevation=1, min_elevation=0)
                    elif y > 0:
                        grid[(x, y)] = WorldTile('dunes', 'sand', default_elevation=0, max_elevation=1, min_elevation=0)
                    else:
                        grid[(x, y)] = WorldTile('graveyard', 'dirt', [('animal_bone', 'item_animal_bone', 4)], default_elevation=0, max_elevation=1, min_elevation=0)
                else:
                    if x == 0 and y == 0:
                        grid[(x, y)] = WorldTile('oasis', 'sand', [('wild_berries', 'item_wild_berries', 4)], can_drink=True, default_elevation=0, max_elevation=0, min_elevation=0)
                    elif x > 0 and y >= 0:
                        rem = (x + y) % 3
                        if rem == 0:
                            grid[(x, y)] = WorldTile('wetland', 'water', [('reed_fiber', 'item_reed_fiber', 3)], default_elevation=0, max_elevation=0, min_elevation=0)
                        elif rem == 1:
                            grid[(x, y)] = WorldTile('shell_beach', 'sand', [('driftwood', 'item_wood_stick', 2)], default_elevation=0, max_elevation=1, min_elevation=0)
                        else:
                            grid[(x, y)] = WorldTile('dunes', 'sand', default_elevation=0, max_elevation=1, min_elevation=0)
                    elif x <= 0 and y > 0:
                        if x == 0:
                            grid[(x, y)] = WorldTile('lake', 'water', [('driftwood', 'item_wood_stick', 2)], can_drink=True, default_elevation=0, max_elevation=0, min_elevation=0)
                        elif (x + y) % 2 == 0:
                            grid[(x, y)] = WorldTile('dahlak_reefs', 'water', default_elevation=0, max_elevation=0, min_elevation=0)
                        else:
                            grid[(x, y)] = WorldTile('shell_beach', 'sand', [('driftwood', 'item_wood_stick', 2)], default_elevation=0, max_elevation=1, min_elevation=0)
                    elif x > 0 and y < 0:
                        rem = (x - y) % 3
                        if rem == 0:
                            grid[(x, y)] = WorldTile('dunes', 'sand', default_elevation=0, max_elevation=1, min_elevation=0)
                        elif rem == 1:
                            grid[(x, y)] = WorldTile('shell_beach', 'sand', [('driftwood', 'item_wood_stick', 2)], default_elevation=0, max_elevation=1, min_elevation=0)
                        else:
                            grid[(x, y)] = WorldTile('wetland', 'water', [('reed_fiber', 'item_reed_fiber', 3)], default_elevation=0, max_elevation=0, min_elevation=0)
                    else:
                        rem = (abs(x) + abs(y)) % 3
                        if rem == 0:
                            grid[(x, y)] = WorldTile('mangrove_bay', 'water', [('reed_fiber', 'item_reed_fiber', 3)], default_elevation=0, max_elevation=0, min_elevation=0)
                        elif rem == 1:
                            grid[(x, y)] = WorldTile('delta', 'water', [('driftwood', 'item_wood_stick', 3)], can_drink=True, default_elevation=0, max_elevation=0, min_elevation=0)
                        else:
                            grid[(x, y)] = WorldTile('coastal_cliffs', 'stone', [('flint_stone', 'item_flint_stone', 2)], default_elevation=1, max_elevation=1, min_elevation=0)

        # Gateways
        grid[(0, 5)]  = WorldTile('mangrove_bay', 'water', [('reed_fiber', 'item_reed_fiber', 4)], default_elevation=0, max_elevation=0, min_elevation=0, travel_point_to='volcanic', travel_target_pos=(5, 0))
        grid[(0, -5)] = WorldTile('deep_cave', 'stone', is_shelter=True, default_elevation=-1, max_elevation=0, min_elevation=-1, travel_point_to='underworld', travel_target_pos=(5, 0))
        grid[(-5, 0)] = WorldTile('bab_el_mandeb', 'sand', [('driftwood', 'item_wood_stick', 3)], default_elevation=0, max_elevation=1, min_elevation=0, travel_point_to='cradle', travel_target_pos=(5, 0))
        grid[(5, 0)]  = WorldTile('coastal_cliffs', 'stone', [('flint_stone', 'item_flint_stone', 3)], default_elevation=1, max_elevation=1, min_elevation=0, travel_point_to='tundra', travel_target_pos=(-5, 0))
        return grid

    def _build_volcanic_realm(self):
        """Realm 3: Sinai Peninsula & Arabian Desert (121 authentic regions, 11x11 grid -5..5)."""
        grid = {}
        for x in range(-5, 6):
            for y in range(-5, 6):
                if y >= 4:
                    if x == 0:
                        grid[(x, y)] = WorldTile('jordan_gateway', 'dirt', [('wood_stick', 'item_wood_stick', 3)], default_elevation=0, max_elevation=1, min_elevation=0)
                    elif x < 0:
                        grid[(x, y)] = WorldTile('hejaz_basalt', 'stone', [('obsidian_shard', 'item_obsidian_shard', 3)], default_elevation=1, max_elevation=1, min_elevation=0)
                    else:
                        grid[(x, y)] = WorldTile('mount_sinai', 'stone', [('flint_stone', 'item_flint_stone', 4)], default_elevation=1, max_elevation=1, min_elevation=0)
                elif y <= -4:
                    if x == 0:
                        grid[(x, y)] = WorldTile('omo_valley', 'dirt', [('wood_stick', 'item_wood_stick', 3)], default_elevation=0, max_elevation=1, min_elevation=0)
                    elif x < 0:
                        grid[(x, y)] = WorldTile('crystal_grotto', 'stone', [('flint_stone', 'item_flint_stone', 2)], is_shelter=True, can_drink=True, default_elevation=-1, max_elevation=0, min_elevation=-1)
                    else:
                        grid[(x, y)] = WorldTile('graveyard', 'dirt', [('animal_bone', 'item_animal_bone', 4)], default_elevation=0, max_elevation=1, min_elevation=0)
                elif x <= -4:
                    if y == 0:
                        grid[(x, y)] = WorldTile('lava_tube', 'stone', [('obsidian_shard', 'item_obsidian_shard', 2)], is_shelter=True, default_elevation=-1, max_elevation=0, min_elevation=-1)
                    elif y > 0:
                        grid[(x, y)] = WorldTile('canyon', 'stone', [('flint_stone', 'item_flint_stone', 2)], default_elevation=-1, max_elevation=0, min_elevation=-1)
                    else:
                        grid[(x, y)] = WorldTile('petrified', 'stone', [('flint_stone', 'item_flint_stone', 2)], default_elevation=1, max_elevation=1, min_elevation=0)
                elif x >= 4:
                    if y == 0:
                        grid[(x, y)] = WorldTile('coastal_cliffs', 'stone', [('flint_stone', 'item_flint_stone', 3)], default_elevation=1, max_elevation=1, min_elevation=0)
                    elif y > 0:
                        grid[(x, y)] = WorldTile('foothills', 'stone', [('flint_stone', 'item_flint_stone', 3)], default_elevation=1, max_elevation=1, min_elevation=0)
                    else:
                        grid[(x, y)] = WorldTile('dunes', 'sand', default_elevation=0, max_elevation=1, min_elevation=0)
                else:
                    if x == 0 and y == 0:
                        grid[(x, y)] = WorldTile('wadi_feiran', 'sand', [('wood_stick', 'item_wood_stick', 3), ('wild_berries', 'item_wild_berries', 3)], can_drink=True, default_elevation=0, max_elevation=0, min_elevation=0)
                    elif x > 0 and y >= 0:
                        rem = (x + y) % 3
                        if rem == 0:
                            grid[(x, y)] = WorldTile('ridge', 'stone', [('obsidian_shard', 'item_obsidian_shard', 3)], default_elevation=1, max_elevation=1, min_elevation=0)
                        elif rem == 1:
                            grid[(x, y)] = WorldTile('foothills', 'stone', [('flint_stone', 'item_flint_stone', 3)], default_elevation=1, max_elevation=1, min_elevation=0)
                        else:
                            grid[(x, y)] = WorldTile('oasis', 'sand', [('wild_berries', 'item_wild_berries', 3)], can_drink=True, default_elevation=0, max_elevation=0, min_elevation=0)
                    elif x <= 0 and y > 0:
                        rem = (abs(x) + y) % 3
                        if rem == 0:
                            grid[(x, y)] = WorldTile('ash_plains', 'stone', [('obsidian_shard', 'item_obsidian_shard', 2)], default_elevation=0, max_elevation=1, min_elevation=0)
                        elif rem == 1:
                            grid[(x, y)] = WorldTile('wadi_feiran', 'sand', [('wild_berries', 'item_wild_berries', 3), ('wood_stick', 'item_wood_stick', 2)], can_drink=True, default_elevation=0, max_elevation=0, min_elevation=0)
                        else:
                            grid[(x, y)] = WorldTile('ridge', 'stone', [('obsidian_shard', 'item_obsidian_shard', 3), ('flint_stone', 'item_flint_stone', 2)], default_elevation=1, max_elevation=1, min_elevation=0)
                    elif x > 0 and y < 0:
                        rem = (x - y) % 3
                        if rem == 0:
                            grid[(x, y)] = WorldTile('dunes', 'sand', default_elevation=0, max_elevation=1, min_elevation=0)
                        elif rem == 1:
                            grid[(x, y)] = WorldTile('predator', 'stone', [('animal_bone', 'item_animal_bone', 2)], default_elevation=1, max_elevation=1, min_elevation=0)
                        else:
                            grid[(x, y)] = WorldTile('cavern', 'stone', [('flint_stone', 'item_flint_stone', 2)], is_shelter=True, default_elevation=0, max_elevation=1, min_elevation=-1)
                    else:
                        rem = (abs(x) + abs(y)) % 3
                        if rem == 0:
                            grid[(x, y)] = WorldTile('ash_plains', 'stone', [('obsidian_shard', 'item_obsidian_shard', 2)], default_elevation=0, max_elevation=1, min_elevation=0)
                        elif rem == 1:
                            grid[(x, y)] = WorldTile('petrified', 'stone', [('flint_stone', 'item_flint_stone', 2)], default_elevation=1, max_elevation=1, min_elevation=0)
                        else:
                            grid[(x, y)] = WorldTile('canyon', 'stone', [('flint_stone', 'item_flint_stone', 2)], default_elevation=-1, max_elevation=0, min_elevation=-1)

        # Gateways
        grid[(0, 5)]  = WorldTile('jordan_gateway', 'dirt', [('wood_stick', 'item_wood_stick', 3)], default_elevation=0, max_elevation=1, min_elevation=0, travel_point_to='tundra', travel_target_pos=(0, -5))
        grid[(0, -5)] = WorldTile('omo_valley', 'dirt', [('wood_stick', 'item_wood_stick', 3)], default_elevation=0, max_elevation=1, min_elevation=0, travel_point_to='cradle', travel_target_pos=(0, 5))
        grid[(5, 0)]  = WorldTile('coastal_cliffs', 'stone', [('flint_stone', 'item_flint_stone', 3)], default_elevation=1, max_elevation=1, min_elevation=0, travel_point_to='coastal', travel_target_pos=(0, 5))
        grid[(-5, 0)] = WorldTile('lava_tube', 'stone', [('obsidian_shard', 'item_obsidian_shard', 2)], is_shelter=True, default_elevation=-1, max_elevation=0, min_elevation=-1, travel_point_to='underworld', travel_target_pos=(-5, 0))
        return grid

    def _build_tundra_realm(self):
        """Realm 4: Fertile Crescent & Mammoth Steppe (121 authentic regions, 11x11 grid -5..5)."""
        grid = {}
        for x in range(-5, 6):
            for y in range(-5, 6):
                if y >= 4:
                    if x == 0:
                        grid[(x, y)] = WorldTile('ice_glacier', 'snow', default_elevation=1, max_elevation=1, min_elevation=0)
                    elif x < 0:
                        grid[(x, y)] = WorldTile('glacier_pass', 'snow', [('flint_stone', 'item_flint_stone', 2)], default_elevation=1, max_elevation=1, min_elevation=0)
                    else:
                        grid[(x, y)] = WorldTile('mammoth_steppe', 'snow', [('animal_bone', 'item_animal_bone', 4)], default_elevation=0, max_elevation=1, min_elevation=0)
                elif y <= -4:
                    if x == 0:
                        grid[(x, y)] = WorldTile('jordan_gateway', 'dirt', [('wood_stick', 'item_wood_stick', 2)], default_elevation=0, max_elevation=1, min_elevation=0)
                    elif x < 0:
                        grid[(x, y)] = WorldTile('rapids', 'water', [('wood_stick', 'item_wood_stick', 2)], can_drink=True, default_elevation=0, max_elevation=0, min_elevation=0)
                    else:
                        grid[(x, y)] = WorldTile('oasis', 'sand', [('wild_berries', 'item_wild_berries', 3)], can_drink=True, default_elevation=0, max_elevation=0, min_elevation=0)
                elif x <= -4:
                    if y == 0:
                        grid[(x, y)] = WorldTile('delta', 'water', [('driftwood', 'item_wood_stick', 3)], can_drink=True, default_elevation=0, max_elevation=0, min_elevation=0)
                    elif y > 0:
                        grid[(x, y)] = WorldTile('mammoth_steppe', 'snow', [('animal_bone', 'item_animal_bone', 3)], default_elevation=0, max_elevation=1, min_elevation=0)
                    else:
                        grid[(x, y)] = WorldTile('canyon', 'stone', [('flint_stone', 'item_flint_stone', 2)], default_elevation=-1, max_elevation=0, min_elevation=-1)
                elif x >= 4:
                    if y == 0:
                        grid[(x, y)] = WorldTile('woodland', 'grass', [('wood_stick', 'item_wood_stick', 3)], default_elevation=0, max_elevation=1, min_elevation=0)
                    elif y > 0:
                        grid[(x, y)] = WorldTile('steppes', 'grass', [('wild_berries', 'item_wild_berries', 3)], default_elevation=0, max_elevation=1, min_elevation=0)
                    else:
                        grid[(x, y)] = WorldTile('graveyard', 'dirt', [('animal_bone', 'item_animal_bone', 4)], default_elevation=0, max_elevation=1, min_elevation=0)
                else:
                    if x == 0 and y == 0:
                        grid[(x, y)] = WorldTile('tigris_headwaters', 'water', [('wood_stick', 'item_wood_stick', 3)], can_drink=True, default_elevation=0, max_elevation=0, min_elevation=0)
                    elif x > 0 and y >= 0:
                        rem = (x + y) % 3
                        if rem == 0:
                            grid[(x, y)] = WorldTile('zagros_foothills', 'grass', [('wood_stick', 'item_wood_stick', 3), ('wild_berries', 'item_wild_berries', 3)], default_elevation=0, max_elevation=1, min_elevation=0)
                        elif rem == 1:
                            grid[(x, y)] = WorldTile('steppes', 'grass', [('wild_berries', 'item_wild_berries', 4)], default_elevation=0, max_elevation=1, min_elevation=0)
                        else:
                            grid[(x, y)] = WorldTile('woodland', 'grass', [('wood_stick', 'item_wood_stick', 3)], default_elevation=0, max_elevation=1, min_elevation=0)
                    elif x <= 0 and y > 0:
                        rem = (abs(x) + y) % 3
                        if rem == 0:
                            grid[(x, y)] = WorldTile('shanidar_cave', 'stone', [('flint_stone', 'item_flint_stone', 3)], is_shelter=True, default_elevation=0, max_elevation=1, min_elevation=-1)
                        elif rem == 1:
                            grid[(x, y)] = WorldTile('tigris_headwaters', 'water', [('driftwood', 'item_wood_stick', 2)], can_drink=True, default_elevation=0, max_elevation=0, min_elevation=0)
                        else:
                            grid[(x, y)] = WorldTile('zagros_foothills', 'grass', [('wood_stick', 'item_wood_stick', 3)], default_elevation=0, max_elevation=1, min_elevation=0)
                    elif x > 0 and y < 0:
                        rem = (x - y) % 3
                        if rem == 0:
                            grid[(x, y)] = WorldTile('shrubland', 'dirt', [('wood_stick', 'item_wood_stick', 2)], default_elevation=0, max_elevation=1, min_elevation=0)
                        elif rem == 1:
                            grid[(x, y)] = WorldTile('predator', 'stone', [('animal_bone', 'item_animal_bone', 2)], default_elevation=1, max_elevation=1, min_elevation=0)
                        else:
                            grid[(x, y)] = WorldTile('cavern', 'stone', [('flint_stone', 'item_flint_stone', 2)], is_shelter=True, default_elevation=0, max_elevation=1, min_elevation=-1)
                    else:
                        rem = (abs(x) + abs(y)) % 3
                        if rem == 0:
                            grid[(x, y)] = WorldTile('wetland', 'water', [('reed_fiber', 'item_reed_fiber', 4)], default_elevation=0, max_elevation=0, min_elevation=0)
                        elif rem == 1:
                            grid[(x, y)] = WorldTile('woodland', 'grass', [('wood_stick', 'item_wood_stick', 3)], default_elevation=0, max_elevation=1, min_elevation=0)
                        else:
                            grid[(x, y)] = WorldTile('cavern', 'stone', [('flint_stone', 'item_flint_stone', 2)], is_shelter=True, default_elevation=0, max_elevation=1, min_elevation=-1)

        # Gateways
        grid[(0, 5)]  = WorldTile('ice_glacier', 'snow', default_elevation=1, max_elevation=1, min_elevation=0, travel_point_to='underworld', travel_target_pos=(0, -5))
        grid[(0, -5)] = WorldTile('jordan_gateway', 'dirt', [('wood_stick', 'item_wood_stick', 2)], default_elevation=0, max_elevation=1, min_elevation=0, travel_point_to='volcanic', travel_target_pos=(0, 5))
        grid[(-5, 0)] = WorldTile('delta', 'water', [('driftwood', 'item_wood_stick', 3)], can_drink=True, default_elevation=0, max_elevation=0, min_elevation=0, travel_point_to='coastal', travel_target_pos=(5, 0))
        grid[(5, 0)]  = WorldTile('woodland', 'grass', [('wood_stick', 'item_wood_stick', 3)], default_elevation=0, max_elevation=1, min_elevation=0, travel_point_to='cradle', travel_target_pos=(-5, 0))
        return grid

    def _build_underworld_realm(self):
        """Realm 5: Deep Subterranean Caverns (121 authentic regions, 11x11 grid -5..5)."""
        grid = {}
        for x in range(-5, 6):
            for y in range(-5, 6):
                if y >= 4:
                    if x == 0:
                        grid[(x, y)] = WorldTile('deep_cave', 'stone', is_shelter=True, can_drink=True, default_elevation=-1, max_elevation=0, min_elevation=-1)
                    elif x < 0:
                        grid[(x, y)] = WorldTile('stalactite_chasm', 'stone', [('flint_stone', 'item_flint_stone', 3)], default_elevation=-1, max_elevation=0, min_elevation=-1)
                    else:
                        grid[(x, y)] = WorldTile('bioluminescent_grotto', 'stone', [('flint_stone', 'item_flint_stone', 2)], is_shelter=True, default_elevation=-1, max_elevation=0, min_elevation=-1)
                elif y <= -4:
                    if x == 0:
                        grid[(x, y)] = WorldTile('ice_glacier', 'stone', is_shelter=True, default_elevation=-1, max_elevation=0, min_elevation=-1)
                    elif x < 0:
                        grid[(x, y)] = WorldTile('canyon', 'stone', [('flint_stone', 'item_flint_stone', 2)], default_elevation=-1, max_elevation=0, min_elevation=-1)
                    else:
                        grid[(x, y)] = WorldTile('lava_tube', 'stone', [('obsidian_shard', 'item_obsidian_shard', 2)], is_shelter=True, default_elevation=-1, max_elevation=0, min_elevation=-1)
                elif x <= -4:
                    if y == 0:
                        grid[(x, y)] = WorldTile('lava_tube', 'stone', [('obsidian_shard', 'item_obsidian_shard', 3)], is_shelter=True, default_elevation=-1, max_elevation=0, min_elevation=-1)
                    elif y > 0:
                        grid[(x, y)] = WorldTile('bioluminescent_grotto', 'stone', [('flint_stone', 'item_flint_stone', 2)], is_shelter=True, default_elevation=-1, max_elevation=0, min_elevation=-1)
                    else:
                        grid[(x, y)] = WorldTile('crystal_grotto', 'stone', [('flint_stone', 'item_flint_stone', 2)], is_shelter=True, can_drink=True, default_elevation=-1, max_elevation=0, min_elevation=-1)
                elif x >= 4:
                    if y == 0:
                        grid[(x, y)] = WorldTile('deep_cave', 'stone', is_shelter=True, default_elevation=-1, max_elevation=0, min_elevation=-1)
                    elif y > 0:
                        grid[(x, y)] = WorldTile('stalactite_chasm', 'stone', [('flint_stone', 'item_flint_stone', 2)], default_elevation=-1, max_elevation=0, min_elevation=-1)
                    else:
                        grid[(x, y)] = WorldTile('petrified', 'stone', [('flint_stone', 'item_flint_stone', 2)], default_elevation=0, max_elevation=0, min_elevation=-1)
                else:
                    if x == 0 and y == 0:
                        grid[(x, y)] = WorldTile('cave_art_sanctuary', 'stone', [('flint_stone', 'item_flint_stone', 3)], is_shelter=True, default_elevation=-1, max_elevation=0, min_elevation=-1)
                    elif x > 0 and y >= 0:
                        rem = (x + y) % 3
                        if rem == 0:
                            grid[(x, y)] = WorldTile('cavern', 'stone', [('flint_stone', 'item_flint_stone', 2)], is_shelter=True, default_elevation=-1, max_elevation=0, min_elevation=-1)
                        elif rem == 1:
                            grid[(x, y)] = WorldTile('subterranean_river', 'water', can_drink=True, default_elevation=-1, max_elevation=-1, min_elevation=-1)
                        else:
                            grid[(x, y)] = WorldTile('canyon', 'stone', [('flint_stone', 'item_flint_stone', 2)], default_elevation=-1, max_elevation=0, min_elevation=-1)
                    elif x <= 0 and y > 0:
                        rem = (abs(x) + y) % 3
                        if rem == 0:
                            grid[(x, y)] = WorldTile('lava_tube', 'stone', [('obsidian_shard', 'item_obsidian_shard', 2)], is_shelter=True, default_elevation=-1, max_elevation=0, min_elevation=-1)
                        elif rem == 1:
                            grid[(x, y)] = WorldTile('cave_art_sanctuary', 'stone', [('flint_stone', 'item_flint_stone', 3)], is_shelter=True, default_elevation=-1, max_elevation=0, min_elevation=-1)
                        else:
                            grid[(x, y)] = WorldTile('subterranean_river', 'water', can_drink=True, default_elevation=-1, max_elevation=-1, min_elevation=-1)
                    elif x > 0 and y < 0:
                        rem = (x - y) % 3
                        if rem == 0:
                            grid[(x, y)] = WorldTile('graveyard', 'dirt', [('animal_bone', 'item_animal_bone', 4)], default_elevation=-1, max_elevation=0, min_elevation=-1)
                        elif rem == 1:
                            grid[(x, y)] = WorldTile('petrified', 'stone', [('flint_stone', 'item_flint_stone', 2)], default_elevation=0, max_elevation=0, min_elevation=-1)
                        else:
                            grid[(x, y)] = WorldTile('deep_cave', 'stone', is_shelter=True, default_elevation=-1, max_elevation=0, min_elevation=-1)
                    else:
                        rem = (abs(x) + abs(y)) % 3
                        if rem == 0:
                            grid[(x, y)] = WorldTile('ridge', 'stone', [('obsidian_shard', 'item_obsidian_shard', 2)], default_elevation=0, max_elevation=0, min_elevation=-1)
                        elif rem == 1:
                            grid[(x, y)] = WorldTile('subterranean_river', 'water', can_drink=True, default_elevation=-1, max_elevation=-1, min_elevation=-1)
                        else:
                            grid[(x, y)] = WorldTile('crystal_grotto', 'stone', [('flint_stone', 'item_flint_stone', 2)], is_shelter=True, can_drink=True, default_elevation=-1, max_elevation=0, min_elevation=-1)

        # Gateways
        grid[(0, 5)]  = WorldTile('deep_cave', 'stone', is_shelter=True, can_drink=True, default_elevation=-1, max_elevation=0, min_elevation=-1, travel_point_to='cradle', travel_target_pos=(0, -5))
        grid[(0, -5)] = WorldTile('ice_glacier', 'stone', is_shelter=True, default_elevation=-1, max_elevation=0, min_elevation=-1, travel_point_to='tundra', travel_target_pos=(0, 5))
        grid[(5, 0)]  = WorldTile('deep_cave', 'stone', is_shelter=True, default_elevation=-1, max_elevation=0, min_elevation=-1, travel_point_to='coastal', travel_target_pos=(0, -5))
        grid[(-5, 0)] = WorldTile('lava_tube', 'stone', [('obsidian_shard', 'item_obsidian_shard', 3)], is_shelter=True, default_elevation=-1, max_elevation=0, min_elevation=-1, travel_point_to='volcanic', travel_target_pos=(-5, 0))
        return grid

    def get_tile(self, x, y):
        return self.grid.get((x, y), None)

    def move_player(self, character, dx, dy):
        """Move character by delta (dx, dy)."""
        new_x = character.pos_x + dx
        new_y = character.pos_y + dy
        
        target_tile = self.get_tile(new_x, new_y)
        if not target_tile:
            current_tile = self.get_tile(character.pos_x, character.pos_y)
            if current_tile and current_tile.travel_point_to:
                dest_name = self.get_realm_display_name(current_tile.travel_point_to)
                msg = f"You stand at the border to {dest_name}. Press Shift + Enter to cross into this map." if loc.lang == 'en' else f"Aap {dest_name} ke kinare par hain. Is map mein dakhil honay ke liay Shift + Enter dabayein."
                if self.speech:
                    self.speech.speak(msg)
                if self.audio:
                    self.audio.play_portalopen()
                return False

            if self.speech:
                self.speech.speak(loc.tr('way_blocked'))
            if self.audio:
                self.audio.play_error()
            return False

        # Apply movement
        character.pos_x = new_x
        character.pos_y = new_y
        character.elevation = target_tile.default_elevation
        character.stamina = max(0.0, character.stamina - 1.5)
        
        if self.audio:
            pan = -0.3 if dx < 0 else (0.3 if dx > 0 else 0.0)
            self.audio.play_footstep(target_tile.surface, pan=pan)

        if self.speech:
            elev_str = self.get_elevation_name(character.elevation)
            msg = f"{target_tile.name} ({elev_str}). {target_tile.desc}"
            if target_tile.travel_point_to:
                dest_name = self.get_realm_display_name(target_tile.travel_point_to)
                portal_hint = f" [Travel Point: Gateway to {dest_name}. Press Shift + Enter to cross into this map]" if loc.lang == 'en' else f" [Travel Point: {dest_name} ka rasta. Is map mein dakhil honay ke liay Shift + Enter dabayein]"
                msg += portal_hint
                if self.audio:
                    self.audio.play_portalopen()
            self.speech.speak(msg)
            
        return True

    def move_forward(self, character):
        facing = character.facing
        if facing == 'North':
            return self.move_player(character, 0, 1)
        elif facing == 'South':
            return self.move_player(character, 0, -1)
        elif facing == 'East':
            return self.move_player(character, 1, 0)
        elif facing == 'West':
            return self.move_player(character, -1, 0)
        return False

    def move_backward(self, character):
        facing = character.facing
        if facing == 'North':
            return self.move_player(character, 0, -1)
        elif facing == 'South':
            return self.move_player(character, 0, 1)
        elif facing == 'East':
            return self.move_player(character, -1, 0)
        elif facing == 'West':
            return self.move_player(character, 1, 0)
        return False

    def climb_up(self, character):
        tile = self.get_tile(character.pos_x, character.pos_y)
        if not tile or character.elevation >= tile.max_elevation:
            if self.speech:
                self.speech.speak(loc.tr('climb_up_blocked'))
            if self.audio:
                self.audio.play_error()
            return False

        character.elevation += 1
        character.stamina = max(0.0, character.stamina - 4.0)
        if self.audio:
            self.audio.play_climb_up()
            self.audio.play_voice_climb()
        elev_str = self.get_elevation_name(character.elevation)
        if self.speech:
            self.speech.speak(loc.tr('climb_up_success', level=elev_str))
        return True

    def climb_down(self, character):
        tile = self.get_tile(character.pos_x, character.pos_y)
        if not tile or character.elevation <= tile.min_elevation:
            if self.speech:
                self.speech.speak(loc.tr('climb_down_blocked'))
            if self.audio:
                self.audio.play_error()
            return False

        character.elevation -= 1
        character.stamina = max(0.0, character.stamina - 2.0)
        if self.audio:
            self.audio.play_climb_down()
            self.audio.play_voice_climb()
        elev_str = self.get_elevation_name(character.elevation)
        if self.speech:
            self.speech.speak(loc.tr('climb_down_success', level=elev_str))
        return True

    def get_elevation_name(self, elev):
        if elev > 0:
            return loc.tr('elevation_high')
        elif elev < 0:
            return loc.tr('elevation_deep')
        return loc.tr('elevation_ground')

    def handle_realm_travel(self, character, screen=None):
        """Called on Shift + Enter: If standing on a Travel Point, directly crosses into the realm!"""
        cur_tile = self.get_tile(character.pos_x, character.pos_y)
        if cur_tile and cur_tile.travel_point_to:
            target_realm = cur_tile.travel_point_to
            target_pos = cur_tile.travel_target_pos
            dest_name = self.get_realm_display_name(target_realm)
            
            # Direct crossing!
            self.current_realm_id = target_realm
            character.pos_x = target_pos[0]
            character.pos_y = target_pos[1]
            new_tile = self.get_tile(character.pos_x, character.pos_y)
            character.elevation = new_tile.default_elevation if new_tile else 0
            
            if self.audio:
                self.audio.play_portalopen()
                self.audio.play_travel_whoosh()
                self.audio.set_realm_ambience(target_realm)
                
            t_name = new_tile.name if new_tile else "Realm"
            t_desc = new_tile.desc if new_tile else ""
            travel_msg = f"Traveled through the Gateway into {dest_name}! You stand upon {t_name}. {t_desc}" if loc.lang == 'en' else f"Aap Gateway se guzar kar {dest_name} mein pohanch gaye hain! {t_name}. {t_desc}"
            if self.speech:
                self.speech.speak(travel_msg)
            return "TRAVELED"
        else:
            not_at_portal_msg = "You are not at a Travel Point gateway. Walk to a map border (North, South, East, West) to find a gateway, or press K to track one." if loc.lang == 'en' else "Aap kisi Travel Point par mojood nahi hain. Map ke kinaron par gateway dhoondein ya K daba kar track karein."
            if self.speech:
                self.speech.speak(not_at_portal_msg)
            if self.audio:
                self.audio.play_error()
            return "NOT_AT_PORTAL"

    def open_travel_points_menu(self, character, tracker, screen=None):
        """Opens the Travel Points & Gateways Directory for the current realm (Key K).
        Allows the player to select any travel gateway in this map with Enter to lock tracking onto it.
        Key O can then be pressed to report distance and compass/relative heading."""
        portal_tiles = []
        for (tx, ty), tile in self.grid.items():
            if tile.travel_point_to:
                dist = abs(tx - character.pos_x) + abs(ty - character.pos_y)
                dest_name = self.get_realm_display_name(tile.travel_point_to)
                portal_tiles.append((tx, ty, tile, dest_name, dist))

        if not portal_tiles:
            msg = "No travel gateways found in this map." if loc.lang == 'en' else "Is map mein koi travel point nahi mila."
            if self.speech:
                self.speech.speak(msg)
            if self.audio:
                self.audio.play_error()
            return

        # Sort by distance
        portal_tiles.sort(key=lambda item: item[4])

        options = []
        for tx, ty, tile, dest_name, dist in portal_tiles:
            dx = tx - character.pos_x
            dy = ty - character.pos_y
            dir_str = tracker._get_direction_name(dx, dy)
            
            if dist == 0:
                label_en = f"Gateway to {dest_name} (At your current location! Press Shift+Enter to travel)"
                label_ur = f"{dest_name} ka Gateway (Aap yahin kharay hain! Shift+Enter dabayein)"
            else:
                label_en = f"Gateway to {dest_name} - {dist} tiles {dir_str} at [{tx}, {ty}]"
                label_ur = f"{dest_name} ka Gateway - {dist} tiles {dir_str} [{tx}, {ty}]"
            
            label = label_en if loc.lang == 'en' else label_ur
            
            def make_lock_fn(target_x=tx, target_y=ty, name=f"Gateway to {dest_name}", dest_id=tile.travel_point_to, d_name=dest_name, distance=dist, d_str=dir_str):
                def _select():
                    tracker.set_target(target_x, target_y, name, target_type='travel_point', realm_dest=dest_id)
                    if distance == 0:
                        conf_msg = f"Tracking locked on {name}. You are already standing on this gateway! Press Shift + Enter to cross into {d_name}." if loc.lang == 'en' else f"{name} track ho gaya. Aap pehle hi is gateway par kharay hain! {d_name} mein dakhil honay ke liay Shift + Enter dabayein."
                    else:
                        conf_msg = f"Tracking locked onto {name}! It is {distance} tiles away to the {d_str}. Press O to hear distance and heading, or follow 3D sonar beeps." if loc.lang == 'en' else f"{name} tracking par lag gaya! Yeh {distance} tiles door {d_str} mein hai. O daba kar fasla aur samt sunein, ya audio sonar pings follow karein."
                    if self.speech:
                        self.speech.speak(conf_msg)
                    if self.audio:
                        self.audio.play_portalopen()
                    return "LOCKED"
                return _select

            options.append((label, make_lock_fn()))

        options.append((loc.tr('back'), lambda: "BACK"))

        cur_realm_name = self.get_realm_display_name(self.current_realm_id)
        menu_title = f"Travel Gateways Directory ({cur_realm_name})" if loc.lang == 'en' else f"Travel Points Directory ({cur_realm_name})"
        menu = AccessibleMenu(menu_title, options, self.audio, self.speech)
        menu.run(screen)

    def open_realm_travel_menu(self, character, screen=None):
        """Opens the Realm Portal Travel menu to journey to other massive maps."""
        realms_info = [
            ('cradle', "1. East African Rift Valley (Cradle of Humankind)", "1. Mashriqi Africa ki Wadi (Insaniyat ki Ibteda)"),
            ('coastal', "2. Prehistoric Red Sea Coast & Bab-el-Mandeb", "2. Qadeem Bahira-e-Ahmar aur Bab-el-Mandeb"),
            ('volcanic', "3. Sinai Peninsula & Arabian Desert Crossroads", "3. Jazeera-e-Numa Sinai aur Qadeem Sehra"),
            ('tundra', "4. Fertile Crescent, Zagros & Mammoth Steppe", "4. Zarkhez Halal, Pahaad aur Mammoth ke Maidan"),
            ('underworld', "5. Deep Subterranean Caverns & Sacred Caves", "5. Zameen-doz Muqaddas Ghaar aur Tareek Dunya")
        ]

        options = []
        for rid, en_label, ur_label in realms_info:
            label = en_label if loc.lang == 'en' else ur_label
            if rid == self.current_realm_id:
                label += " [Current Realm]" if loc.lang == 'en' else " [Mojooda Map]"
            
            def make_travel_fn(target_id=rid, tname=label):
                return lambda: self._travel_to_realm(character, target_id, tname)
            options.append((label, make_travel_fn()))

        options.append((loc.tr('back'), lambda: "BACK"))

        menu_title = "Realm Portal Travel (Shift + Enter)" if loc.lang == 'en' else "Dosray Maps ki Sair (Shift + Enter)"
        menu = AccessibleMenu(menu_title, options, self.audio, self.speech)
        menu.run(screen)

    def _travel_to_realm(self, character, realm_id, realm_name):
        if realm_id == self.current_realm_id:
            msg = "You are already in this realm." if loc.lang == 'en' else "Aap pehle hi is map mein mojood hain."
            if self.speech:
                self.speech.speak(msg)
            return "DONE"

        self.current_realm_id = realm_id
        character.pos_x = 0
        character.pos_y = 0
        character.elevation = 0

        if self.audio:
            self.audio.play_portalopen()
            self.audio.play_travel_whoosh()
            self.audio.set_realm_ambience(realm_id)

        cur_tile = self.get_tile(0, 0)
        t_name = cur_tile.name if cur_tile else "Realm"
        t_desc = cur_tile.desc if cur_tile else ""

        travel_msg = f"Traveled across continents to {realm_name}! You stand upon {t_name}. {t_desc}" if loc.lang == 'en' else f"Aap safar kar ke {realm_name} mein pohanch gaye hain! {t_name}. {t_desc}"
        if self.speech:
            self.speech.speak(travel_msg)

        qs = self.quest_system or getattr(character, 'quest_system', None)
        if qs:
            qs.check_milestone(character, 'cross_realm')

        return "TRAVELED"

    def interact_current_tile(self, character):
        tile = self.get_tile(character.pos_x, character.pos_y)
        if not tile:
            return

        interacted = False
        if tile.can_drink:
            character.drink_water()
            interacted = True

        if tile.resources:
            gathered_msgs = []
            for item_id, item_tr_key, qty in list(tile.resources):
                item_name = loc.tr(item_tr_key)
                character.add_item(item_id, item_name, qty)
                gathered_msgs.append(f"{qty} {item_name}")
                if item_id in ('obsidian_shard', 'flint_stone'):
                    qs = self.quest_system or getattr(character, 'quest_system', None)
                    if qs:
                        qs.check_milestone(character, 'mine_minerals')
            tile.resources.clear()
            msg = loc.tr('gathered_items', items=', '.join(gathered_msgs))
            if self.audio:
                self.audio.play("menu_select")
            if self.speech:
                self.speech.speak(msg)
            interacted = True

        if not interacted:
            if self.speech:
                self.speech.speak(loc.tr('nothing_to_gather'))
            if self.audio:
                self.audio.play("footstep_dirt")

    def update_time(self, dt):
        """Simulate day/night cycle progression. 1 real second = 1 game minute (24 minutes = 1 full day/night)."""
        self.world_time_seconds = (self.world_time_seconds + dt * 2.0) % 1440.0
        self.weather_timer += dt
        if self.weather_timer > 120.0:
            self.weather_timer = 0.0
            import random
            if self.current_realm_id == 'tundra':
                weathers = ['clear', 'blizzard', 'clear']
            elif self.current_realm_id == 'underworld':
                weathers = ['clear']
            else:
                weathers = ['clear', 'rain', 'clear', 'storm']
            self.weather = random.choice(weathers)

    def get_time_of_day(self):
        hour = int((self.world_time_seconds / 60.0) % 24)
        if 5 <= hour < 11:
            phase = loc.tr('time_morning')
            is_night = False
        elif 11 <= hour < 15:
            phase = loc.tr('time_midday')
            is_night = False
        elif 15 <= hour < 19:
            phase = loc.tr('time_afternoon')
            is_night = False
        elif 19 <= hour < 22:
            phase = loc.tr('time_dusk')
            is_night = True
        else:
            phase = loc.tr('time_night')
            is_night = True
        return hour, phase, is_night

    def get_weather_name(self):
        w_map = {
            'clear': 'weather_clear',
            'rain': 'weather_rain',
            'storm': 'weather_storm',
            'blizzard': 'weather_blizzard'
        }
        return loc.tr(w_map.get(self.weather, 'weather_clear'))

    def report_time_and_weather(self, character):
        hour, phase, is_night = self.get_time_of_day()
        w_name = self.get_weather_name()
        temp = int(character.temperature)
        msg = loc.tr('time_report', hour=hour, phase=phase, weather=w_name, temp=temp)
        if self.speech:
            self.speech.speak(msg)
        return msg

    def build_shelter_at(self, character, quest_system=None):
        """Constructs a Lean-to shelter on the player's current tile."""
        tile = self.get_tile(character.pos_x, character.pos_y)
        if not tile:
            return False

        if tile.is_shelter:
            msg = "This location already has a sturdy shelter! Press B to rest safely." if loc.lang == 'en' else "Yahan pehle se aik mehfooz panahgah bani hui hai! Rest karne ke liye B dabayen."
            if self.speech:
                self.speech.speak(msg)
            return True

        has_sticks = character.get_item_quantity('wood_stick') >= 3
        has_fibers = character.get_item_quantity('reed_fiber') >= 2

        if not (has_sticks and has_fibers):
            msg = loc.tr('shelter_req_err')
            if self.speech:
                self.speech.speak(msg)
            if self.audio:
                self.audio.play_footstep('dirt')
            return False

        character.remove_item('wood_stick', 3)
        character.remove_item('reed_fiber', 2)
        tile.is_shelter = True

        if self.audio:
            self.audio.play("craft_success")
            self.audio.play("fire_kindle")
        
        msg = loc.tr('shelter_built')
        if self.speech:
            self.speech.speak(msg)

        qs = quest_system or self.quest_system or getattr(character, 'quest_system', None)
        if qs:
            qs.check_milestone(character, 'build_shelter')
        return True

    def rest_in_shelter(self, character, quest_system=None):
        tile = self.get_tile(character.pos_x, character.pos_y)
        if not tile or not tile.is_shelter:
            msg = "No shelter here. Press B or craft a shelter with 3 branches and 2 fibers to rest." if loc.lang == 'en' else "Yahan koi panahgah nahi hai. Shelter bananay ke liye 3 lakriyan aur 2 fibers darkaar hain."
            if self.speech:
                self.speech.speak(msg)
            return False

        character.stamina = min(100.0, character.stamina + 50.0)
        character.health = min(100.0, character.health + 30.0)
        character.temperature = 37.0
        
        if self.audio:
            self.audio.play("menu_select")
            
        msg = loc.tr('shelter_rested')
        if self.speech:
            self.speech.speak(msg)

        qs = quest_system or self.quest_system or getattr(character, 'quest_system', None)
        if qs:
            qs.check_milestone(character, 'rest_shelter')
        return True

    def look_around(self, character):
        tile = self.get_tile(character.pos_x, character.pos_y)
        if not tile:
            return
        
        nearby = []
        directions = [
            (0, 1, loc.tr('north')),
            (0, -1, loc.tr('south')),
            (1, 0, loc.tr('east')),
            (-1, 0, loc.tr('west'))
        ]
        
        for dx, dy, d_name in directions:
            neighbor = self.get_tile(character.pos_x + dx, character.pos_y + dy)
            if neighbor:
                nearby.append(f"{d_name}: {neighbor.name}")
                
        elev_str = self.get_elevation_name(character.elevation)
        facing_str = loc.tr(character.facing.lower())
        msg = loc.tr('look_around_intro',
            name=tile.name,
            elev=elev_str,
            facing=facing_str,
            neighbors='. '.join(nearby)
        )
        if self.speech:
            self.speech.speak(msg)
        return msg
