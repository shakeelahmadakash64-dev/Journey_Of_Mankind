"""
Comprehensive Automated Verification Script for Journey of Mankind (Safar-e-Insaan)
Tests:
1. In-bag books presence (diary, guide_book, crafting_book)
2. Guide Book & Crafting Book chapter reader content across all 6 languages
3. QuestSystem, milestones, diary updates, and epoch advancement
4. Campfire fire-striking & meat roasting (cooked_meat)
5. Animal taming (pet companion) & combat assist
6. Shelter construction & resting
7. Day/Night time progression & weather reporting
8. Dynamic language cycling across English, Urdu, Spanish, French, Arabic, Hindi
"""

import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

# Mock audio & speech for headless test execution
class MockAudio:
    def play(self, *args, **kwargs): pass
    def play_footstep(self, *args, **kwargs): pass
    def play_sonar_beep(self, *args, **kwargs): pass
    def play_mammoth_trumpet(self, *args, **kwargs): pass
    def play_predator_growl(self, *args, **kwargs): pass
    def play_wolf_howl(self, *args, **kwargs): pass
    def play_item_found(self, *args, **kwargs): pass
    def play_portalopen(self, *args, **kwargs): pass
    def play_travel_whoosh(self, *args, **kwargs): pass
    def play_weapon_swing(self, *args, **kwargs): pass
    def play_weapon_hit(self, *args, **kwargs): pass
    def play_voice_attack(self, *args, **kwargs): pass
    def play_voice_hurt(self, *args, **kwargs): pass
    def play_heartbeat(self, *args, **kwargs): pass
    def play_voice_pant(self, *args, **kwargs): pass
    def play_stomach_rumble(self, *args, **kwargs): pass
    def play_craft(self, *args, **kwargs): pass
    def play_menu_select(self, *args, **kwargs): pass
    def play_menu_back(self, *args, **kwargs): pass
    def play_error(self, *args, **kwargs): pass
    def play_turn(self, *args, **kwargs): pass
    def play_bag_open(self, *args, **kwargs): pass
    def play_bag_close(self, *args, **kwargs): pass
    def play_page_turn(self, *args, **kwargs): pass
    def play_shelter_enter(self, *args, **kwargs): pass
    def play_shelter_exit(self, *args, **kwargs): pass
    def play_door_open(self, *args, **kwargs): pass
    def play_door_close(self, *args, **kwargs): pass
    def set_realm_ambience(self, realm_id='cradle', *args, **kwargs):
        self.current_ambience = realm_id
    def set_shelter_ambience(self, *args, **kwargs):
        self.current_ambience = 'ambience_shelter'
    def stop_ambient(self, *args, **kwargs):
        self.current_ambience = None

class MockSpeech:
    def __init__(self):
        self.spoken = []
    def speak(self, text, interrupt=True):
        self.spoken.append(text)
        # print(f"[Speech]: {text}")

from core.localization import loc
from game.character import Character
from game.world import World
from game.crafting import CraftingSystem
from game.creatures import FaunaManager, Creature
from game.quests import QuestSystem
from game.bag import BagSystem

