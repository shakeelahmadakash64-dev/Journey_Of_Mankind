"""
Journey of Mankind - Localization Engine (English Primary, Urdu Secondary)
Provides seamless language switching between English (default) and Urdu for screen readers and UI.
Includes rich strings for Elevation, Directions, Prehistoric Creatures, Weapons Crafting, and Audio Guide.
"""

class Localization:
    def __init__(self, default_lang='en'):
        self.lang = default_lang
        self._strings = {
            'en': {
                # Game Title & Menus
                'game_title': "Journey of Mankind: The Audio Survival Odyssey",
                'menu_title': "Journey of Mankind - Main Menu",
                'menu_start': "Start / Continue Game",
                'menu_new_account': "Create New Account",
                'menu_select_account': "Select / Switch Account",
                'menu_language': "Change Language (English / Urdu)",
                'menu_help': "Controls & Audio Guide",
                'menu_quit': "Exit Game",
                'menu_current_account': "Current Account",
                'none': "None",
                'selected': "Selected",
                'back': "Back",
                'quit_farewell': "Exiting Journey of Mankind. Farewell!",
                'lang_switched': "Language set to English.",

                # Account & Prompts
                'enter_name_prompt': "Enter your player name",
                'name_instructions': "Type your name and press Enter, or press Escape to cancel.",
                'name_empty_err': "Player name cannot be empty. Please type again.",
                'char_deleted': "Deleted",
                'account_created': "Account '{name}' created successfully!",
                'account_exists': "Account name '{name}' already exists. Please choose another.",
                'no_accounts': "No accounts found. Please create a new account first.",
                'account_selected': "Account '{name}' selected.",

                # Prologue
                'prologue_start': "Starting the Genesis Prologue. Press Spacebar at any time to skip.",
                'prologue_skipped': "Prologue skipped.",
                'prologue_scene1': "Billions of years ago, in the vast infinite darkness, a colossal cosmic event ignited the universe—the Big Bang. Stars formed, galaxies revolved, and our Solar System was born.",
                'prologue_scene2': "Molten fires cooled into solid rock. Torrential rains fell from roaring skies for millennia, filling great primordial oceans as the first spark of life took breath.",
                'prologue_scene3': "And then came the dawn of humankind! A vulnerable being, weaponless and alone, yet gifted with intelligence and wonder. Today is your very first day on Primordial Earth.",
                'prologue_scene4': "Your destiny: Survive against the wild, master fire, craft tools, trade with tribes, and advance science until you unlock the stars. Welcome to the Journey of Mankind!",

                # Survival Vitals & Health
                'status_report': "Status: Health {health}%, Hunger {hunger}%, Thirst {thirst}%, Stamina {stamina}%, Body Temp {temp} Celsius.",
                'health_report': "Health: {val} percent.",
                'health_critical': "Danger! You are critically wounded or exhausted.",
                'hunger_report': "Hunger: {val} percent.",
                'hunger_alert': "Your stomach is empty. Forage for food quickly!",
                'thirst_report': "Thirst: {val} percent.",
                'thirst_alert': "Your throat is parched. Find freshwater immediately!",
                'stamina_report': "Stamina: {val} percent.",
                'temp_report': "Body Temperature: {val} degrees Celsius.",
                'temp_cold_alert': "You are shivering from cold. Build a fire or seek shelter.",
                'temp_warm_alert': "A campfire warms your body.",
                'thirst_quenched': "Your thirst is already fully quenched.",
                'drank_water': "Drank refreshing cool freshwater. Thirst is now {val} percent.",
                'item_not_in_inv': "Item not found in your inventory.",
                'ate_berries': "Ate wild berries. Hunger restored, now at {val} percent.",
                'gathered_items': "You gathered: {items}.",
                'nothing_to_gather': "Nothing more to forage or gather here right now.",
                'inv_empty': "Your inventory is currently empty.",
                'inv_list': "Inventory contents: {items}.",
                'fire_req_err': "You need at least 2 Flint stones and 2 Wood sticks to start a fire.",
                'fire_made': "Sparks ignite into a roaring campfire! Warmth embraces you and wild beasts flee into the shadows.",
                'death_msg': "You have perished: {reason}. Try again.",
                'death_reason_starve': "from acute starvation and dehydration.",
                'death_reason_predator': "mauled by a prehistoric predator.",

                # Elevation (Page Up / Page Down)
                'climb_up_success': "You scramble up the steep incline onto the higher plateau. Elevation: {level}.",
                'climb_up_blocked': "The rock face above is sheer vertical cliff. You cannot climb higher here.",
                'climb_down_success': "You descend carefully down the slopes into the lower depression. Elevation: {level}.",
                'climb_down_blocked': "You have reached the bottom ground level. Cannot descend further here.",
                'elevation_high': "High Plateau / Ridge (Elevation +1)",
                'elevation_ground': "Valley Ground Level (Elevation 0)",
                'elevation_deep': "Subterranean Depth / Canyon (Elevation -1)",
                'elevation_status': "Current elevation: {elev_name}.",

                # Direction & Compass
                'facing_report': "You are facing {dir} ({deg} degrees). Press Shift + Arrows to change direction, or Up arrow to walk forward.",
                'turned_to': "Turned to face {dir} ({deg} degrees).",
                'degrees': "{val} degrees",
                'north': "North",
                'south': "South",
                'east': "East",
                'west': "West",
                'compass_title': "Real Compass & GPS Position",
                'compass_coords': "Coordinates: X {x}, Y {y}, Elevation {elev}.",
                'compass_region': "Current Region: {area} in {realm}.",
                'compass_heading': "Facing: {facing} ({deg} degrees).",
                'compass_surroundings': "Surroundings: North: {north}. South: {south}. East: {east}. West: {west}.",
                'compass_target_none': "Tracking: None. Press A to track beasts or K for travel points.",
                'compass_target_active': "Tracking Target: {name} is {dist} tiles {dir}.",

                # Prehistoric Creatures & Fauna
                'fauna_radar_title': "Prehistoric Animal Radar (Current Realm)",
                'fauna_no_beasts': "No live creatures detected roaming in this realm right now.",
                'fauna_locked': "Tracking locked onto {name}! {dist} steps {dir}. Press O anytime to check orientation or follow audio sonar pings.",
                'fauna_hostile_tag': "(Hostile Predator)",
                'fauna_herbivore_tag': "(Herbivore / Huntable)",
                'creature_mammoth_name': "Woolly Mammoth (Stegodon)",
                'creature_mammoth_desc': "A towering prehistoric giant with curved ivory tusks and thick fur. Its heavy footsteps shake the earth.",
                'creature_sabertooth_name': "Sabertooth Cat (Machairodus)",
                'creature_sabertooth_desc': "A lethal apex predator with razor-sharp curved fangs and yellow predatory eyes, stalking from the shadows.",
                'creature_cave_bear_name': "Giant Cave Bear (Ursus spelaeus)",
                'creature_cave_bear_desc': "A colossal hibernating bear guarding the deep cavern interior. Its deep growl echoes off the stone walls.",
                'creature_hyena_name': "Dire Hyena Pack",
                'creature_hyena_desc': "Scavengers with bone-crushing jaws cackling in the distance.",
                'creature_gazelle_name': "Primordial Gazelle",
                'creature_gazelle_desc': "A swift, graceful herbivore grazing peacefully. Valuable source of meat, sinew, and hides.",
                'creature_rhino_name': "Woolly Rhinoceros (Coelodonta)",
                'creature_rhino_desc': "A massive armored beast with a giant double horn and shaggy winter pelt.",
                'creature_lion_name': "Siberian Cave Lion (Panthera spelaea)",
                'creature_lion_desc': "An enormous prehistoric apex predator stalking the frozen tundra margins.",
                'creature_serpent_name': "Blind Underworld Serpent",
                'creature_serpent_desc': "A giant subterranean serpent sensing vibrations through limestone cavern walls.",
                'creature_near_warning': "Warning! You hear a {name} nearby in the {direction}! Prepare your weapon or keep your distance.",
                'creature_attacked_player': "The {name} strikes at you! You take {dmg} damage.",
                'player_attack_hit': "You strike the {name} with your {weapon} for {dmg} damage!",
                'creature_slain': "The {name} has collapsed! You harvested fresh meat and bones.",
                'character_respawned': "You collapsed from exhaustion or fatal wounds! The ancestral primordial spirits revive you at the Central Sacred Hearth with full vitals.",
                'auto_revived': "You collapsed from fatal wounds or exhaustion! The ancestral primordial spirits automatically revive you at the Central Sacred Hearth with full 100% vitals.",
                'item_scan_cycle': "{name} (Qty: {qty}) - {dist} steps {dir}. Press Enter to lock tracking or M for next item.",
                'item_scan_water_cycle': "Freshwater Drinking Source - {dist} steps {dir}. Press Enter to lock tracking or M for next item.",
                'item_scan_none': "No ground items or resources found in this realm right now.",
                'item_scan_locked': "Tracking locked onto {name}! {dist} steps {dir}. Follow audio sonar pings or press O for orientation.",
                'animal_scan_cycle': "{name} {tag} - {dist} steps {dir}. Press Enter to lock tracking or A for next animal.",
                'animal_scan_locked': "Tracking locked onto {name}! {dist} steps {dir}. Follow audio sonar pings or press O for orientation.",
                'tile_interact_empty': "Nothing to pick up on this ground. Press M to scan for nearby items or A for animals.",

                # Weapons & Crafting
                'craft_menu_title': "Stone Age Weapon & Tool Crafting",
                'craft_equipped': "Currently equipped: {weapon}.",
                'craft_success': "Successfully crafted: {item}! It has been added to your inventory.",
                'craft_missing_mat': "Missing materials! Recipe requires: {req}.",
                'craft_spear_name': "Hardwood Spear (Lakri ka Neza)",
                'craft_spear_desc': "Long sharpened wooden spear. Keeps predators at bay and deals 25 piercing damage.",
                'craft_spear_req': "2 Hardwood Branches, 1 Flint Stone",
                'craft_dagger_name': "Obsidian Dagger (Obsidian Chhuri)",
                'craft_dagger_desc': "Razor-sharp black volcanic glass blade bound with reed fiber. Deals 35 slashing damage.",
                'craft_dagger_req': "1 Obsidian Shard, 1 Hardwood Branch, 1 Reed Fiber",
                'craft_torch_name': "Fire Torch (Aag ki Mashaal)",
                'craft_torch_desc': "Blazing firebrand that illuminates dark caverns and frightens predators.",
                'craft_torch_req': "1 Hardwood Branch, 1 Reed Fiber, Active Campfire",
                'craft_club_name': "Heavy Bone Club (Haddi ka Gurj)",
                'craft_club_desc': "Crushing blunt weapon carved from prehistoric animal bone. Deals 30 impact damage.",
                'craft_club_req': "1 Animal Bone, 1 Reed Fiber",
                'craft_sling_name': "Hunting Stone Sling (Pathar ki Ghulail)",
                'craft_sling_desc': "Woven reed pouch to hurl stones at distant game. Deals 18 ranged damage.",
                'craft_sling_req': "2 Reed Fibers, 1 Smooth Flint Stone",

                # Interactive In-Game Audio Guide
                'guide_title': "Primordial Survival Audio Guide",
                'guide_section_nav': (
                    "1. Navigation, Elevation, Compass & Gateways: "
                    "Use Arrow keys (Up, Down, Left, Right) to walk across the regions. "
                    "Hold Shift with Arrow keys (Shift + Up, Down, Left, Right) to turn facing direction in place (North 0 degrees, South 180 degrees, East 90 degrees, West 270 degrees). "
                    "Press C or D to hear your Real Compass & GPS coordinates, elevation, facing heading in degrees, and surrounding areas. "
                    "Tap M repeatedly to cycle through all ground resources and water sources one by one with distance and direction. Press Enter on any item to lock sonar tracking! "
                    "Tap A repeatedly to cycle through all live prehistoric beasts one by one. Press Enter on any animal to lock sonar tracking! "
                    "Press Enter or Spacebar on any tile to pick up ground resources into your bag or drink freshwater. "
                    "Press Page Up to climb up steep ridges or plateaus. "
                    "Press Page Down to descend into deep caverns or sunken valleys. "
                    "Press Shift + Page Up to increase background ambient volume, and Shift + Page Down to decrease it. "
                    "Press Home to increase game master sound volume, and End to decrease it. "
                    "Press X to attack or hunt beasts with your equipped weapon. "
                    "Press K to open the Travel Gateways Directory to select any destination and lock tracking onto it. "
                    "Press O to hear the exact distance in tiles and heading to your active target, with 3D sonar beeps. "
                    "Press Shift + Enter when standing at a border gateway to travel directly into the adjacent map."
                ),
                'volume_ambient_changed': "Background volume: {val} percent.",
                'volume_game_changed': "Game volume: {val} percent.",
                'guide_section_fauna': (
                    "2. Prehistoric Fauna & Animal Radar: "
                    "The world is inhabited by real prehistoric creatures across all 5 realms: Woolly Mammoths, Sabertooth Cats, Cave Bears, Dire Hyenas, Woolly Rhinos, and Gazelles. "
                    "Tap A repeatedly anytime to scan and cycle through every live beast in the realm one by one with distance and direction. "
                    "Press Enter on any beast to lock tracking onto it. "
                    "Follow the 3D stereo sonar pings, or press O to check distance and heading. "
                    "When adjacent to or on the beast, press X to attack and hunt it with your weapon!"
                ),
                'guide_section_weapons': (
                    "3. How to Craft Weapons (Step-by-Step Tutorial): "
                    "First, explore the world and tap M to scan nearby ground resources, then press Enter to collect them. "
                    "Gather Hardwood Branches from the Cradle Valley, Flint Stones and Obsidian from the Volcanic Ridge, Reed Fibers from the Marshes, and Animal Bones from hunting. "
                    "Second, press V on your keyboard to open the Crafting Menu. "
                    "Third, use Up and Down arrow keys to browse craftable weapons: Hardwood Spear, Obsidian Dagger, Fire Torch, Bone Club, or Stone Sling. "
                    "Fourth, press Enter to craft. The new weapon will automatically equip and increase your damage. "
                    "Fifth, when encountering wild beasts, press X to attack with your crafted weapon!"
                ),
                'guide_section_vitals': (
                    "4. Human Biology & Vitals: "
                    "Keep your Health, Hunger, Thirst, Stamina, and Temperature high. "
                    "Drink at lakes and rivers with Enter or Spacebar. "
                    "Forage berries with Enter and press 1 to eat. "
                    "Press Shift + C or F to strike fire with flint when cold. "
                    "Listen to bodily distress audio cues: heartbeats alert low health, stomach rumbles alert hunger. "
                    "If you ever collapse from wounds or exhaustion, the ancestral primordial fires will automatically revive you immediately with full 100% vitals at the Central Hearth."
                ),

                # Map & Navigation
                'way_blocked': "Dense prehistoric foliage and treacherous terrain block your path.",
                'current_location_is': "You have arrived at: {name}. {desc}",
                'look_around_intro': "You are at '{name}' ({elev}). Facing: {facing}. Nearby: {neighbors}",

                # Primordial Map Tiles (Authentic Prehistoric Regions)
                'tile_cradle_name': "The Primordial Cradle Valley",
                'tile_cradle_desc': "The birthplace of early humankind. Lush wild grasses sway under an ancient sun. Scattered branches carpet the fertile ground.",
                'tile_lake_name': "The Great Primordial Lake",
                'tile_lake_desc': "A vast, crystal-clear freshwater lake stretching to the horizon. Waves lap against the shore. You can drink clean water here.",
                'tile_wetland_name': "The Reed Marshes & Wetlands",
                'tile_wetland_desc': "Thick reeds and muddy shallows. Dragonflies buzz through the humid mist. Abundant reeds squelch under your feet.",
                'tile_savannah_name': "The Acacia Savannah Grasslands",
                'tile_savannah_desc': "Golden plains dotted with acacia trees. Grazing herds roam the grassland. Abundant edible shrubs grow here.",
                'tile_oasis_name': "The Sunken Palm Oasis",
                'tile_oasis_desc': "A hidden depression sheltering sweet wild date palms and cool groundwater. A tranquil haven from the open wilderness.",
                'tile_ridge_name': "The Obsidian Volcanic Ridge",
                'tile_ridge_desc': "Jagged volcanic rock formation. Sharp black obsidian and rich flint stones lie scattered across the harsh dark terrain.",
                'tile_canyon_name': "The Basalt Echo Canyon",
                'tile_canyon_desc': "Towering walls of volcanic basalt rock. Every footstep echoes powerfully between the cliffs. Heavy stones abound.",
                'tile_cavern_name': "The Great Limestone Cavern Entrance",
                'tile_cavern_desc': "A massive arched cave mouth offering refuge from rain and predators. Deep inside, stalactites drip into darkness.",
                'tile_deep_cave_name': "The Subterranean Cave Chamber",
                'tile_deep_cave_desc': "Total subterranean darkness. Cool underground air and dripping water echo. Perfect natural shelter to kindle a fire and rest.",
                'tile_rainforest_name': "The Primeval Rainforest",
                'tile_rainforest_desc': "Towering prehistoric trees with sprawling canopy foliage. Vines drape down, and wildlife calls resonate from the branches.",
                'tile_delta_name': "The Rushing River Delta",
                'tile_delta_desc': "A wide, fast-moving river branching into the lake. Driftwood, smooth pebbles, and freshwater abound.",
                'tile_predator_name': "The Predator Ridge & Hyena Bluffs",
                'tile_predator_desc': "A high windy plateau overlooking the valley. Animal bones litter the ground. Danger lurks in the rocky crevices.",
                'tile_ash_plains_name': "The Volcanic Ash Plains",
                'tile_ash_plains_desc': "A stark expanse of grey volcanic ash and pumice. The wind howls softly across the barren ground.",
                
                # Extended Contiguous Regions (to ensure no dead-ends)
                'tile_glacier_pass_name': "The Glacial Mountain Pass",
                'tile_glacier_pass_desc': "High freezing mountain pass bordered by ancient ice sheets. Frigid winds howl through the rocky notch.",
                'tile_rapids_name': "The Upper River Rapids",
                'tile_rapids_desc': "Frothing white water cascading over granite boulders. Cool spray fills the air. Clean rushing water to drink.",
                'tile_deep_jungle_name': "The Deep Primeval Jungle",
                'tile_deep_jungle_desc': "Humid, dense jungle canopy with massive hanging strangler figs. Exotic wild berries and heavy hardwood sticks lie everywhere.",
                'tile_steppes_name': "The Northern Hunting Steppes",
                'tile_steppes_desc': "Wide grassy plains stretching beneath rolling clouds. Prehistoric game animals graze peacefully.",
                'tile_foothills_name': "The Volcanic Foothills",
                'tile_foothills_desc': "Dark slopes littered with pumice stone and sulfur deposits. Sharp rocks and flint stones abound.",
                'tile_woodland_name': "The Eastern Woodland Edge",
                'tile_woodland_desc': "Open forest of ancient oak and pine trees. Fallen deadwood and wild fruits carpet the ground.",
                'tile_petrified_name': "The Petrified Forest Ridge",
                'tile_petrified_desc': "Ancient stone logs turned to solid quartz and agate millions of years ago. Extremely hard stone minerals.",
                'tile_shrubland_name': "The Dry Shrubland & Termite Mounds",
                'tile_shrubland_desc': "Sun-baked red earth dotted with giant clay mounds and thorn bushes. Tough roots and dry tinder.",
                'tile_lava_tube_name': "The Dark Lava Tube Tunnel",
                'tile_lava_tube_desc': "Smooth cylindrical volcanic rock tunnel cutting deep through the mountain. Protected from external weather.",
                'tile_crystal_grotto_name': "The Sunken Crystal Grotto",
                'tile_crystal_grotto_desc': "A subterranean sanctuary with crystal-clear underground springs reflecting shimmering minerals.",
                'tile_graveyard_name': "The Prehistoric Bone Graveyard",
                'tile_graveyard_desc': "Ancient washing ground where bones of mammoths and large beasts rest. Abundant large animal bones.",
                'tile_dunes_name': "The Scorching Desert Dunes",
                'tile_dunes_desc': "Rolling golden sand dunes radiating extreme prehistoric heat. Thirst drains rapidly under the blazing sun.",

                # Authentic Prehistoric Geography Additions
                'tile_turkana_lake_name': "Lake Turkana Jade Basin",
                'tile_turkana_lake_desc': "An ancient expansive alkaline lake known as the Jade Sea. Giant prehistoric fish leap from the greenish waters. Clean drinking shallows.",
                'tile_omo_valley_name': "Omo Valley River Crossing",
                'tile_omo_valley_desc': "Fertile floodplains of the Omo River where early hominids flourished. Gateway to the northern desert passes.",
                'tile_olduvai_gorge_name': "Olduvai Gorge Paleolithic Site",
                'tile_olduvai_gorge_desc': "A deep steep-sided geological ravine where layers of early human tools rest. Rich deposits of flint, quartz, and stone choppers.",
                'tile_serengeti_plains_name': "Serengeti Grazing Savannah",
                'tile_serengeti_plains_desc': "Endless golden grasses under the open prehistoric sky. Gazelles and ancient fauna graze peacefully.",
                'tile_rift_highlands_name': "Ngorongoro Volcanic Highlands",
                'tile_rift_highlands_desc': "High cool volcanic ridges overlooking the expansive rift valley. Tough mountain wood and obsidian stones.",
                'tile_bab_el_mandeb_name': "Bab-el-Mandeb Strait Crossing",
                'tile_bab_el_mandeb_desc': "The narrow prehistoric maritime gateway connecting the African Horn to the Arabian Peninsula. Gentle waves lap the shore.",
                'tile_dahlak_reefs_name': "Dahlak Coral Archipelago",
                'tile_dahlak_reefs_desc': "Vibrant shallow prehistoric coral reefs. Clear saltwater with abundant marine life and shellfish.",
                'tile_shell_beach_name': "Prehistoric Shellfish Shoreline",
                'tile_shell_beach_desc': "Pristine sandy beach littered with giant clams, oyster shells, and coastal driftwood.",
                'tile_mangrove_bay_name': "Coastal Mangrove Estuary",
                'tile_mangrove_bay_desc': "Tangled roots of coastal mangrove trees standing in tidal waters. Plentiful reed fibers and smooth stones.",
                'tile_coastal_cliffs_name': "Coral Sandstone Sea Bluffs",
                'tile_coastal_cliffs_desc': "Towering sandstone cliffs battered by sea spray. Provides an expansive vantage point over the ancient ocean.",
                'tile_wadi_feiran_name': "Wadi Feiran Desert Oasis",
                'tile_wadi_feiran_desc': "A miraculous desert corridor nourished by cool underground springs and wild date palms. Fresh drinking water.",
                'tile_mount_sinai_name': "Mount Sinai Granite Peak",
                'tile_mount_sinai_desc': "High red granite peaks jutting into the clear desert sky. Frigid mountain winds whistle through narrow passes.",
                'tile_hejaz_basalt_name': "Hejaz Volcanic Basalt Fields",
                'tile_hejaz_basalt_desc': "Vast plateau of black volcanic lava rocks and ancient basalt craters. Rich in razor-sharp obsidian glass.",
                'tile_jordan_gateway_name': "Jordan Valley Northern Pass",
                'tile_jordan_gateway_desc': "A strategic rift valley gateway leading from the arid deserts toward the fertile northern river basins.",
                'tile_tigris_headwaters_name': "Tigris & Euphrates Headwaters",
                'tile_tigris_headwaters_desc': "Rushing crystal mountain rivers that nourish the Fertile Crescent. Clean freshwater cascades over river stones.",
                'tile_zagros_foothills_name': "Zagros Mountain Foothills",
                'tile_zagros_foothills_desc': "Rolling green foothills dotted with wild oak, pistachio trees, and wild einkorn wheat.",
                'tile_mammoth_steppe_name': "Pleistocene Mammoth Steppe",
                'tile_mammoth_steppe_desc': "Endless cold permafrost steppes stretching beneath sweeping pale skies. Roaming grounds of woolly mammoths.",
                'tile_ice_glacier_name': "Ice Age Glacial Moraine",
                'tile_ice_glacier_desc': "Massive towering walls of ancient glacial ice grinding against bedrock. Frozen snow crunches underfoot.",
                'tile_shanidar_cave_name': "Shanidar Paleolithic Cave",
                'tile_shanidar_cave_desc': "A renowned ancient Neanderthal and early human rock shelter with evidence of floral burials and warm hearths.",
                'tile_cave_art_sanctuary_name': "Paleolithic Cave Art Sanctuary",
                'tile_cave_art_sanctuary_desc': "Deep stone chamber decorated with ochre hand stencils and paintings of running beasts. A sacred ancient haven.",
                'tile_stalactite_chasm_name': "Stalactite Cathedral",
                'tile_stalactite_chasm_desc': "A magnificent subterranean vault where giant limestone pillars drip mineral water in rhythmic harmony.",
                'tile_subterranean_river_name': "Subterranean River of Ancients",
                'tile_subterranean_river_desc': "A hidden underground river carving through solid limestone depths. Cool, drinkable subterranean waters.",
                'tile_bioluminescent_grotto_name': "Bioluminescent Crystal Grotto",
                'tile_bioluminescent_grotto_desc': "A wonder of the underworld illuminated by shimmering glowing mineral crystals and cavern flora.",

                # Items
                'item_wood_stick': "Hardwood Branch",
                'item_flint_stone': "Flint Stone",
                'item_obsidian_shard': "Obsidian Blade Shard",
                'item_wild_berries': "Wild Berries",
                'item_reed_fiber': "Sturdy Reed Fiber",
                'item_animal_bone': "Large Animal Bone",
                'item_spear': "Hardwood Spear",
                'item_obsidian_dagger': "Obsidian Dagger",
                'item_torch': "Fire Torch",
                'item_bone_club': "Bone Club",
                'item_sling': "Stone Sling",
                'item_meat': "Raw Game Meat",
                'item_cooked_meat': "Cooked Roasted Meat",
                'item_guide_book': "Survival Guide Book",
                'item_crafting_book': "Crafting Recipe Book",
                'item_diary': "Journey Diary",

                # Bag & Item Usage Details
                'bag_title': "Satchel / Inventory Bag",
                'bag_opened': "Bag opened. {count} items in bag. Currently holding: {holding}. Use Up and Down arrow keys to browse. Press Enter to hold in hand, press G for item details and usage, or press I to close.",
                'bag_empty': "Your bag is empty. Explore the realm and press Enter on resources to gather them. Press I or Escape to close.",
                'bag_item_held': "Now holding {name} in hand! Attack damage: {dmg}. Press Spacebar in the world to use it.",
                'bag_held_tag': "[Holding in Hand]",
                'weapon_swung_empty': "Used {weapon}! Swung with {dmg} attack power into the air. No creatures within range.",

                'item_details_wood_stick': "Hardwood Branch: Sturdy prehistoric timber gathered from ancient trees. Used to craft spears, fire torches, wooden clubs, and as firewood to ignite and fuel campfires.",
                'item_details_flint_stone': "Flint Stone: Hard sharp-cleaving mineral. Used with wood to strike sparks for fire, and sharp-knapped to craft stone spearheads, scrapers, and slings.",
                'item_details_obsidian_shard': "Obsidian Blade Shard: Razor-sharp black volcanic glass mined from volcanic ridges. Used to craft the deadly, high-damage Obsidian Dagger.",
                'item_details_reed_fiber': "Sturdy Reed Fiber: Tough fibrous plants gathered from wetlands and marshes. Used for binding spearheads, weaving hunting stone slings, and tying fire torches.",
                'item_details_animal_bone': "Large Animal Bone: Dense, heavy bone harvested from hunted prehistoric beasts. Used to craft the crushing Bone Club and primitive tools.",
                'item_details_wild_berries': "Wild Berries: Juicy sweet primeval berries. Eaten directly (Key 1) to restore 25% hunger and 5% health.",
                'item_details_meat': "Raw Game Meat: Fresh high-protein meat harvested from hunting wild beasts. Consumed directly or roasted over campfires.",
                'item_details_cooked_meat': "Cooked Roasted Meat: Savory steak roasted over glowing campfire embers. Restores 65% hunger and 30% health.",
                'item_details_spear': "Hardwood Spear: Formidable prehistoric weapon crafted from wood and flint. Deals 25 piercing attack damage against beasts and predators.",
                'item_details_obsidian_dagger': "Obsidian Dagger: Lethal close-quarters weapon with a razor volcanic glass edge. Deals 35 slashing damage, the highest damage in early eras.",
                'item_details_torch': "Fire Torch: Blazing branch wrapped with reed fiber. Lights pitch-black underground caves, scares away wild beasts, and deals 15 fire damage.",
                'item_details_bone_club': "Heavy Bone Club: Crushing blunt weapon fashioned from prehistoric beast bone. Deals 30 impact damage.",
                'item_details_sling': "Hunting Stone Sling: Flexible woven reed sling. Hurls smooth stones across distance dealing 18 ranged damage.",
                'item_details_guide_book': "Survival Guide Book: In-bag handbook of early human knowledge. Press Enter to browse and listen to survival chapters.",
                'item_details_crafting_book': "Crafting Recipe Book: Blueprint manual of prehistoric metallurgy and tools. Press Enter to hear exact crafting recipes.",
                'item_details_diary': "Journey Diary: Personal chronicle of your life achievements, active era milestones, and epoch progression. Press Enter or J to read.",

                # Interactive Books: Chapter Reader
                'guide_book_title': "Survival Guide Book (Chapter Reader)",
                'guide_ch1_title': "1. Navigation & Direction Facing",
                'guide_ch1_body': "Use Arrow keys to walk across regions. Hold Shift with Arrow keys (Up, Down, Left, Right) to turn facing in place (North 0 deg, South 180 deg, East 90 deg, West 270 deg) without moving.",
                'guide_ch2_title': "2. Real Compass, GPS & Elevation",
                'guide_ch2_body': "Press C or D to hear your exact GPS coordinates, elevation, heading in degrees, and surrounding 4 regions. Press Page Up to climb ridges and Page Down to descend into caves.",
                'guide_ch3_title': "3. Hunting & Spacebar Combat",
                'guide_ch3_body': "Open your bag with I, select any weapon or tool, and press Enter to hold it in hand. Press Spacebar in the world to strike nearby beasts and harvest meat and bone.",
                'guide_ch4_title': "4. Sonar Radar & Lock-On Tracking",
                'guide_ch4_body': "Tap M repeatedly to cycle through all ground resources one by one with distance & direction. Tap A to cycle all live beasts. Press Enter on any scanned item to lock 3D sonar tracking!",
                'guide_ch5_title': "5. Vitals, Fire & Ancestral Revival",
                'guide_ch5_body': "Check vitals with H, U, W, S, T. Press Shift+C or F with 2 flints and 2 sticks to kindle fire. If you ever collapse from wounds, ancestral spirits automatically revive you at the Sacred Hearth with 100% vitals.",
                'guide_ch6_title': "6. Day/Night, Weather & Taming",
                'guide_ch6_body': "Press N to check in-game time and weather. At night, stay near campfires or hold a torch for warmth. Press T near wild canines with raw meat to tame a loyal hunting companion.",

                'craft_book_title': "Crafting Recipe Book (Blueprint Reader)",
                'craft_ch1_title': "1. Hardwood Spear (25 Damage)",
                'craft_ch1_body': "Requires: 2 Hardwood Branches, 1 Flint Stone. Press V to open Crafting Menu. Crafts a long thrusting spear that pierces predators.",
                'craft_ch2_title': "2. Obsidian Dagger (35 Damage)",
                'craft_ch2_body': "Requires: 1 Obsidian Shard, 1 Hardwood Branch, 1 Reed Fiber. Razor-sharp volcanic glass delivering the highest melee damage.",
                'craft_ch3_title': "3. Fire Torch (15 Damage)",
                'craft_ch3_body': "Requires: 1 Hardwood Branch, 1 Reed Fiber, Active Campfire. Illuminates pitch-black caves and frightens beasts.",
                'craft_ch4_title': "4. Heavy Bone Club (30 Damage)",
                'craft_ch4_body': "Requires: 1 Large Animal Bone, 1 Reed Fiber. Carved from mammoth and bear skeletons to crush aggressive beasts.",
                'craft_ch5_title': "5. Hunting Stone Sling (18 Damage)",
                'craft_ch5_body': "Requires: 2 Reed Fibers, 1 Flint Stone. Woven pouch that hurls stones across distance.",
                'craft_ch6_title': "6. Campfire Meat Roasting",
                'craft_ch6_body': "Requires: Active Campfire and Raw Game Meat. Roasts meat into savory Cooked Steaks restoring 65% hunger and 30% health.",
                'craft_ch7_title': "7. Primitive Lean-to Shelter",
                'craft_ch7_body': "Requires: 3 Hardwood Branches, 2 Reed Fibers. Builds a weatherproof camp on your tile where you can rest safely.",

                # Epochs & Quests
                'era_1_name': "Paleolithic Dawn (Old Stone Age)",
                'era_1_desc': "The dawn of human survival. Master fire, craft wooden spears, hunt Pleistocene beasts, and journey across continents.",
                'era_2_name': "Neolithic Revolution (Agricultural Age)",
                'era_2_desc': "Humanity settles the earth. Domesticate the first hunting wolf, build shelters, and harvest the fertile ground.",
                'era_3_name': "Chalcolithic & Bronze Age (Metallurgy)",
                'era_3_desc': "The discovery of metallurgy. Mine copper and volcanic minerals, forge bone clubs, and trade with wandering tribes.",
                'epoch_advanced_title': "EPOCH ADVANCEMENT: {era}",
                'epoch_advanced_announce': "A New Era Dawns! Humanity has advanced into {era}! {desc}",
                'quest_completed_announce': "Milestone Achieved: {title}! Your Journey Diary has been updated.",

                'quest_fire_title': "The First Flame",
                'quest_fire_desc': "Strike your first campfire using 2 flint stones and 2 branches (Shift+C or F).",
                'quest_spear_title': "Weapon of Survival",
                'quest_spear_desc': "Craft a Hardwood Spear in the Crafting Menu (Key V).",
                'quest_hunt_title': "Pleistocene Hunter",
                'quest_hunt_desc': "Attack or hunt any wild beast with your weapon using Spacebar.",
                'quest_roast_title': "Master of the Hearth",
                'quest_roast_desc': "Roast raw meat over a campfire into savory Cooked Meat.",
                'quest_cross_realm_title': "Across the Great Divide",
                'quest_cross_realm_desc': "Cross a Border Gateway into an adjacent realm with Shift + Enter.",
                'quest_tame_wolf_title': "Man's First Friend",
                'quest_tame_wolf_desc': "Tame a wild canine into a Loyal Hunting Companion using meat (Key T).",
                'quest_build_shelter_title': "Primitive Haven",
                'quest_build_shelter_desc': "Build a weatherproof Lean-to Shelter with branches and reed fiber.",
                'quest_craft_dagger_title': "Volcanic Razor",
                'quest_craft_dagger_desc': "Craft a deadly Obsidian Dagger in the Crafting Menu (Key V).",
                'quest_rest_shelter_title': "Restful Solitude",
                'quest_rest_shelter_desc': "Rest inside your shelter to recover stamina and temperature.",
                'quest_mine_minerals_title': "Geological Discovery",
                'quest_mine_minerals_desc': "Gather rich obsidian shards and flint stones from volcanic ridges.",
                'quest_craft_club_title': "Bone Crusher",
                'quest_craft_club_desc': "Craft a Heavy Bone Club from beast skeleton.",
                'quest_trade_elder_title': "First Caravan",
                'quest_trade_elder_desc': "Barter supplies with a wandering tribal elder.",

                # Diary
                'diary_title': "Journey Diary (Safar-nama)",
                'diary_current_era': "Current Historical Epoch: {era}.",
                'diary_progress': "Milestones Achieved: {done} of {total} completed.",
                'diary_active_goals': "Active Era Goals",
                'diary_recent_history': "Recent Achievements",
                'diary_era_ready_advance': "All current epoch goals completed! Ready to advance.",

                # Systems: Cooking, Taming, Shelter, Weather
                'roast_success': "Roasted raw meat over the campfire! Sizzling Cooked Meat added to your satchel.",
                'roast_no_fire': "You need an active campfire nearby to roast meat! Press Shift + C or F with flint and wood to strike fire.",
                'roast_no_meat': "You don't have any raw meat to roast. Hunt beasts or forage to obtain meat.",
                'tame_success': "Offered nutritious meat to the {name}. It sniffs your hand gratefully and is now your Loyal Hunting Companion!",
                'tame_no_beast': "No wild animals within taming range. Approach an animal and press T.",
                'tame_no_food': "You need meat or berries in your satchel to tame wild animals.",
                'shelter_built': "Built a sturdy primitive Lean-to Shelter! You are now sheltered from rain and night winds.",
                'shelter_rested': "Rested peacefully inside your shelter. Stamina, health, and temperature fully restored!",
                'shelter_entered': "Door opened, entered the spacious indoor shelter, and door closed. Explore the interior with Arrow Keys. Press Shift + Enter at the door (0, -2) to exit.",
                'shelter_exited': "Opened the timber door and stepped out into the open wilderness. Door latched shut.",
                'shelter_door_closed_hint': "You are facing the closed timber door. Press Shift + Enter here to open the door and step outside.",
                'shelter_must_walk_to_door': "You must walk to the timber door at the South entrance (0, -2) to open it. Press Shift + Enter when at the door.",
                'shelter_walk_blocked': "You are inside the shelter. Walk to the door at (0, -2) and press Shift + Enter to exit.",
                'shelter_loc_door': "Sturdy Timber Door (0, -2). Press Shift + Enter here to open the door and step outside.",
                'shelter_loc_entry': "Entry Threshold & Woven Mat (0, -1). Cedar planks underfoot.",
                'shelter_loc_hearth': "Central Stone Fireplace & Hearth (0, 0). Golden embers glow brightly, filling the room with comforting warmth.",
                'shelter_loc_bedroll': "Fur Sleeping Bedroll (0, 1). Soft mammoth and wolf pelts gently restore health and stamina.",
                'shelter_loc_meat_rack': "North Wall & Smoked Meat Rack (0, 2). Cured meats hung high, safe from beasts.",
                'shelter_loc_workbench': "Stone Tool Workbench (-1, 0). Flint flakes, knapping stones, and spear shafts.",
                'shelter_loc_herbs': "Fresh Water Pitcher & Herbs (1, 0). Clean mountain spring water and fragrant soothing herbs.",
                'shelter_loc_wall_west': "West Insulated Cedar Wall (-2, 0). Thick logs block the howling outdoor winds.",
                'shelter_loc_wall_east': "East Wall & Peephole Window (2, 0). Narrow gap lets you safely listen to the wild outdoor realm.",
                'shelter_loc_nw': "Warm North-West Sleeping Alcove (-1, 1).",
                'shelter_loc_ne': "North-East Supplies & Baskets Corner (1, 1).",
                'shelter_loc_sw': "South-West Crafting Stash Corner (-1, -1).",
                'shelter_loc_se': "South-East Entry Storage Corner (1, -1).",
                'shelter_wall_hit': "You reached the sturdy shelter wall. The indoor space is safe and warm.",
                'shelter_scan_cycle': "Primitive Lean-to Shelter - {dist} steps {dir}. Press Enter to lock tracking or M for next item.",
                'shelter_name': "Primitive Lean-to Shelter",
                'shelter_req_err': "Building a shelter requires 3 Hardwood Branches and 2 Reed Fibers.",
                'time_report': "Time: {hour:02d}:00 ({phase}). Weather: {weather}. Temperature: {temp}C.",
                'time_morning': "Fresh Morning Sun",
                'time_midday': "High Noon",
                'time_afternoon': "Warm Afternoon",
                'time_dusk': "Evening Dusk",
                'time_night': "Starry Cold Night",
                'weather_clear': "Clear Skies",
                'weather_rain': "Gentle Rain",
                'weather_storm': "Thunderstorm",
                'weather_blizzard': "Howling Blizzard",
                'guide_hint_bag': "Your Survival Guide Book and Crafting Recipe Book are inside your satchel! Press I to open your bag, select either book with arrow keys, and press Enter to browse and listen to chapters in your selected language.",
                'tab_menu_title': "Survival Quick Hub (Tab Key)",
                'tab_menu_quests': "Historical Epoch & Quest Journal",
                'tab_menu_lang': "Change Language (Zuban Tabdeel Karein)",
                'tab_menu_diary': "Listen to Journey Diary (Safarnama)",
                'tab_menu_weather': "Time & Weather Status",
                'tab_menu_updater': "Check for Updates from GitHub",
                'tab_menu_resume': "Resume Journey (Back to World)",
                'menu_updater': "Check for Updates (GitHub)",
                'updater_check': "Check for Updates (GitHub)",
                'updater_install': "Download & Install Latest Update",
                'updater_already_latest': "Your game is already at the latest version ({version}). No update is needed!",
                'page_nav_hint': "Press Tab for Next Page, Shift + Tab for Previous Page, or Escape to return to bag.",
                'page_read_title': "Page {cur} of {total}: {title}",

                # Partner & Family System
                'partner_title': "Clan Companion & Life Partner",
                'partner_talk': "Talk / Share Heartfelt Words",
                'partner_gift': "Offer Gift / Token of Affection",
                'partner_gift_title': "Select Gift from Satchel",
                'partner_meal': "Share a Warm Hearth Meal",
                'partner_role': "Companion Role",
                'partner_family': "Pass Legacy / Cradle Next Generation",
                'tab_menu_partner': "Life Partner & Companion Hub",

                # Realistic Human Needs & Physiology
                'fatigue_report': "Fatigue: {val} percent.",
                'fatigue_alert': "You are utterly exhausted and yawning. Rest upon the soft bedroll inside your shelter!",
                'morale_report': "Morale & Sanity: {val} percent.",
                'social_report': "Social Connection: {val} percent.",
                'full_human_status': "Vitals: Health {health}%, Hunger {hunger}%, Thirst {thirst}%, Stamina {stamina}%, Temp {temp}C, Fatigue {fatigue}%, Morale {morale}%, Social {social}%.",
                'whistle_companion_bark': "You whistled sharply! Your faithful canine companion barks joyfully and bounds to your side.",
                'whistle_companion_none': "You whistled into the wind, but no beast answered. Feed meat to a wild wolf to tame a loyal companion (Key T).",
                'bedroll_sleep': "You curled up upon the warm fur bedroll. Restful slumber embraces you, washing away exhaustion and restoring your strength.",

                # Audio Settings Menu
                'menu_audio_settings': "Audio Settings & Volume Controls",
                'tab_menu_audio_settings': "Audio & Volume Controls",
                'audio_settings_title': "Audio Settings & Volume Controls",
                'audio_master_vol': "Master Game Volume: {val}%",
                'audio_ambient_vol': "Realm Ambience Volume: {val}%",
                'audio_weather_vol': "Dynamic Weather Volume: {val}%",
                'audio_sfx_vol': "Sound Effects (SFX) Volume: {val}%",
                'audio_vol_up': "Increase Volume (+10%)",
                'audio_vol_down': "Decrease Volume (-10%)",

                # Controls Guide
                'controls_guide': (
                    "Complete Controls Guide: "
                    "Arrow keys: Walk in that direction across all regions. "
                    "Shift + Arrow keys (Up, Down, Left, Right): Turn facing direction in place (North 0 deg, South 180 deg, East 90 deg, West 270 deg). "
                    "C or D: Hear Real Compass & GPS coordinates, elevation, heading in degrees, and surrounding regions. "
                    "Spacebar (or X): Use equipped weapon or held item to attack / strike nearby creatures. "
                    "Enter: Pick up ground items, drink water, or lock sonar tracking onto scanned items and animals. "
                    "M: Tap repeatedly to scan/cycle all ground resources one by one with distance & direction. Press Enter on any item to lock tracking! "
                    "A: Tap repeatedly to scan/cycle all live prehistoric animals one by one. Press Enter on any animal to lock tracking! "
                    "Shift + Enter: Cross through Travel Point gateway into adjacent map. "
                    "K: Open Travel Gateways Directory to select destination and start tracking. "
                    "O: Hear distance and compass/relative heading to your tracked target. "
                    "I: Open or Close Inventory Bag. Inside bag, use Up/Down to browse, Enter to hold an item in hand, and G to hear item usage and details. "
                    "V: Open Weapon & Tool Crafting Menu. "
                    "G or F1: Open the Survival Audio Guide. "
                    "Page Up: Climb up steep plateaus. "
                    "Page Down: Descend into caverns and canyons. "
                    "Shift + Page Up: Increase background ambient volume. "
                    "Shift + Page Down: Decrease background ambient volume. "
                    "Home: Increase game master sound volume. "
                    "End: Decrease game master sound volume. "
                    "Shift + C or F: Strike campfire. "
                    "H, U, W, S, T: Check Vitals. "
                    "1: Eat food. "
                    "L: Look around surroundings. "
                    "Q or Escape: Save and exit."
                )
            },

            'ur': {
                # Game Title & Menus
                'game_title': "Journey of Mankind: Safar-e-Insaan",
                'menu_title': "Journey of Mankind - Main Menu",
                'menu_start': "Khail Shuru Karein (Start / Continue)",
                'menu_new_account': "Naya Account Banayein (New Account)",
                'menu_select_account': "Account Chunein (Select Account)",
                'menu_language': "Zaban Badlein (Change Language)",
                'menu_help': "Controls aur Rehnumai (Help & Keys)",
                'menu_quit': "Game Band Karein (Quit)",
                'menu_current_account': "Mojooda Account",
                'none': "Koi nahi",
                'selected': "Chun liya",
                'back': "Wapis",
                'quit_farewell': "Journey of Mankind se kharij ho rahay hain. Allah Hafiz!",
                'lang_switched': "Zaban Urdu par set kar di gayi hai.",

                # Account & Prompts
                'enter_name_prompt': "Apna player naam darj karein",
                'name_instructions': "Naam likh kar Enter dabayein, ya wapis jane ke liay Escape dabayein.",
                'name_empty_err': "Naam khali nahi ho sakta. Dobara likhein.",
                'char_deleted': "Mita diya",
                'account_created': "Account '{name}' kamyabi se ban gaya hai!",
                'account_exists': "Naam '{name}' pehle se mojood hai. Barah-e-karam doosra naam chunein.",
                'no_accounts': "Abhi koi account mojood nahi hai. Pehle naya account banayein.",
                'account_selected': "Account '{name}' select kar liya gaya hai.",

                # Prologue
                'prologue_start': "Genesis Prologue shuru ho raha hai. Skip karne ke liay kisi bhi waqt Spacebar dabayein.",
                'prologue_skipped': "Prologue skip kar diya gaya.",
                'prologue_scene1': "Arbaon saal pehle, be-karaan tareeki mein aik azeem dhamaka hua—Big Bang. Kainaat pheli, sitaray chamkay, aur hamara nizam-e-shamsi wajood mein aaya.",
                'prologue_scene2': "Zameen aag ke sholon se thandi hui. Asman se musladhar barishein barsin, azeem samandar banay, aur pehli zindagi janam lenay lagi.",
                'prologue_scene3': "Aur phir hua insan ka aaghaz! Aik naya wajood, be-hathiyar aur tanha, jis ke seenay mein aqal aur justaju ki rooh phoonki gayi. Aaj aap ka pehla din hai.",
                'prologue_scene4': "Aap ka maqsad: Zinda rehna, aag jalana, dushmanon se ladna, tijarat karna, aur science aur technology ke aakhri ufuq tak pohanchna. Journey of Mankind mein khush amdeed!",

                # Survival Vitals & Health
                'status_report': "Status: Sehat {health}%, Bhook {hunger}%, Pyaas {thirst}%, Tawanai {stamina}%, Darja-e-hararat {temp}C.",
                'health_report': "Sehat: {val} feesad.",
                'health_critical': "Khatra! Aap shadeed zakhmi ya kamzor hain.",
                'hunger_report': "Bhook: {val} feesad.",
                'hunger_alert': "Pait khali hai, khana dhoondein!",
                'thirst_report': "Pyaas: {val} feesad.",
                'thirst_alert': "Gala khushk hai, paani peeyein!",
                'stamina_report': "Tawanai: {val} feesad.",
                'temp_report': "Darja-e-Hararat: {val} degree Celsius.",
                'temp_cold_alert': "Sardi mehsoos ho rahi hai, aag jalayein ya panah lein.",
                'temp_warm_alert': "Paas aag jal rahi hai, jism garam hai.",
                'thirst_quenched': "Aap ki pyaas pehle hi bujhi hui hai.",
                'drank_water': "Thanda aur taaza paani peeya. Pyaas ab {val} feesad hai.",
                'item_not_in_inv': "Yeh cheez inventory mein nahi hai.",
                'ate_berries': "Jangli berries khayein. Bhook kam hui, ab {val} feesad hai.",
                'gathered_items': "Aap ne haasil kiya: {items}.",
                'nothing_to_gather': "Yahan mazeed koi cheez talash karne ko nahi mili.",
                'inv_empty': "Inventory khali hai.",
                'inv_list': "Inventory ki fehrist: {items}.",
                'fire_req_err': "Aag jalane ke liay 2 Flint Pathar aur 2 Lakrian zaroori hain.",
                'fire_made': "Chingari phooti aur aag jal gayi! Garmaish mil rahi hai aur jungle ke janwar door bhaag gaye.",
                'death_msg': "Aap ki maut ho gayi: {reason}. Koshish jari rakhein.",
                'death_reason_starve': "Bhook aur pyaas ki shiddat se.",
                'death_reason_predator': "Qadeem darinday ke hamlay se.",

                # Elevation (Page Up / Page Down)
                'climb_up_success': "Aap dhalwan charh kar unchi pahari par pohanch gaye hain. Oonchai: {level}.",
                'climb_up_blocked': "Aage seedhi chattani deewar hai, yahan se mazeed upar nahi charha ja sakta.",
                'climb_down_success': "Aap dhalwan se utar kar neechi khai ya ghaar mein pohanch gaye hain. Oonchai: {level}.",
                'climb_down_blocked': "Aap bilkul zameeni satah par hain, yahan se mazeed neeche utarna mumkin nahi.",
                'elevation_high': "Unchi Pahari / Tila (Elevation +1)",
                'elevation_ground': "Zameeni Satah (Elevation 0)",
                'elevation_deep': "Gehra Ghaar / Khai (Elevation -1)",
                'elevation_status': "Mojooda oonchai: {elev_name}.",

                # Direction & Compass
                'facing_report': "Aap ka rukh {dir} ({deg} darjay) ki taraf hai. Rukh badalne ke liay Shift + Arrow aur agay chalne ke liay Up arrow dabayein.",
                'turned_to': "Rukh {dir} ({deg} darjay) ki taraf ho gaya.",
                'degrees': "{val} darjay",
                'north': "Shumal (North)",
                'south': "Janoob (South)",
                'east': "Mashriq (East)",
                'west': "Maghrib (West)",
                'compass_title': "Haqeeqi Compass aur GPS Maqaam",
                'compass_coords': "Maqaam: X {x}, Y {y}, Oonchai {elev}.",
                'compass_region': "Mojooda Ilaqa: {area}, {realm}.",
                'compass_heading': "Rukh: {facing} ({deg} darjay).",
                'compass_surroundings': "Aas Paas: Shumal: {north}. Janoob: {south}. Mashriq: {east}. Maghrib: {west}.",
                'compass_target_none': "Tracking: Koi nahi. Janwaron ke liay A aur Travel Points ke liay K dabayein.",
                'compass_target_active': "Manzil: {name} {dist} tiles door {dir} mein hai.",

                # Prehistoric Creatures & Fauna
                'fauna_radar_title': "Qadeem Janwaron ka Radar",
                'fauna_no_beasts': "Is map mein koi zinda janwar mojood nahi hai.",
                'fauna_locked': "{name} ko tracking par laga diya gaya! {dir} ki taraf {dist} qadam. O daba kar samt maloom karein ya audio pings sun kar pohnchein.",
                'fauna_hostile_tag': "(Khatarnak Darinda)",
                'fauna_herbivore_tag': "(Ghaas-khora / Shikar ke qabil)",
                'creature_mammoth_name': "Woolly Mammoth (Qadeem Haathi)",
                'creature_mammoth_desc': "Azeem-ush-shaan qadeem baal-daar haathi jis ke lambay ghoomay huay daanth hain. Is ke qadmon se zameen hil rahi hai.",
                'creature_sabertooth_name': "Sabertooth Tiger (Khatarnak Bhedia-Sher)",
                'creature_sabertooth_desc': "Khatarnak darinda jis ke do lambay talwar numaa khanjar daanth hain. Chattanon ke peechay se ghurra raha hai.",
                'creature_cave_bear_name': "Azeem Ghaar ka Bhaloo (Cave Bear)",
                'creature_cave_bear_desc': "Ghaar ke androon ka azeem reechh. Is ki daharh chattanon se goonjti hai.",
                'creature_hyena_name': "Dire Hyena (Qadeem Lakadbagha)",
                'creature_hyena_desc': "Haddiyan chabane walay darinday jo door se ajeeb aawazain nikal rahay hain.",
                'creature_gazelle_name': "Qadeem Hiran (Gazelle)",
                'creature_gazelle_desc': "Taiz raftaar khubsoorat hiran jo ghaas charh raha hai. Gosht aur chamray ka behtareen zariya.",
                'creature_rhino_name': "Woolly Genda (Woolly Rhino)",
                'creature_rhino_desc': "Bhari bharkam baal-daar qadeem genda jis ke do azeem seengh hain.",
                'creature_lion_name': "Qadeem Ghaar ka Sher (Cave Lion)",
                'creature_lion_desc': "Barafani ilaqon ka azeem sher jo shikar ki talash mein phalta hai.",
                'creature_serpent_name': "Zameen-doz Andha Saanp (Cave Serpent)",
                'creature_serpent_desc': "Ghaaron ki gehraiyon mein rehnay wala azeem saanp jo aawaz aur thar-tharahat se shikar karta hai.",
                'creature_near_warning': "Khatra! {direction} se {name} ki aawaz aa rahi hai! Apna hathiyar tayar karein.",
                'creature_attacked_player': "{name} ne aap par hamla kiya! Aap ko {dmg} nuqsan pohancha.",
                'player_attack_hit': "Aap ne {weapon} se {name} par waar kiya! {dmg} damage diya.",
                'character_respawned': "Aap shadeed thakan ya zakhmon ki wajah se behosh ho gaye! Qadeem roohon ne aap ko markazi aag ke paas mukammal sehat ke sath dobara zinda kar diya.",
                'auto_revived': "Aap shadeed zakhmon ya thakan se behosh ho gaye thay! Qadeem roohon ne aap ko markazi aag ke paas mukammal 100% sehat ke sath foran dobara zinda kar diya.",
                'item_scan_cycle': "{name} ({qty}) - {dir} ki taraf {dist} qadam. Tracking ke liay Enter dabayein ya aglay samaan ke liay M dabayein.",
                'item_scan_water_cycle': "Meethay Paani ka Chashma - {dir} ki taraf {dist} qadam. Tracking ke liay Enter dabayein ya aglay samaan ke liay M dabayein.",
                'item_scan_none': "Is map mein zameen par mazeed koi samaan nahi mila.",
                'item_scan_locked': "{name} tracking par lock ho gaya! {dir} ki taraf {dist} qadam. Audio sonar pings sun kar agay barhein ya O dabayein.",
                'animal_scan_cycle': "{name} {tag} - {dir} ki taraf {dist} qadam. Tracking ke liay Enter dabayein ya aglay janwar ke liay A dabayein.",
                'animal_scan_locked': "{name} tracking par lock ho gaya! {dir} ki taraf {dist} qadam. Audio sonar pings sun kar agay barhein ya O dabayein.",
                'tile_interact_empty': "Yahan zameen par uthanay ke liay koi samaan nahi hai. Qareebi samaan dhoondnay ke liay M dabayein ya janwaron ke liay A dabayein.",

                # Weapons & Crafting
                'craft_menu_title': "Pathar ke Dour ke Hathiyar Craft Karna",
                'craft_equipped': "Hathiyar haath mein: {weapon}.",
                'craft_success': "Kamyabi se tayar hua: {item}! Inventory mein shaamil ho gaya.",
                'craft_missing_mat': "Samaan ki kami hai! Zaroori samaan: {req}.",
                'craft_spear_name': "Lakri ka Neza (Hardwood Spear)",
                'craft_spear_desc': "Lamba nok-daar lakri ka neza jo darindon ko door rakhta hai aur 25 piercing damage daita hai.",
                'craft_spear_req': "2 Lakri ki Tehniyan, 1 Flint Pathar",
                'craft_dagger_name': "Obsidian Chhuri (Obsidian Dagger)",
                'craft_dagger_desc': "Kaalay sheeshay jaisi teez dhaar khanjar. 35 slashing damage daita hai.",
                'craft_dagger_req': "1 Obsidian Tukra, 1 Lakri ki Tehni, 1 Sarkanday ka Resha",
                'craft_torch_name': "Aag ki Mashaal (Fire Torch)",
                'craft_torch_desc': "Jalti hui mashaal jo tareek ghaar ko roshan karti hai aur darindon ko darati hai.",
                'craft_torch_req': "1 Lakri ki Tehni, 1 Sarkanday ka Resha, Jal Rahi Aag",
                'craft_club_name': "Haddi ka Gurj (Bone Club)",
                'craft_club_desc': "Qadeem janwar ki haddi se bana bhari gurj. 30 impact damage daita hai.",
                'craft_club_req': "1 Janwar ki Haddi, 1 Sarkanday ka Resha",
                'craft_sling_name': "Pathar phenkne wali Ghulail (Stone Sling)",
                'craft_sling_desc': "Sarkandon se bani ghulail jo door se pathar phenk kar shikar karti hai. 18 damage daita hai.",
                'craft_sling_req': "2 Sarkanday ke Reshay, 1 Chikna Flint Pathar",

                # Interactive In-Game Audio Guide
                'guide_title': "Safar-e-Insaan Survival Audio Guide",
                'guide_section_nav': (
                    "1. Chalna, Charhai/Utrai, Compass aur Gateways: "
                    "Arrow keys (Up, Down, Left, Right) se un samt mein agay barhein. "
                    "Shift ke sath Arrow keys dabane se (Shift + Up, Down, Left, Right) chalay baghair usi jagah rukh badlein (Shumal 0 darjay, Janoob 180 darjay, Mashriq 90 darjay, Maghrib 270 darjay). "
                    "C ya D daba kar apna Haqeeqi Compass aur GPS maqaam, oonchai, darjay, aur aas paas ke ilaqay sunein. "
                    "Bar bar M dabayein taakay zameen par para tamam samaan aur meethay paani ke chashmay aik aik kar ke sunein. Enter daba kar kisi bhi cheez ko sonar tracking par lagayein! "
                    "Bar bar A dabayein taakay tamam zinda qadeem janwar aik aik kar ke sunein. Enter daba kar kisi bhi janwar ko sonar tracking par lagayein! "
                    "Kisi bhi jagah kharay ho kar Enter ya Spacebar dabayein taakay zameen par pari cheezain utha kar bag mein daal sakein ya paani pee sakein. "
                    "Page Up se unchi dhalwan aur pahari charhein. "
                    "Page Down se gehre ghaaron aur khaiyon mein utrein. "
                    "Background volume barhane ke liay Shift + Page Up aur kam karne ke liay Shift + Page Down dabayein. "
                    "Game master volume barhane ke liay Home aur kam karne ke liay End dabayein. "
                    "X daba kar apnay hathiyar se qareebi janwar par hamla ya shikar karein. "
                    "K daba kar Travel Points Directory kholein aur Enter se manzil ko tracking par lagayein. "
                    "O daba kar manzil ka fasla aur samt sunein. "
                    "Travel Point par pohanch kar Shift + Enter dabayein taakay dosray map mein dakhil ho sakein."
                ),
                'volume_ambient_changed': "Background volume: {val} feesad.",
                'volume_game_changed': "Game volume: {val} feesad.",
                'guide_section_fauna': (
                    "2. Qadeem Janwar aur Animal Radar: "
                    "Is zameen ke tamam 5 maps mein us waqt ke haqeeqi janwar mojood hain: Woolly Mammoth, Sabertooth Sher, Azeem Bhaloo, Dire Hyena, Woolly Genda aur Hiran. "
                    "Bar bar A dabane se tamam zinda janwar faslay aur samt ke sath aik aik kar ke sune ja saktay hain. Enter dabane se tracking lock ho jati hai. "
                    "Audio sonar beeps sun kar ya O daba kar us tak pohnchein, aur paas ja kar X daba kar shikar karein!"
                ),
                'guide_section_weapons': (
                    "3. Hathiyar Craft Karne ka Mukammal Tareeqa: "
                    "Pehla qadam: Jungle aur ilaqon mein ghoom kar M se samaan scan karein aur Enter daba kar zameen se samaan jama karein. "
                    "Ibteda ki wadi se Lakri ki Tehniyan, Pahari se Flint Pathar aur Obsidian, Daldal se Sarkanday ke Reshay, aur Shikar se Haddiyan haasil karein. "
                    "Doosra qadam: Keyboard par V dabayein taakay Crafting Menu khul jaye. "
                    "Teesra qadam: Up aur Down arrow keys se hathiyar chunein (Neza, Obsidian Dagger, Aag ki Mashaal, Haddi ka Gurj, ya Ghulail). "
                    "Choutha qadam: Enter dabayein. Hathiyar ban kar foran aap ke haath mein aa jayega aur aap ki taaqat barh jayegi. "
                    "Paanchwan qadam: Jab koi darinda qareeb aaye to X daba kar us par waar karein!"
                ),
                'guide_section_vitals': (
                    "4. Insani Jism aur Zinda Rehna: "
                    "Sehat, Bhook, Pyaas, Tawanai aur Darja-e-hararat ka khayal rakhein. "
                    "Enter ya Spacebar se jheel aur darya se paani peeyein aur berries chunein. "
                    "1 daba kar berries khayein. "
                    "Shift + C ya F daba kar aag jalayein. "
                    "Dil ki taiz dhadkan kam sehat ki aur pait ki garbar bhook ki nishani hai. "
                    "Agar aap shadeed zakhmi ya behosh ho jayein to qadeem roohein foran aap ko markazi aag ke paas 100 feesad mukammal sehat ke sath khud-bakhud dobara zinda kar dengi."
                ),

                # Map & Navigation
                'way_blocked': "Aage ghana jungle aur dushwar pahaad hain, rasta band hai.",
                'current_location_is': "Aap pohanch gaye hain: {name}. {desc}",
                'look_around_intro': "Aap '{name}' ({elev}) par hain. Rukh: {facing}. Qareeb ke rastay: {neighbors}",

                # Primordial Map Tiles (Authentic Prehistoric Regions)
                'tile_cradle_name': "Ibteda ki Wadi (The Primordial Cradle Valley)",
                'tile_cradle_desc': "Insaniyat ki paidaish ki sarzameen. Qadeem suraj ke neechay sabzah lehlaha raha hai. Zameen par lakrian aur tehniyan bikhri paray hain.",
                'tile_lake_name': "Azeem Qadeem Jheel (The Great Primordial Lake)",
                'tile_lake_desc': "Ufuq tak pheli hui shaffaf meethay paani ki azeem jheel. Lehrein sahil se takra rahi hain. Yahan saaf paani piya ja sakta hai.",
                'tile_wetland_name': "Sarkandon ki Daldal (The Reed Marshes)",
                'tile_wetland_desc': "Ghani sarkanday aur geeli daldali zameen. Hawa mein namee hai aur qadmon ke neechay narm mitti aur reshay hain.",
                'tile_savannah_name': "Sabzah-zaar Savannah (Acacia Savannah)",
                'tile_savannah_desc': "Sonay ki tarha chamakta sabzah jahan acacia ke darakht hain. Qareeb hi zaiqaydaar jangli berries ki jhariyan lagi hain.",
                'tile_oasis_name': "Gehra Nakhlisan (The Sunken Oasis)",
                'tile_oasis_desc': "Kajoor ke jangli darakhton aur thanday chashmay ka pur-sukoon nakhlistan. Jungle ki dhoop se bachne ki aali jagah.",
                'tile_ridge_name': "Aatish-fishani Flint Pahari (Obsidian Volcanic Ridge)",
                'tile_ridge_desc': "Kaalay shishay jaisi teez obsidian aur thos flint pathar bikhray paray hain jin se aag aur pehle hathiyar banaye ja saktay hain.",
                'tile_canyon_name': "Goonjti Hui Basalt Khai (Basalt Echo Canyon)",
                'tile_canyon_desc': "Aatish-fishani pathron ki unchi deewarein. Har aawaz aur qadam ki goonj chattanon se wapis aati hai.",
                'tile_cavern_name': "Azeem Choona Ghaar ka Dahanah (Great Limestone Cavern)",
                'tile_cavern_desc': "Aik qadeem ghaar ka azeem dahanah jo toofan aur darindon se mukammal panah daita hai.",
                'tile_deep_cave_name': "Ghaar ka Gehra Kamra (Subterranean Cave Chamber)",
                'tile_deep_cave_desc': "Mukammal tareeki aur thandi chattanein. Yahan aag jala kar pur-aman qayam kiya ja sakta hai.",
                'tile_rainforest_name': "Qadeem Barani Jungle (Primeval Rainforest)",
                'tile_rainforest_desc': "Azeem-ush-shaan darakht aur latakti hui bailain. Janwaron aur parindon ki aawazain faza mein goonjti hain.",
                'tile_delta_name': "Darya ka Delta (The River Delta)",
                'tile_delta_desc': "Darya jheel se milta hai. Behtay huay paani ki taiz aawaz, tehniyan aur saaf pathar yahan dastiyab hain.",
                'tile_predator_name': "Darindon ki Pahari (The Predator Ridge)",
                'tile_predator_desc': "Hawa chalti hai aur chattanon par haddiyan bikhri hain. Khatra har taraf mojood hai, hoshiyar rahein.",
                'tile_ash_plains_name': "Raakh ke Maidan (Volcanic Ash Plains)",
                'tile_ash_plains_desc': "Kaali raakh aur khamosh hawaon ka wusat maidan.",
                
                # Extended Contiguous Regions (Urdu)
                'tile_glacier_pass_name': "Barafani Pahari Pass (Glacial Mountain Pass)",
                'tile_glacier_pass_desc': "Barafani hawaon ka uncha pahari rasta. Pathreeli chattanein aur thand.",
                'tile_rapids_name': "Darya ki Tez Dhara (Upper River Rapids)",
                'tile_rapids_desc': "Granite pathron par koodta hua shaffaf paani. Thandi phuwaar aur peenay ka meetha paani.",
                'tile_deep_jungle_name': "Ghana Barani Jungle (Deep Primeval Jungle)",
                'tile_deep_jungle_desc': "Ghane darakht aur latakti bailain. Zameen par lakrian aur jangli phal bikhray paray hain.",
                'tile_steppes_name': "Shumali Shikar ke Maidan (Northern Hunting Steppes)",
                'tile_steppes_desc': "Door tak pheli ghaas jahan qadeem janwar azaad ghoomtay hain.",
                'tile_foothills_name': "Aatish-fishani Dhalwanein (Volcanic Foothills)",
                'tile_foothills_desc': "Kaalay pathar aur flint pathron se bhari zameen.",
                'tile_woodland_name': "Mashriqi Jungle ka Kinara (Eastern Woodland Edge)",
                'tile_woodland_desc': "Qadeem sanober ke darakht aur girri hui lakrian.",
                'tile_petrified_name': "Pathraye Huay Jungle ki Pahari (Petrified Forest Ridge)",
                'tile_petrified_desc': "Lakhon saal purani lakri jo pathar ban chuki hai. Sakht minerals ka zakhira.",
                'tile_shrubland_name': "Khushk Jhariyon ka Maidan (Dry Shrubland)",
                'tile_shrubland_desc': "Surkh mitti aur qadeem jhariyan jahan mazboot tehniyan milti hain.",
                'tile_lava_tube_name': "Tareek Lava Tunnel (Dark Lava Tube)",
                'tile_lava_tube_desc': "Pahari ke androon mein qudrati ghaar jo toofan aur barish se panah daiti hai.",
                'tile_crystal_grotto_name': "Chamaktay Paani ki Ghaar (Crystal Grotto)",
                'tile_crystal_grotto_desc': "Zameen ke neechay shaffaf chashmay ki pur-sukoon panahgah.",
                'tile_graveyard_name': "Qadeem Haddiyon ka Qabristan (Bone Graveyard)",
                'tile_graveyard_desc': "Bhari janwaron aur haathiyon ki haddiyon ka muqam. Hathiyar banane ke liay bhari haddiyan.",
                'tile_dunes_name': "Garam Registan ke Teelay (Scorching Desert Dunes)",
                'tile_dunes_desc': "Suraj ki taiz dhoop mein chamakti surkh rait. Pyaas tezi se barhti hai.",

                # Authentic Prehistoric Geography Additions (Urdu)
                'tile_turkana_lake_name': "Turkana Jheel ka Jade Basin",
                'tile_turkana_lake_desc': "Sabz paani ki qadeem azeem jheel. Saaf meetha paani aur machliyon ki aawazain.",
                'tile_omo_valley_name': "Omo Valley Daryai Rasta",
                'tile_omo_valley_desc': "Omo darya ka zarkhez kinarah jahan qadeem insani aabaad-kari ke aasaar miltay hain. Shumali raston ka gateway.",
                'tile_olduvai_gorge_name': "Olduvai Gorge Qadeem Ravine",
                'tile_olduvai_gorge_desc': "Insani tareekh ki azeem tareen khai jahan pathar ke pehle hathiyar aur flint miltay hain.",
                'tile_serengeti_plains_name': "Serengeti Charagah (Serengeti Savannah)",
                'tile_serengeti_plains_desc': "Sonay ki manand ghaas ka be-karaan maidan jahan gazelle aur qadeem janwar ghoomtay hain.",
                'tile_rift_highlands_name': "Ngorongoro Aatish-fishani Balai Ilāqay",
                'tile_rift_highlands_desc': "Wadi ke oopar unchi thandi pahari jahan mazboot lakri aur obsidian pathar bikhray hain.",
                'tile_bab_el_mandeb_name': "Bab-el-Mandeb Samandari Rasta",
                'tile_bab_el_mandeb_desc': "Africa aur Arab ke darmiyan qadeem samandari rasta. Sahil par aahista behti hui lehrein.",
                'tile_dahlak_reefs_name': "Dahlak Coral Chattanain",
                'tile_dahlak_reefs_desc': "Kam-gehray shaffaf samandar mein chamaktay corals aur samandari daulat.",
                'tile_shell_beach_name': "Seepiyon aur Samandari Sahil",
                'tile_shell_beach_desc': "Rait ka shaffaf sahil jahan seepiyan, clams aur lakrian bikhri hain.",
                'tile_mangrove_bay_name': "Mangrove Darakhton ki Khari",
                'tile_mangrove_bay_desc': "Paani mein khari jarein aur sarkandon ke ghane reshay.",
                'tile_coastal_cliffs_name': "Sahili Balai Chattanain (Sea Bluffs)",
                'tile_coastal_cliffs_desc': "Samandari hawaon se goonjti hui baland pahari chattanain.",
                'tile_wadi_feiran_name': "Wadi Feiran Sehrai Nakhlistan",
                'tile_wadi_feiran_desc': "Kajooron aur thanday chashmon ka qudrati nakhlistan jahan meetha paani piya ja sakta hai.",
                'tile_mount_sinai_name': "Koh-e-Sinai Granite Choti",
                'tile_mount_sinai_desc': "Surkh granite ki baland tareen choti. Tez sard hawaien pathron ke darmiyan sarsarati hain.",
                'tile_hejaz_basalt_name': "Hejaz Kaali Basalt Chattanain",
                'tile_hejaz_basalt_desc': "Kaali aatish-fishani lava chattanain jahan shishay jaisa tez obsidian milta hai.",
                'tile_jordan_gateway_name': "Wadi-e-Urdun ka Shumali Rasta",
                'tile_jordan_gateway_desc': "Sehra se zarkhez daryai wadiyon ki taraf janay wala ahem rasta.",
                'tile_tigris_headwaters_name': "Dajlah-o-Furat ke Sar-Chashmay",
                'tile_tigris_headwaters_desc': "Zarkhez Halal ko sairaab karne walay shaffaf darya. Peenay ka meetha paani aur saaf pathar.",
                'tile_zagros_foothills_name': "Koh-e-Zagros ki Dhalwanain",
                'tile_zagros_foothills_desc': "Sabz dhalwanain jahan jangli gandum aur phaldar jhariyan ugi hain.",
                'tile_mammoth_steppe_name': "Barafani Mammoth Steppe",
                'tile_mammoth_steppe_desc': "Sard barafani ghaas ka azeem maidan jahan Woolly Mammoth azaad ghoomtay hain.",
                'tile_ice_glacier_name': "Ice Age Azeem Glacier",
                'tile_ice_glacier_desc': "Lakhon saal purani thos baraf ki unchi deewarein. Qadmon ke neechay baraf ki aawaz.",
                'tile_shanidar_cave_name': "Shanidar Qadeem Ghaar",
                'tile_shanidar_cave_desc': "Qadeem insani panahgah jahan aag ke aasaar aur qudrati chhat mojood hai.",
                'tile_cave_art_sanctuary_name': "Qadeem Naqsh-o-Nigar Ghaar",
                'tile_cave_art_sanctuary_desc': "Deewaron par banay surkh rang ke haath aur janwaron ke aasaar. Pur-aman panahgah.",
                'tile_stalactite_chasm_name': "Stalactite Choona Ghaar",
                'tile_stalactite_chasm_desc': "Chhat se lataktay choonay ke qalam aur tapaktay paani ki aawazain.",
                'tile_subterranean_river_name': "Zameen-doz Behta Darya",
                'tile_subterranean_river_desc': "Ghaar ke androon mein tezi se behta hua shaffaf thanda darya.",
                'tile_bioluminescent_grotto_name': "Chamaktay Crystals ki Ghaar",
                'tile_bioluminescent_grotto_desc': "Tareeki mein roshan chamaktay minerals aur rooh-parwar mahol.",

                # Items
                'item_wood_stick': "Lakri ki Tehni",
                'item_flint_stone': "Flint Pathar",
                'item_obsidian_shard': "Obsidian Pathar ka Tukra",
                'item_wild_berries': "Jangli Berries",
                'item_reed_fiber': "Sarkanday ka Resha",
                'item_animal_bone': "Janwar ki Badi Haddi",
                'item_spear': "Lakri ka Neza",
                'item_obsidian_dagger': "Obsidian Dagger",
                'item_torch': "Aag ki Mashaal",
                'item_bone_club': "Haddi ka Gurj",
                'item_sling': "Pathar ki Ghulail",
                'item_meat': "Kacha Gosht",
                'item_cooked_meat': "Bhuna hua Gosht",
                'item_guide_book': "Survival Guide Kitab",
                'item_crafting_book': "Dastkari Recipe Kitab",
                'item_diary': "Safar-nama (Journey Diary)",

                # Bag & Item Usage Details
                'bag_title': "Basta / Samaan ka Bag",
                'bag_opened': "Bag khul gaya. Bag mein {count} cheezain hain. Haath mein pakra hua: {holding}. Up aur Down arrow keys se browse karein. Haath mein pakarnay ke liay Enter dabayein, tafseel aur istemal ke liay G dabayein, ya band karne ke liay I dabayein.",
                'bag_empty': "Aap ka bag khali hai. Map par ghoom kar zameen se samaan uthanay ke liay Enter dabayein. Band karne ke liay I ya Escape dabayein.",
                'bag_item_held': "{name} haath mein pakar liya! Hamla taaqat {dmg} hai. Chalane ke liay bahar Spacebar dabayein.",
                'bag_held_tag': "[Haath mein pakra hua]",
                'weapon_swung_empty': "{weapon} chalaya! {dmg} hamla taaqat ke sath hawa mein waar kiya. Qareeb koi darinda nahi mila.",

                'item_details_wood_stick': "Lakri ki Tehni: Darakhton se mili mazboot qadeem lakri. Is se neza, aag ki mashaal, aur auzaar banaye jatay hain, aur yeh aag jalane aur barqarar rakhne ke kaam aati hai.",
                'item_details_flint_stone': "Flint Pathar: Sakht aur chingaari dainay wala pathar. Isay lakri ke sath ragar kar aag jalai jati hai, aur is se dhaar-daar neza, auzaar aur ghulail banti hai.",
                'item_details_obsidian_shard': "Obsidian Tukra: Pahaadon se milnay wala kaala teez tareen volcanic sheesha. Is se nihayat qaatil aur teez dhaar Obsidian Chhuri (Dagger) banti hai.",
                'item_details_reed_fiber': "Sarkanday ka Resha: Daldal se milnay walay mazboot reshay. Yeh neza baandhnay, ghulail bun-nay aur mashaal baandhnay ke kaam aatay hain.",
                'item_details_animal_bone': "Janwar ki Haddi: Shikar kiay gaye qadeem janwaron ki bhari haddi. Is se dushmanon ko torna wala Haddi ka Gurj (Bone Club) aur auzaar bantay hain.",
                'item_details_wild_berries': "Jangli Berries: Raseelay meethay jungle ke phal. Inhein khaanay se 25 feesad bhook kam hoti hai aur 5 feesad sehat bahaal hoti hai.",
                'item_details_meat': "Kacha Gosht: Shikar se mila taaza gosht. Kacha khayein ya aag par bhon kar khayein.",
                'item_details_cooked_meat': "Bhuna hua Gosht: Aag ke angaron par paka hua mazaydar gosht. 65 feesad bhook aur 30 feesad sehat bahaal karta hai.",
                'item_details_spear': "Lakri ka Neza: Lakri aur flint pathar se bana lamba dhaar-daar neza. Darindon par 25 piercing damage daita hai.",
                'item_details_obsidian_dagger': "Obsidian Chhuri: Kaalay sheeshay se bana nihayat teez khanjar. 35 slashing damage daita hai jo sab se taqatwar waar karta hai.",
                'item_details_torch': "Aag ki Mashaal: Jalti hui mashaal. Gehre tareek ghaaron ko roshan karti hai, darindon ko darati hai, aur 15 aag ka damage daiti hai.",
                'item_details_bone_club': "Haddi ka Gurj: Janwar ki bhari haddi se bana gurj. Darindon par 30 impact damage daita hai.",
                'item_details_sling': "Pathar ki Ghulail: Sarkandon se bani ghulail. Door se pathar phenk kar 18 ranged damage daiti hai.",
                'item_details_guide_book': "Survival Guide Kitab: Zinda rehne ki rehnuma kitab. Sun-nay ke liay Enter dabayein.",
                'item_details_crafting_book': "Dastkari Recipe Kitab: Hathiyar aur auzaar banane ke nuskhey. Nuskhey sun-nay ke liay Enter dabayein.",
                'item_details_diary': "Safar-nama (Journey Diary): Aap ke tareekhi kaarnamay aur dor ke ahdaaf ka record. Sun-nay ke liay Enter ya J dabayein.",

                # Interactive Books: Chapter Reader (Urdu)
                'guide_book_title': "Survival Guide Kitab (Chapter Reader)",
                'guide_ch1_title': "1. Chalna aur Rukh Badalna",
                'guide_ch1_body': "Arrow keys se agay barhein. Chalay baghair usi jagah rukh badalne ke liay Shift + Arrow keys (Up, Down, Left, Right) dabayein (Shumal 0, Janoob 180, Mashriq 90, Maghrib 270 darjay).",
                'guide_ch2_title': "2. Haqeeqi Compass, GPS aur Oonchai",
                'guide_ch2_body': "C ya D se apna GPS maqaam, oonchai, darjay aur gird-o-nawash ke 4 ilaqay sunein. Pahari charhnay ke liay Page Up aur ghaaron mein utarnay ke liay Page Down dabayein.",
                'guide_ch3_title': "3. Shikar aur Spacebar Combat",
                'guide_ch3_body': "Bag khol kar Enter se hathiyar haath mein pakrein. Bahar Spacebar se qareebi janwaron par waar karein aur gosht aur haddi haasil karein.",
                'guide_ch4_title': "4. Sonar Radar aur Lock Tracking",
                'guide_ch4_body': "M se zameen ka samaan aik aik kar ke sunein, A se tamam janwar sunein. Kisi par bhi Enter daba kar 3D sonar tracking lagayein!",
                'guide_ch5_title': "5. Sehat, Aag aur Dobara Zinda Hona",
                'guide_ch5_body': "H, U, W, S, T se vitals sunein. Shift+C ya F se 2 flint aur 2 lakriyon se aag jalayein. Behosh hone par qadeem roohein markazi aag par 100% sehat ke sath khud revive karti hain.",
                'guide_ch6_title': "6. Din/Raat, Mausam aur Janwar Paalna",
                'guide_ch6_body': "N se waqt aur mausam sunein. Raat ko aag ke paas rahein ya mashaal pakrein. Bheriye ya gazelle ke paas T daba kar gosht khilayein aur apna Shikari Saathi banayein.",

                'craft_book_title': "Dastkari Recipe Kitab (Blueprint Reader)",
                'craft_ch1_title': "1. Lakri ka Neza (25 Damage)",
                'craft_ch1_body': "Zaroorat: 2 Lakri ki Tehniyan, 1 Flint Pathar. V daba kar craft karein. Lamba dhaar-daar neza banta hai jo darindon ka seena cheer daita hai.",
                'craft_ch2_title': "2. Obsidian Chhuri (35 Damage)",
                'craft_ch2_body': "Zaroorat: 1 Obsidian Tukra, 1 Tehni, 1 Sarkanday ka Resha. Kaalay sheeshay ka teez khanjar jo sab se taqatwar waar karta hai.",
                'craft_ch3_title': "3. Aag ki Mashaal (15 Damage)",
                'craft_ch3_body': "Zaroorat: 1 Tehni, 1 Resha, Jal Rahi Aag. Tareek ghaaron ko roshan karti hai aur darindon ko darati hai.",
                'craft_ch4_title': "4. Haddi ka Gurj (30 Damage)",
                'craft_ch4_body': "Zaroorat: 1 Badi Haddi, 1 Resha. Mammoth aur bhaloo ki haddi se bana bhari gurj.",
                'craft_ch5_title': "5. Pathar ki Ghulail (18 Damage)",
                'craft_ch5_body': "Zaroorat: 2 Reshay, 1 Flint Pathar. Door se shikar karne wali ghulail.",
                'craft_ch6_title': "6. Aag par Gosht Bhonna",
                'craft_ch6_body': "Zaroorat: Jal Rahi Aag aur Kacha Gosht. Kacha gosht aag par bhon kar 65% bhook aur 30% sehat bahaal karne wala gosht banta hai.",
                'craft_ch7_title': "7. Chhappar / Primitive Camp",
                'craft_ch7_body': "Zaroorat: 3 Tehniyan, 2 Reshay. Barish aur toofan se mehfooz chhappar banta hai jahan aaraam kiya ja sakta hai.",

                # Epochs & Quests (Urdu)
                'era_1_name': "Qadeem Stone Age (Ibteda-e-Insaniyat)",
                'era_1_desc': "Insaniyat ka aaghaz. Aag jalayein, hathiyar banayein, qadeem janwaron ka shikar karein aur azeem maps ka safar karein.",
                'era_2_name': "Neolithic Revolution (Kheti-baari aur Janwar Paalna)",
                'era_2_desc': "Insan zameen par aabaad hota hai. Bheriye ko apna sathi banayein, chhappar banayein aur zameen ki nematon ko chunein.",
                'era_3_name': "Bronze Age (Madniyat aur Kansa)",
                'era_3_desc': "Dhaat ki daryaft. Pahaadon se minerals dhoondein, haddi ke gurj banayein aur doosray qabeelon se tijarat karein.",
                'epoch_advanced_title': "DOR KI TARAQQI: {era}",
                'epoch_advanced_announce': "Naya Dor Shuru Hua! Insaniyat ne taraqqi kar ke {era} mein qadam rakh diya hai! {desc}",
                'quest_completed_announce': "Kamyabi Haasil: {title}! Aap ka Safar-nama (Journey Diary) update ho gaya hai.",

                'quest_fire_title': "Pehli Aag",
                'quest_fire_desc': "2 flint pathar aur 2 lakriyon se apni pehli aag jalayein (Shift+C ya F).",
                'quest_spear_title': "Baqaa ka Hathiyar",
                'quest_spear_desc': "Crafting Menu (V) mein Lakri ka Neza banayein.",
                'quest_hunt_title': "Qadeem Shikari",
                'quest_hunt_desc': "Spacebar daba kar kisi bhi qadeem darinday par hamla ya shikar karein.",
                'quest_roast_title': "Aag ka Ustaad",
                'quest_roast_desc': "Aag par kacha gosht bhon kar mazaydar paka hua gosht banayein.",
                'quest_cross_realm_title': "Azeem Sarhad Paar",
                'quest_cross_realm_desc': "Shift + Enter daba kar Border Gateway se doosray continent dakhil hon.",
                'quest_tame_wolf_title': "Insan ka Pehla Dost",
                'quest_tame_wolf_desc': "Gosht khila kar jungle ke janwar ko apna Wafadar Shikari Saathi banayein (Key T).",
                'quest_build_shelter_title': "Qadeem Panahgah",
                'quest_build_shelter_desc': "Lakriyon aur reshon se apna Chhappar ya Khema banayein.",
                'quest_craft_dagger_title': "Aatish-fishani Khanjar",
                'quest_craft_dagger_desc': "V menu se teez tareen Obsidian Dagger banayein.",
                'quest_rest_shelter_title': "Pur-sukoon Aaraam",
                'quest_rest_shelter_desc': "Chhappar ke andar aaraam kar ke tawanai aur hararat bahaal karein.",
                'quest_mine_minerals_title': "Madniyat ki Daryaft",
                'quest_mine_minerals_desc': "Pahariyon se obsidian aur qeemti pathar jama karein.",
                'quest_craft_club_title': "Haddi ka Tor",
                'quest_craft_club_desc': "Janwar ki haddi se bhari gurj banayein.",
                'quest_trade_elder_title': "Pehla Karwan",
                'quest_trade_elder_desc': "Doosray qabeelay ke buzurg se samaan ka tabadla (tijarat) karein.",

                # Diary (Urdu)
                'diary_title': "Safar-nama (Journey Diary)",
                'diary_current_era': "Mojooda Tareekhi Dor: {era}.",
                'diary_progress': "Mukammal Ahdaaf: {total} mein se {done} pooray huay.",
                'diary_active_goals': "Mojooda Dor ke Ahdaaf",
                'diary_recent_history': "Taza Tareen Kaarnamay",
                'diary_era_ready_advance': "Is dor ke tamam ahdaaf pooray ho chukay hain! Aglay dor mein jane ke liay tayyar.",

                # Systems: Cooking, Taming, Shelter, Weather (Urdu)
                'roast_success': "Aag par kacha gosht bhon liya! Mazaydar bhuna hua gosht bag mein shaamil ho gaya.",
                'roast_no_fire': "Gosht bhonnay ke liay qareeb aag ka jalna zaroori hai! Shift+C ya F se aag jalayein.",
                'roast_no_meat': "Aap ke bag mein bhonnay ke liay kacha gosht nahi hai. Shikar karein.",
                'tame_success': "Aap ne {name} ko gosht khilaya. Us ne aap ka haath soongha aur aap ka Wafadar Shikari Saathi ban gaya!",
                'tame_no_beast': "Qareeb koi janwar nahi mila jise paala ja sakay. Janwar ke qareeb ja kar T dabayein.",
                'tame_no_food': "Janwar ko paalne ke liay aap ke bag mein gosht ya phal hona zaroori hai.",
                'shelter_built': "Kamyabi se Chhappar (Shelter) bana liya! Ab aap toofan aur sardi se mehfooz hain.",
                'shelter_rested': "Chhappar mein pur-sukoon aaraam kiya. Tawanai, sehat aur hararat 100% bahaal ho gayi!",
                'shelter_entered': "Darwaza khula, aap bari panahgah mein dakhil huay, aur darwaza band hua. Andar move karne ke liye Arrow keys use karein. Bahar jane ke liye darwazay (0, -2) par ja kar Shift + Enter dabayein.",
                'shelter_exited': "Darwaza khola aur khuli fiza mein bahar aa gaye. Darwaza band hua.",
                'shelter_door_closed_hint': "Aap band darwazay ke samnay hain. Bahar jane ke liye yahan Shift + Enter dabayein.",
                'shelter_must_walk_to_door': "Bahar nikalnay ke liye pehle darwazay (0, -2) par jayein, phir Shift + Enter dabayein.",
                'shelter_walk_blocked': "Aap panahgah ke andar hain. Darwazay (0, -2) par ja kar Shift + Enter dabayein.",
                'shelter_loc_door': "Panahgah ka Mazboot Darwaza (0, -2). Bahar nikalnay ke liye yahan Shift + Enter dabayein.",
                'shelter_loc_entry': "Dakhlay ka Farsh aur Mat (0, -1). Lakri ke takhtay.",
                'shelter_loc_hearth': "Markazi Patharon ka Alao aur Choolha (0, 0). Angaray chamak rahay hain aur poora kamra garm hai.",
                'shelter_loc_bedroll': "Narm Khaal ka Bistar (0, 1). Yahan aaraam karne se sehat aur stamina bahaal hotay hain.",
                'shelter_loc_meat_rack': "Shimali Deewar aur Sukha Gosht (0, 2). Janwaron se mehfooz khushk gosht.",
                'shelter_loc_workbench': "Pathar ke Ozaar aur Workbench (-1, 0). Flint ke tukray aur lakri ke bhalay.",
                'shelter_loc_herbs': "Saaf Paani ka Bartan aur Jari Bootiyan (1, 0). Peenay ka saaf paani aur khushbudaar bootiyan.",
                'shelter_loc_wall_west': "Maghribi Mazboot Deewar (-2, 0). Bahar ki sakht sardi aur hawa andar nahi aa sakti.",
                'shelter_loc_wall_east': "Mashriqi Deewar aur Roshan-daan (2, 0). Bahar ke mausam par nazar rakhnay ke liye.",
                'shelter_loc_nw': "Shimal-Maghrib ka Garm Kona (-1, 1).",
                'shelter_loc_ne': "Shimal-Mashriq ka Saman ka Kona (1, 1).",
                'shelter_loc_sw': "Janoob-Maghrib Lakriyon ka Zakhira (-1, -1).",
                'shelter_loc_se': "Janoob-Mashriq Dakhlay ka Kona (1, -1).",
                'shelter_wall_hit': "Aap panahgah ki mazboot lakri ki deewar tak pohanch gaye hain. Andar ka mahol mehfooz aur garm hai.",
                'shelter_scan_cycle': "Kacha Chhappar (Shelter) - {dir} ki taraf {dist} qadam. Tracking ke liay Enter dabayein ya aglay samaan ke liay M dabayein.",
                'shelter_name': "Kacha Chhappar (Shelter)",
                'shelter_req_err': "Chhappar banane ke liay 3 Lakri ki Tehniyan aur 2 Sarkanday ke Reshay darkaar hain.",
                'time_report': "Waqt: {hour:02d}:00 ({phase}). Mausam: {weather}. Darja-e-hararat: {temp} degree.",
                'time_morning': "Subah ki Taaza Dhoop",
                'time_midday': "Do-pahar",
                'time_afternoon': "Garam Se-pahar",
                'time_dusk': "Shaam ka Dhundlaka",
                'time_night': "Sard Tareek Raat",
                'weather_clear': "Saaf Aasman",
                'weather_rain': "Halki Barish",
                'weather_storm': "Garaj Chamak ka Toofan",
                'weather_blizzard': "Sard Barafani Toofan",
                'guide_hint_bag': "Aap ki Survival Guide Book aur Crafting Recipe Book aap ke bag mein mojood hain! Bag kholnay ke liay I dabayein, arrow keys se book chunein aur Enter daba kar apni zuban mein suniye.",
                'tab_menu_title': "Survival Quick Hub (Tab Key)",
                'tab_menu_quests': "Tareekhi Dor aur Ahdaaf (Quests Journal)",
                'tab_menu_lang': "Zuban Tabdeel Karein (Change Language)",
                'tab_menu_diary': "Safarnama Suniye (Journey Diary)",
                'tab_menu_weather': "Waqt aur Mausam ki Maloomat",
                'tab_menu_updater': "GitHub se Nayi Update Check Karein",
                'tab_menu_resume': "Game mein Wapsi (Resume)",
                'menu_updater': "GitHub Update Check Karein",
                'updater_check': "GitHub se Update Check Karein",
                'updater_install': "Taza Tareen Update Download & Install Karein",
                'updater_already_latest': "Aap ke paas pehle se taza tareen version ({version}) mojood hai. Kisi update ki zaroorat nahi!",
                'page_nav_hint': "Aglay page ke liay Tab, pichlay page ke liay Shift + Tab, aur wapsi ke liay Escape dabayein.",
                'page_read_title': "Page {cur} az {total}: {title}",

                # Partner & Family System
                'partner_title': "Hamsafar aur Qabila Sathi",
                'partner_talk': "Dil ki Baat / Guftagoo",
                'partner_gift': "Tohfa Dein / Pyar ka Izhar",
                'partner_gift_title': "Bag se Tohfa Chunein",
                'partner_meal': "Choolhay ka Garm Khana Share Karein",
                'partner_role': "Sathi ka Kirdar",
                'partner_family': "Insani Nasl ka Aaghaz / Bachay ki Pedaish",
                'tab_menu_partner': "Hamsafar aur Sathi Menu",

                # Realistic Human Needs & Physiology
                'fatigue_report': "Thakawat: {val} feesad.",
                'fatigue_alert': "Aap shadeed thakawat aur neend se nidhal hain. Panahgah ke garm bistar par aaram karein!",
                'morale_report': "Hosla aur Sukoon: {val} feesad.",
                'social_report': "Insani Rabta: {val} feesad.",
                'full_human_status': "Mukammal Status: Sehat {health}%, Bhook {hunger}%, Pyaas {thirst}%, Tawanai {stamina}%, Hararat {temp}C, Thakawat {fatigue}%, Hosla {morale}%, Rabta {social}%.",
                'whistle_companion_bark': "Aap ne tez seeti bajayi! Aap ka wafadar kutta khushi se bhonk kar daurta hua aap ke qareeb aa gaya.",
                'whistle_companion_none': "Aap ne seeti bajayi, par abhi koi sathi nahi mila. Kacha gosht khila kar bheriye ko apna sathi banayein (Key T).",
                'bedroll_sleep': "Aap garm khaal ke bistar par so gaye. Gehri meethi neend ne tamam thakawat door kar di aur jism tawaana ho gaya.",

                # Audio Settings Menu
                'menu_audio_settings': "Awaz aur Volume ki Settings",
                'tab_menu_audio_settings': "Awaz aur Volume Controls",
                'audio_settings_title': "Awaz aur Volume Controls",
                'audio_master_vol': "Master Game Volume: {val}%",
                'audio_ambient_vol': "Mahol Ambience Volume: {val}%",
                'audio_weather_vol': "Mausam ki Awaz ka Volume: {val}%",
                'audio_sfx_vol': "Sound Effects (SFX) Volume: {val}%",
                'audio_vol_up': "Awaz Barhayein (+10%)",
                'audio_vol_down': "Awaz Kam Karein (-10%)",

                # Controls Guide
                'controls_guide': (
                    "Mukammal Controls Guide: "
                    "Arrow keys: Un samt mein agay barhna. "
                    "Shift + Arrow keys (Up, Down, Left, Right): Chalay baghair usi jagah rukh badalna (Shumal 0 darjay, Janoob 180 darjay, Mashriq 90 darjay, Maghrib 270 darjay). "
                    "C ya D: Haqeeqi Compass aur GPS maqaam, unchai, darjay, aur aas paas ke ilaqay sunna. "
                    "Spacebar (ya X): Haath mein pakra hathiyar ya cheez chalana aur qareebi darindon par hamla karna. "
                    "Enter: Zameen par pari cheezain uthana ya paani peena; ya scanned cheez/janwar par tracking lock karna. "
                    "M: Bar bar M dabayein taakay zameen par para tamam samaan aik aik kar ke sunein. Enter daba kar kisi bhi cheez ko tracking par lagayein! "
                    "A: Bar bar A dabayein taakay tamam qadeem janwar aik aik kar ke sunein. Enter daba kar kisi bhi janwar ko tracking par lagayein! "
                    "Shift + Enter: Travel Point se dosray map mein dakhil hona. "
                    "K: Travel Points Directory khol kar manzil chun-na aur tracking lagana. "
                    "O: Manzil ka fasla (tiles) aur samt sunna. "
                    "I: Bag kholna ya band karna. Bag ke andar Up/Down se browse karein, Enter se cheez haath mein pakrein, aur G se us ka istemal aur tafseel sunein. "
                    "V: Hathiyar aur Tools Craft karne ka Menu kholna. "
                    "G ya F1: Survival Audio Guide sunna. "
                    "Page Up: Unchi pahariyon par charhna. "
                    "Page Down: Gehre ghaaron mein utarna. "
                    "Shift + Page Up: Background volume barhana. "
                    "Shift + Page Down: Background volume kam karna. "
                    "Home: Game master sound volume barhana. "
                    "End: Game master sound volume kam karna. "
                    "Shift + C ya F: Aag jalana. "
                    "H, U, W, S, T: Sehat, Bhook, Pyaas, Tawanai aur Darja-e-hararat sunna. "
                    "1: Khana khana. "
                    "L: Apnay gird-o-nawash ka jaiza lena. "
                    "Q ya Escape: Save aur exit."
                )
            },

            'es': {
                'game_title': "Journey of Mankind: Odisea Humana",
                'menu_title': "Journey of Mankind - Menú Principal",
                'menu_start': "Iniciar Juego / Continuar",
                'menu_new_account': "Crear Nueva Cuenta",
                'menu_select_account': "Seleccionar Cuenta",
                'menu_language': "Cambiar Idioma",
                'menu_help': "Controles y Guía",
                'menu_quit': "Salir del Juego",
                'menu_current_account': "Cuenta Actual",
                'none': "Ninguno",
                'selected': "Seleccionado",
                'back': "Atrás",
                'quit_farewell': "Saliendo de Journey of Mankind. ¡Hasta pronto!",
                'lang_switched': "Idioma cambiado a Español.",
                'bag_title': "Bolsa de Inventario",
                'bag_opened': "Bolsa abierta. {count} objetos. En mano: {holding}. Usa flechas para navegar. Enter para sostener, G para detalles, I para cerrar.",
                'bag_empty': "Tu bolsa está vacía. Presiona Enter en el suelo para recoger recursos.",
                'bag_item_held': "¡Ahora sostienes {name} en mano! Daño de ataque: {dmg}. Presiona Espacio para usarlo.",
                'bag_held_tag': "[En Mano]",
                'weapon_swung_empty': "¡Usaste {weapon}! Blandido con {dmg} de fuerza. No hay bestias cerca.",
                'diary_title': "Diario de Viaje (Crónica)",
                'diary_current_era': "Época Histórica Actual: {era}.",
                'diary_progress': "Hitos Cumplidos: {done} de {total}.",
                'era_1_name': "Amanecer Paleolítico (Edad de Piedra)",
                'era_2_name': "Revolución Neolítica (Agricultura y Domesticación)",
                'era_3_name': "Edad del Bronce (Metalurgia)",
                'north': "Norte", 'south': "Sur", 'east': "Este", 'west': "Oeste"
            },

            'fr': {
                'game_title': "Journey of Mankind: L'Odyssée Humaine",
                'menu_title': "Journey of Mankind - Menu Principal",
                'menu_start': "Commencer / Continuer",
                'menu_new_account': "Créer un Nouveau Compte",
                'menu_select_account': "Sélectionner un Compte",
                'menu_language': "Changer de Langue",
                'menu_help': "Commandes et Aide",
                'menu_quit': "Quitter le Jeu",
                'menu_current_account': "Compte Actuel",
                'none': "Aucun",
                'selected': "Sélectionné",
                'back': "Retour",
                'quit_farewell': "Sortie de Journey of Mankind. À bientôt !",
                'lang_switched': "Langue changée en Français.",
                'bag_title': "Sacoche d'Inventaire",
                'bag_opened': "Sac ouvert. {count} objets. En main : {holding}. Utilisez les flèches pour naviguer. Entrée pour équiper, G pour détails, I pour fermer.",
                'bag_empty': "Votre sac est vide. Appuyez sur Entrée au sol pour ramasser des ressources.",
                'bag_item_held': "Vous tenez maintenant {name} en main ! Dégâts : {dmg}. Espace pour frapper.",
                'bag_held_tag': "[En Main]",
                'weapon_swung_empty': "Arme {weapon} utilisée avec {dmg} de puissance. Aucune bête à portée.",
                'diary_title': "Journal de Voyage (Chronique)",
                'diary_current_era': "Époque Historique Actuelle : {era}.",
                'diary_progress': "Objectifs Accomplis : {done} sur {total}.",
                'era_1_name': "Aube Paléolithique (Âge de Pierre)",
                'era_2_name': "Révolution Néolithique (Agriculture)",
                'era_3_name': "Âge du Bronze (Métallurgie)",
                'north': "Nord", 'south': "Sud", 'east': "Est", 'west': "Ouest"
            },

            'ar': {
                'game_title': "Journey of Mankind: Rihlat Al-Insan",
                'menu_title': "Journey of Mankind - Al-Qayimah Al-Raeesiyah",
                'menu_start': "Ibd'a Al-Liba (Start / Continue)",
                'menu_new_account': "Insha'a Hisab Jadeed (New Account)",
                'menu_select_account': "Ikhtiyar Hisab (Select Account)",
                'menu_language': "Taghyeer Al-Lughah (Change Language)",
                'menu_help': "Al-Tahakkum wal Irshad (Help & Controls)",
                'menu_quit': "Khuruj (Quit)",
                'menu_current_account': "Al-Hisab Al-Hali",
                'none': "La Shay",
                'selected': "Tam Al-Ikhtiyar",
                'back': "Rujoo",
                'quit_farewell': "Maa Al-Salamah fi Rihlat Al-Insan!",
                'lang_switched': "Tam taghyeer al-lughah ila Al-Arabiyya.",
                'bag_title': "Haqeebat Al-Ghanimah (Satchel)",
                'bag_opened': "Futihat al-haqeebah. Feeha {count} aghrad. Fi yadak: {holding}. As-hum li-tataffah. Enter lil-imsak, G lit-tafaseel, I lil-ighlaq.",
                'bag_empty': "Al-haqeebah farighah. Ighgat Enter ala al-ard li-jam'a al-mawarid.",
                'bag_item_held': "Amsakta {name} bi-yadak! Quwwat al-hamla: {dmg}. Ighgat Space fil-alam li-istikhdamih.",
                'bag_held_tag': "[Bi-Yadak]",
                'weapon_swung_empty': "Darabta bi-{weapon}! Quwwah {dmg}. La yoojad haywanat qareebah.",
                'diary_title': "Mudhakkirat Al-Rihlah (Safar-nama)",
                'diary_current_era': "Al-Asr Al-Tareekhi Al-Hali: {era}.",
                'diary_progress': "Al-Ahdaf Al-Munjazah: {done} min {total}.",
                'era_1_name': "Asr Al-Hajar Al-Qadeem (Paleolithic)",
                'era_2_name': "Al-Thawrah Al-Zira'iyyah (Neolithic)",
                'era_3_name': "Asr Al-Bronz (Bronze Age)",
                'north': "Shamal", 'south': "Janoob", 'east': "Sharq", 'west': "Gharb"
            },

            'hi': {
                'game_title': "Journey of Mankind: Manav Yatra",
                'menu_title': "Journey of Mankind - Mukhya Menu",
                'menu_start': "Khel Shuru Karein (Start / Continue)",
                'menu_new_account': "Naya Account Banayein (New Account)",
                'menu_select_account': "Account Chunein (Select Account)",
                'menu_language': "Bhasha Badlein (Change Language)",
                'menu_help': "Niyam aur Controls (Help)",
                'menu_quit': "Khel Band Karein (Quit)",
                'menu_current_account': "Vartaman Account",
                'none': "Koi nahi",
                'selected': "Chun liya",
                'back': "Wapas",
                'quit_farewell': "Journey of Mankind se alvida. Namaste!",
                'lang_switched': "Bhasha Hindi par set kar di gayi hai.",
                'bag_title': "Basta / Inventory Bag",
                'bag_opened': "Bag khul gaya. Isme {count} cheezein hain. Haath mein: {holding}. Arrow keys se browse karein, Enter se pakrein, G se details sunein.",
                'bag_empty': "Bag khali hai. Zameen se samaan uthane ke liye Enter dabayein.",
                'bag_item_held': "{name} haath mein pakad liya! Hamla shakti {dmg} hai. Chalane ke liye Space dabayein.",
                'bag_held_tag': "[Haath mein pakda hua]",
                'weapon_swung_empty': "{weapon} chalaya! Shakti {dmg}. Aas paas koi janwar nahi mila.",
                'diary_title': "Yatra Diary (Safarnama)",
                'diary_current_era': "Vartaman Aitihasik Daur: {era}.",
                'diary_progress': "Pura kiya gaya: {done} / {total}.",
                'era_1_name': "Pracheen Pathar Kaal (Paleolithic)",
                'era_2_name': "Krishi Kranti Kaal (Neolithic)",
                'era_3_name': "Kansa Kaal (Bronze Age)",
                'north': "Uttar", 'south': "Dakshin", 'east': "Poorva", 'west': "Paschim"
            }
        }

    LANGUAGES = [
        ('en', "English"),
        ('ur', "Roman Urdu (Urdu Zaban)"),
        ('es', "Español (Spanish)"),
        ('fr', "Français (French)"),
        ('ar', "Al-Arabiyya (Arabic)"),
        ('hi', "Hindi (Hinglish)")
    ]

    def set_language(self, lang):
        if lang in self._strings:
            self.lang = lang
            return True
        return False

    def toggle_language(self):
        langs = [code for code, _ in self.LANGUAGES]
        if self.lang in langs:
            idx = langs.index(self.lang)
            self.lang = langs[(idx + 1) % len(langs)]
        else:
            self.lang = 'en'
        return self.lang

    def get_current_language_display(self):
        for code, name in self.LANGUAGES:
            if code == self.lang:
                return name
        return self.lang.upper()

    def tr(self, key, **kwargs):
        text = self._strings.get(self.lang, {}).get(key)
        if text is None:
            text = self._strings.get('en', {}).get(key, key)
        if kwargs:
            try:
                return text.format(**kwargs)
            except Exception:
                return text
        return text

loc = Localization(default_lang='en')
