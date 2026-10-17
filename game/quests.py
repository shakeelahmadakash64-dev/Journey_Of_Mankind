"""
Journey of Mankind - Historical Epoch Evolution & Quest Journal System
Chronicles the entire progression of early humankind across historical eras:
- Era 1: The Paleolithic Dawn (Qadeem Stone Age - Fire, Flint, Spears & Migration)
- Era 2: The Neolithic Revolution (Agricultural Revolution, Animal Taming & Shelters)
- Era 3: The Chalcolithic & Bronze Age (Metallurgy, Smelting, Mining & Ancient Trade)

Manages the player's in-bag Journey Diary, milestone verification, and celebratory epoch advancements.
"""

import time
from core.localization import loc

class Quest:
    def __init__(self, quest_id, era, title_key, desc_key, reward_exp=100):
        self.quest_id = quest_id
        self.era = era
        self.title_key = title_key
        self.desc_key = desc_key
        self.reward_exp = reward_exp

    @property
    def title(self):
        return loc.tr(self.title_key)

    @property
    def desc(self):
        return loc.tr(self.desc_key)

class QuestSystem:
    def __init__(self, audio=None, speech=None):
        self.audio = audio
        self.speech = speech
        self.current_era = 1
        self.completed_quests = set()
        self.diary_history = []
        self._init_all_quests()

    def _init_all_quests(self):
        self.quests = {
            # Era 1: Paleolithic Dawn
            'fire': Quest('fire', 1, 'quest_fire_title', 'quest_fire_desc', 100),
            'spear': Quest('spear', 1, 'quest_spear_title', 'quest_spear_desc', 150),
            'hunt': Quest('hunt', 1, 'quest_hunt_title', 'quest_hunt_desc', 200),
            'roast': Quest('roast', 1, 'quest_roast_title', 'quest_roast_desc', 120),
            'cross_realm': Quest('cross_realm', 1, 'quest_cross_realm_title', 'quest_cross_realm_desc', 250),

            # Era 2: Neolithic Revolution
            'tame_wolf': Quest('tame_wolf', 2, 'quest_tame_wolf_title', 'quest_tame_wolf_desc', 300),
            'build_shelter': Quest('build_shelter', 2, 'quest_build_shelter_title', 'quest_build_shelter_desc', 250),
            'craft_dagger': Quest('craft_dagger', 2, 'quest_craft_dagger_title', 'quest_craft_dagger_desc', 200),
            'rest_shelter': Quest('rest_shelter', 2, 'quest_rest_shelter_title', 'quest_rest_shelter_desc', 150),

            # Era 3: Bronze Age
            'mine_minerals': Quest('mine_minerals', 3, 'quest_mine_minerals_title', 'quest_mine_minerals_desc', 350),
            'craft_club': Quest('craft_club', 3, 'quest_craft_club_title', 'quest_craft_club_desc', 300),
            'trade_elder': Quest('trade_elder', 3, 'quest_trade_elder_title', 'quest_trade_elder_desc', 400),
        }

    def check_milestone(self, character, quest_id):
        """Validates if an active quest has been completed and updates diary/era."""
        if quest_id not in self.quests:
            return False

        if quest_id in self.completed_quests:
            return False

        quest = self.quests[quest_id]
        if quest.era != self.current_era:
            # Player can achieve future era quests or current era
            pass

        self.completed_quests.add(quest_id)
        
        # Add to personal Journey Diary history
        timestamp_str = time.strftime("%H:%M")
        era_name = self.get_era_name(quest.era)
        entry = f"[{era_name}] {quest.title}: {quest.desc}"
        self.diary_history.append(entry)

        if self.audio:
            self.audio.play_item_found()

        complete_msg = loc.tr('quest_completed_announce', title=quest.title)
        if self.speech:
            self.speech.speak(complete_msg)

        # Check if all quests of current era are completed
        self._check_era_advancement(character)
        return True

    def _check_era_advancement(self, character):
        """Checks if current era's required quests are fulfilled to advance humanity."""
        current_era_quests = [q for q in self.quests.values() if q.era == self.current_era]
        if all(q.quest_id in self.completed_quests for q in current_era_quests):
            self.advance_era(character)

    def advance_era(self, character):
        """Advances humanity into the next grand historical epoch!"""
        self.current_era += 1
        new_era_name = self.get_era_name(self.current_era)
        new_era_desc = self.get_era_desc(self.current_era)

        if self.audio:
            self.audio.play_portalopen()
            self.audio.play_travel_whoosh()

        adv_entry = f"*** {loc.tr('epoch_advanced_title', era=new_era_name)} *** - {new_era_desc}"
        self.diary_history.append(adv_entry)

        # Full restore and vital boost reward for epoch breakthrough
        character.health = 100.0
        character.hunger = 100.0
        character.thirst = 100.0
        character.stamina = 100.0

        speech_msg = loc.tr('epoch_advanced_announce', era=new_era_name, desc=new_era_desc)
        if self.speech:
            self.speech.speak(speech_msg)

    def get_era_name(self, era=None):
        e = era if era is not None else self.current_era
        if e == 1:
            return loc.tr('era_1_name')
        elif e == 2:
            return loc.tr('era_2_name')
        elif e == 3:
            return loc.tr('era_3_name')
        return f"Era {e}"

    def get_era_desc(self, era=None):
        e = era if era is not None else self.current_era
        if e == 1:
            return loc.tr('era_1_desc')
        elif e == 2:
            return loc.tr('era_2_desc')
        elif e == 3:
            return loc.tr('era_3_desc')
        return ""

    def get_diary_summary(self):
        """Constructs a comprehensive spoken summary of the player's Journey Diary."""
        era_name = self.get_era_name()
        current_quests = [q for q in self.quests.values() if q.era == self.current_era]
        completed_in_era = [q for q in current_quests if q.quest_id in self.completed_quests]
        pending_in_era = [q for q in current_quests if q.quest_id not in self.completed_quests]

        lines = [
            f"{loc.tr('diary_title')}.",
            f"{loc.tr('diary_current_era', era=era_name)}",
            f"{loc.tr('diary_progress', done=len(completed_in_era), total=len(current_quests))}"
        ]

        if pending_in_era:
            lines.append(f"{loc.tr('diary_active_goals')}:")
            for q in pending_in_era:
                lines.append(f"- {q.title}: {q.desc}")
        else:
            lines.append(loc.tr('diary_era_ready_advance'))

        if self.diary_history:
            lines.append(f"{loc.tr('diary_recent_history')}:")
            for h in self.diary_history[-4:]:
                lines.append(f"- {h}")

        return "\n".join(lines)