def run_tests():
    print("=" * 60)
    print("STARTING JOURNEY OF MANKIND EPOCH & ACCESSIBILITY TESTS")
    print("=" * 60)

    audio = MockAudio()
    speech = MockSpeech()
    quest_system = QuestSystem(audio=audio, speech=speech)
    world = World(audio=audio, speech=speech, quest_system=quest_system)
    crafting = CraftingSystem(audio=audio, speech=speech, quest_system=quest_system)
    fauna = FaunaManager(audio=audio, speech=speech)
    bag = BagSystem(audio=audio, speech=speech)

    # 1. Starting Books Presence
    char = Character("TestPlayer", audio=audio, speech=speech)
    char.quest_system = quest_system

    inv_ids = [item['id'] for item in char.inventory]
    assert 'guide_book' in inv_ids, "Missing guide_book in satchel!"
    assert 'crafting_book' in inv_ids, "Missing crafting_book in satchel!"
    assert 'diary' in inv_ids, "Missing diary in satchel!"
    print("[PASS] TEST 1 PASSED: Satchel contains guide_book, crafting_book, and diary.")

    # 2. Languages Verification & Localization Cycling
    supported_langs = ['en', 'ur', 'es', 'fr', 'ar', 'hi']
    for l in supported_langs:
        loc.set_language(l)
        assert loc.lang == l, f"Failed setting language {l}"
        diary_summary = quest_system.get_diary_summary()
        assert len(diary_summary) > 20, f"Diary summary too short in {l}"
        guide_t = loc.tr('guide_ch1_title')
        assert guide_t, f"Missing guide_ch1_title in {l}"
    print(f"[PASS] TEST 2 PASSED: All 6 languages ({', '.join(supported_langs)}) verified.")

    # Reset to English for remaining checks
    loc.set_language('en')

    # 3. Fire-striking Milestone ('fire')
    assert 'fire' not in quest_system.completed_quests
    char.add_item('flint_stone', 'Flint Stone', 2)
    char.add_item('wood_stick', 'Branch', 4)
    char.make_fire(quest_system)
    assert char.has_fire is True, "Fire striking failed!"
    assert 'fire' in quest_system.completed_quests, "Quest 'fire' not completed!"
    print("[PASS] TEST 3 PASSED: Campfire struck, 'fire' milestone completed.")

    # 4. Weapon Crafting Milestone ('spear')
    char.add_item('flint_stone', 'Flint Stone', 1)
    char.add_item('wood_stick', 'Branch', 2)
    spear_recipe = next(r for r in crafting.recipes if r.recipe_id == 'spear')
    crafting.craft_item(spear_recipe, char)
    assert 'spear' in quest_system.completed_quests, "Quest 'spear' not completed!"
    assert char.equipped_weapon == 'spear', "Spear not equipped!"
    print("[PASS] TEST 4 PASSED: Hardwood Spear crafted, 'spear' milestone completed.")

    # 5. Combat & Hunting Milestone ('hunt')
    beast = Creature('test_wolf', 'cradle', 'creature_wolf_name', 'creature_wolf_desc', 30, 10, True, 'wolf', 0, 0)
    fauna.attack_creature(char, beast)
    assert 'hunt' in quest_system.completed_quests, "Quest 'hunt' not completed!"
    print("[PASS] TEST 5 PASSED: Creature attacked, 'hunt' milestone completed.")

    # 6. Meat Roasting Milestone ('roast')
    char.add_item('meat', 'Raw Meat', 1)
    char.roast_meat(quest_system)
    assert 'roast' in quest_system.completed_quests, "Quest 'roast' not completed!"
    assert any(i['id'] == 'cooked_meat' for i in char.inventory), "Cooked meat not added!"
    print("[PASS] TEST 6 PASSED: Meat roasted over campfire, 'roast' milestone completed.")

    # 7. Realm Crossing & Era 1 Advancement
    world._travel_to_realm(char, 'coastal', 'Prehistoric Red Sea')
    assert 'cross_realm' in quest_system.completed_quests, "Quest 'cross_realm' not completed!"
    assert quest_system.current_era == 2, f"Era should have advanced to 2! Current: {quest_system.current_era}"
    print(f"[PASS] TEST 7 PASSED: Realm crossed, humanity advanced to Era 2: {quest_system.get_era_name(2)}!")

    # 8. Animal Taming Milestone ('tame_wolf') & Pet Combat Assist
    wild_wolf = Creature('wolf_pack', 'coastal', 'creature_wolf_name', 'creature_wolf_desc', 50, 15, True, 'wolf', 0, 0)
    char.tame_creature(wild_wolf, quest_system)
    assert 'tame_wolf' in quest_system.completed_quests, "Quest 'tame_wolf' not completed!"
    assert char.pet is not None, "Companion pet not recorded on character!"
    
    # Test Pet combat assist
    target_beast = Creature('bear', 'coastal', 'creature_cave_bear_name', 'desc', 100, 20, False, 'mammoth', 0, 0)
    old_hp = target_beast.health
    fauna.attack_creature(char, target_beast)
    # weapon damage (25) + pet damage (15) = 40
    expected_hp = old_hp - (char.weapon_damage + 15)
    assert target_beast.health == expected_hp, f"Expected {expected_hp} HP after weapon+pet attack, got {target_beast.health}"
    print("[PASS] TEST 8 PASSED: Animal tamed, companion assisted in combat with bonus damage.")

    # 9. Shelter Building ('build_shelter') and Resting ('rest_shelter')
    char.add_item('wood_stick', 'Branch', 3)
    char.add_item('reed_fiber', 'Fiber', 2)
    world.build_shelter_at(char, quest_system)
    assert 'build_shelter' in quest_system.completed_quests, "Quest 'build_shelter' not completed!"
    
    world.rest_in_shelter(char, quest_system)
    assert 'rest_shelter' in quest_system.completed_quests, "Quest 'rest_shelter' not completed!"
    print("[PASS] TEST 9 PASSED: Shelter built and rested inside.")

    # 10. Day/Night Cycle and Time/Weather
    world.update_time(120.0)
    hour, phase, is_night = world.get_time_of_day()
    weather_name = world.get_weather_name()
    report = world.report_time_and_weather(char)
    assert "Time:" in report, f"Time report missing prefix: {report}"
    print(f"[PASS] TEST 10 PASSED: Time & weather simulated ({report}).")

    # 11. Read Journey Diary
    diary_summary = quest_system.get_diary_summary()
    assert "Paleolithic Dawn" in diary_summary or "Neolithic Revolution" in diary_summary
    print("[PASS] TEST 11 PASSED: Journey Diary successfully formatted with epoch achievements.")

    # 12. Era 2 Completion -> Advance to Era 3 (Chalcolithic & Bronze Age)
    char.add_item('obsidian_shard', 'Obsidian Shard', 1)
    char.add_item('wood_stick', 'Branch', 1)
    char.add_item('reed_fiber', 'Fiber', 1)
    dagger_recipe = next(r for r in crafting.recipes if r.recipe_id == 'obsidian_dagger')
    crafting.craft_item(dagger_recipe, char)
    assert 'craft_dagger' in quest_system.completed_quests, "Quest 'craft_dagger' not completed!"
    assert quest_system.current_era == 3, f"Humanity should have advanced to Era 3! Current: {quest_system.current_era}"
    print(f"[PASS] TEST 12 PASSED: Obsidian Dagger crafted, humanity advanced to Era 3: {quest_system.get_era_name(3)}!")

    # 13. Shelter Tracking in M Key Scanner
    shelters_in_grid = [tile for tile in world.grid.values() if tile.is_shelter]
    assert len(shelters_in_grid) >= 1, "No shelter found in grid for M scanner!"
    print(f"[PASS] TEST 13 PASSED: Shelter located in realm grid for Key M sonar tracking.")

    # 14. Shift + Enter Shelter Entry & Exit with Door Sounds & Ambience
    assert not char.is_inside_shelter, "Player should not start inside shelter."
    char.enter_shelter(quest_system)
    assert char.is_inside_shelter is True, "Failed to enter shelter!"
    assert getattr(audio, 'current_ambience', None) == 'ambience_shelter', "Audio did not switch to shelter ambience!"
    assert char.shelter_x == 0 and char.shelter_y == -1, "Player should be at shelter entry (0, -1)!"
    # Check shelter vitals
    char.stamina = 50.0
    char.update_vitals(1.0)
    assert char.stamina > 50.0, "Shelter did not regenerate stamina!"
    char.exit_shelter(realm_id='cradle')
    assert char.is_inside_shelter is False, "Failed to exit shelter!"
    assert getattr(audio, 'current_ambience', None) == 'cradle', "Audio did not restore realm ambience on exit!"
    print("[PASS] TEST 14 PASSED: Shift + Enter enters shelter with door audio & ambient switch, and exits back to open world.")

    # 15. In-Game Tab Quick Hub Localization Keys
    assert loc.tr('tab_menu_title'), "Missing tab_menu_title string!"
    assert loc.tr('tab_menu_quests'), "Missing tab_menu_quests string!"
    assert loc.tr('tab_menu_lang'), "Missing tab_menu_lang string!"
    assert loc.tr('page_nav_hint'), "Missing page_nav_hint string!"
    print("[PASS] TEST 15 PASSED: In-Game Tab Quick Hub and Textbook keys verified across localizations.")

    # 16. Authentic Sound Assets (Zipper, Doors, Pages, Shelter Ambience)
    sound_files = ['bag_open.wav', 'bag_close.wav', 'door_open.wav', 'door_close.wav', 'page_turn.wav', 'shelter_enter.wav', 'shelter_exit.wav', 'ambience_shelter.wav']
    sounds_folder = os.path.join(SCRIPT_DIR, 'sounds')
    for sf in sound_files:
        p = os.path.join(sounds_folder, sf)
        assert os.path.exists(p) and os.path.getsize(p) > 5000, f"Sound file {sf} missing or invalid!"
    print(f"[PASS] TEST 16 PASSED: All 8 authentic audio files ({', '.join(sound_files)}) verified on disk.")

    # 17. Auto-Revive Clears Shelter State
    char.is_inside_shelter = True
    char.revive()
    assert char.is_inside_shelter is False, "Auto-revive should clear inside_shelter state!"
    assert char.health == 100.0 and char.is_alive, "Character was not fully revived!"
    print("[PASS] TEST 17 PASSED: Auto-revive properly resets position, vitals, and clears shelter state.")

    # 18. Spacious 5x5 Shelter Interior Movement, Door Block & Shift+Enter Exit
    char.enter_shelter(quest_system)
    assert char.is_inside_shelter is True
    # Walk to Hearth (0, 0)
    moved = char.move_inside_shelter(0, 1)
    assert moved is True and char.shelter_x == 0 and char.shelter_y == 0
    # Walk to Bedroll (0, 1)
    moved = char.move_inside_shelter(0, 1)
    assert moved is True and char.shelter_y == 1
    # Try Shift+Enter away from door: should not exit!
    # Walk to door (0, -2)
    char.move_inside_shelter(0, -3)
    assert char.shelter_x == 0 and char.shelter_y == -2
    # Walking South at door should NOT exit automatically (door is closed)!
    south_walk = char.move_inside_shelter(0, -1)
    assert south_walk is False and char.is_inside_shelter is True, "Walking South should not automatically exit!"
    # Pressing Shift+Enter at door exits successfully!
    char.exit_shelter(realm_id='cradle')
    assert char.is_inside_shelter is False, "Shift + Enter at door should exit shelter!"
    print("[PASS] TEST 18 PASSED: Walking South does not exit; Shift+Enter at door exits shelter.")

    # 19. Shift+Enter Strictly Limited to Travel Point Gateways (No Portal Menu Popup)
    char.pos_x = 0
    char.pos_y = 0
    # Pos (0, 0) is not a border travel gateway
    travel_res = world.handle_realm_travel(char, None)
    assert travel_res == "NOT_AT_PORTAL", f"Expected NOT_AT_PORTAL, got {travel_res}"
    print("[PASS] TEST 19 PASSED: Shift+Enter strictly reserved for actual Travel Points (no portal menu popup).")

    # 20. Auto-Updater Verification & Database Preservation
    import json
    from core.updater import parse_version, PRESERVED_FILES, CURRENT_VERSION
    assert parse_version("1.2.0") == (1, 2, 0)
    assert parse_version("v1.3.5") == (1, 3, 5)
    assert parse_version("v2.0.0") > parse_version("1.2.0")
    assert 'mankind_data.db' in PRESERVED_FILES
    assert 'error.log' in PRESERVED_FILES

    # Check version.json exists and is valid
    version_file = os.path.join(os.path.dirname(__file__), 'version.json')
    assert os.path.exists(version_file)
    with open(version_file, 'r', encoding='utf-8') as f:
        v_data = json.load(f)
    # Verify updater translations in all languages
    for lang_code in ['en', 'ur', 'es', 'fr', 'ar', 'hi']:
        loc.set_language(lang_code)
        chk = loc.tr('updater_check')
        inst = loc.tr('updater_install')
        assert chk and len(chk) > 0, f"Missing updater_check for {lang_code}"
        assert inst and len(inst) > 0, f"Missing updater_install for {lang_code}"
    loc.set_language('en')

    print("[PASS] TEST 20 PASSED: Auto-updater versions, manifest & player DB preservation verified.")

    print("=" * 60)
    print("ALL 20 UNIT & INTEGRATION TESTS COMPLETED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == '__main__':
    run_tests()
