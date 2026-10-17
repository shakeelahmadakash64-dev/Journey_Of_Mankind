"""
Journey of Mankind - Prehistoric Clan Partner & Relationship System
Simulates human social connection, emotional companionship, shelter sharing,
cooperative survival, shared meals, gifting, and family generation legacy.
Fully accessible with screen reader dialogue in English and Roman Urdu.
"""

import time
import random
from core.localization import loc
from game.menu import AccessibleMenu

class PartnerSystem:
    def __init__(self, audio=None, speech=None):
        self.audio = audio
        self.speech = speech
        self.is_rescued = False
        self.name = "Ayla"
        self.gender = "female"
        self.affection = 50.0  # 0 to 100
        self.status = "at_shelter"  # 'at_shelter', 'with_player', 'tending_fire'
        self.has_child = False
        self.last_interaction_time = time.time()
        self.last_gift_time = 0.0

    def get_dict(self):
        return {
            'is_rescued': self.is_rescued,
            'name': self.name,
            'gender': self.gender,
            'affection': self.affection,
            'status': self.status,
            'has_child': self.has_child
        }

    def load_dict(self, data):
        if not data:
            return
        self.is_rescued = bool(data.get('is_rescued', False))
        self.name = str(data.get('name', 'Ayla'))
        self.gender = str(data.get('gender', 'female'))
        self.affection = float(data.get('affection', 50.0))
        self.status = str(data.get('status', 'at_shelter'))
        self.has_child = bool(data.get('has_child', False))

    def rescue_partner(self, character, quest_system=None):
        """Called when player rescues or unites with their clan companion."""
        self.is_rescued = True
        self.affection = 65.0
        self.status = "at_shelter"
        character.social = 100.0
        character.morale = min(100.0, character.morale + 30.0)

        msg = (
            f"You have united with {self.name}, a fellow survivor of the primordial earth! "
            f"You are no longer alone against the wild. Together, you will build a home, survive the elements, "
            f"and carry the torch of humanity forward!" if loc.lang == 'en' else
            f"Aap {self.name} se mil chuke hain! Ab aap is khaufnak qadeem dunya mein tanha nahi hain. "
            f"Aap dono mil kar panahgah banayein gay, shikar karein gay, aur insaniyat ke chiragh ko aagay barhayein gay!"
        )
        if self.audio:
            self.audio.play("item_found")
            self.audio.play("menu_select")
        if self.speech:
            self.speech.speak(msg)

        if quest_system and hasattr(quest_system, 'check_milestone'):
            quest_system.check_milestone(character, 'partner_united')

    def open_partner_menu(self, character, screen=None):
        """Interactive Accessible Dialogue Hub with Life Partner."""
        if not self.is_rescued:
            has_food_or_shelter = character.is_inside_shelter or any(i.get('id') in ('cooked_meat', 'meat', 'wild_berries') for i in character.inventory)
            if has_food_or_shelter:
                self.rescue_partner(character, getattr(character, 'quest_system', None))
                return
            else:
                msg = (
                    "You have not yet found a clan companion in the wilderness. "
                    "Build a shelter (Key B) or forage berries and meat to welcome a fellow survivor!" if loc.lang == 'en' else
                    "Aap ko abhi tak koi hamsafar nahi mila. "
                    "Panahgah banayein (Key B) ya bag mein khana rakhein ta kay kisi doosray bhatkay huay insan ko sahara day sakein!"
                )
                if self.speech:
                    self.speech.speak(msg)
                return

        def action_talk():
            self._do_talk(character)
            return "TALKED"

        def action_gift():
            self._open_gift_menu(character, screen)
            return "GIFTED"

        def action_share_meal():
            self._do_share_meal(character)
            return "MEAL"

        def action_toggle_role():
            if self.status == 'at_shelter':
                self.status = 'with_player'
                msg = (
                    f"{self.name} will now accompany you on your hunting and exploration journey!" if loc.lang == 'en' else
                    f"{self.name} ab aap ke sath shikar aur safar par chalay gi!"
                )
            else:
                self.status = 'at_shelter'
                msg = (
                    f"{self.name} will remain at the shelter, keeping the hearth fire burning and guarding the food!" if loc.lang == 'en' else
                    f"{self.name} ab panahgah mein choolhay ki aag roshan rakhay gi aur rashan ki hifazat karay gi!"
                )
            if self.speech:
                self.speech.speak(msg)
            if self.audio:
                self.audio.play("menu_select")
            return "ROLE"

        def action_family():
            self._do_family_event(character)
            return "FAMILY"

        status_desc = "With You" if self.status == 'with_player' else "At Shelter"
        options = [
            (f"{loc.tr('partner_talk')} ({self.name})", action_talk),
            (loc.tr('partner_gift'), action_gift),
            (loc.tr('partner_meal'), action_share_meal),
            (f"{loc.tr('partner_role')}: [{status_desc}]", action_toggle_role),
        ]

        if character.current_era >= 3 and self.affection >= 85.0 and not self.has_child:
            options.append((loc.tr('partner_family'), action_family))

        options.append((loc.tr('back'), lambda: "BACK"))

        title = f"{self.name} ({loc.tr('partner_title')}) - Affection: {int(self.affection)}%"
        menu = AccessibleMenu(title, options, self.audio, self.speech)
        menu.run(screen)

    def _do_talk(self, character):
        """Meaningful human conversation between survivors."""
        character.social = min(100.0, character.social + 20.0)
        character.morale = min(100.0, character.morale + 15.0)
        self.affection = min(100.0, self.affection + 3.0)

        dialogues_en = [
            f"{self.name} smiles warmly: 'The hearth is bright today. When we sit together, the prehistoric dark doesn't feel so frightening.'",
            f"{self.name} looks at the stars: 'Do you ever wonder what is out there beyond the night sky? One day, our descendants will reach those lights.'",
            f"{self.name} holds your hand: 'I watched you brave the sabertooth cat. Your courage keeps our fire alive.'",
            f"{self.name} checks your supplies: 'Stay safe out in the wilds. I will always wait for you at the shelter door.'",
            f"{self.name} shares a story: 'My elders spoke of a great river to the East. With you by my side, I know we will reach it.'"
        ]
        dialogues_ur = [
            f"{self.name} muskuratay huay kehti hai: 'Aaj choolhay ki aag bohot pur-sukoon hai. Jab hum sath hotay hain to jungle ki tareeki ka khauf nahi rehta.'",
            f"{self.name} sitaron ki taraf dekh kar kehti hai: 'Kya aap ne socha hai asman ke uss paar kya hai? Ek din hamari naslein un sitaron tak pohanchein gi.'",
            f"{self.name} aap ka haath thaam kar kehti hai: 'Aap ki himmat aur shikar ki wajah se hamari panahgah aabaad hai.'",
            f"{self.name} kehti hai: 'Bahar shikar par ehtiyat karein. Main darwazay par aap ki wapsi ka intizar karoon gi.'",
            f"{self.name} kehti hai: 'Hum dono mil kar is zameen par insaniyat ki azeem tareekh likhein gay.'"
        ]

        txt = random.choice(dialogues_en if loc.lang == 'en' else dialogues_ur)
        if self.audio:
            self.audio.play("menu_select")
        if self.speech:
            self.speech.speak(txt)

    def _open_gift_menu(self, character, screen=None):
        """Allows giving precious resources or crafted gifts to partner."""
        giftable_items = [
            ('cooked_meat', 15.0, "Delicious savory roasted meat"),
            ('wild_berries', 8.0, "Sweet wild berries"),
            ('meat', 10.0, "Fresh hunted game meat"),
            ('obsidian_shard', 18.0, "Gleaming volcanic obsidian jewelry"),
            ('bone_club', 12.0, "Sturdy carved bone trinket"),
            ('wood_stick', 6.0, "Fragrant dry cedar firewood")
        ]

        options = []
        for item_id, aff_bonus, label in giftable_items:
            count = sum(i.get('quantity', 0) for i in character.inventory if i.get('id') == item_id)
            if count > 0:
                def make_give_fn(i_id=item_id, bonus=aff_bonus):
                    def give():
                        character.remove_item(i_id, 1)
                        self.affection = min(100.0, self.affection + bonus)
                        character.social = 100.0
                        character.morale = min(100.0, character.morale + 20.0)
                        msg = (
                            f"You gave {self.name} a gift! Her trust and affection grew to {int(self.affection)}%." if loc.lang == 'en' else
                            f"Aap ne {self.name} ko tohfa diya! Us ka aitaymad aur pyar barh kar {int(self.affection)}% ho gaya."
                        )
                        if self.audio:
                            self.audio.play("item_found")
                        if self.speech:
                            self.speech.speak(msg)
                        return "GIFT_GIVEN"
                    return give
                options.append((f"{label} (Count: {count})", make_give_fn()))

        if not options:
            msg = "You have no giftable items (roasted meat, berries, obsidian, or carved bone) in your satchel." if loc.lang == 'en' else "Aap ke bag mein tohfay ke liy koi cheez (bhoona gosht, berries, obsidian) mojood nahi."
            if self.speech:
                self.speech.speak(msg)
            return

        options.append((loc.tr('back'), lambda: "BACK"))
        menu = AccessibleMenu(loc.tr('partner_gift_title'), options, self.audio, self.speech)
        menu.run(screen)

    def _do_share_meal(self, character):
        """Shares a warm hearth meal together, restoring vital stats for both survivors."""
        food_ids = ('cooked_meat', 'wild_berries', 'meat')
        chosen_food = next((f_id for f_id in food_ids if any(i.get('id') == f_id and i.get('quantity', 0) > 0 for i in character.inventory)), None)
        if not chosen_food:
            msg = "You need roasted meat, fresh meat, or berries in your satchel to share a meal together." if loc.lang == 'en' else "Khana share karne ke liay bag mein bhoona gosht, kacha gosht ya berries honi chahiyen."
            if self.speech:
                self.speech.speak(msg)
            return

        character.remove_item(chosen_food, 1)

        character.hunger = min(100.0, character.hunger + 45.0)
        character.social = 100.0
        character.morale = 100.0
        character.fatigue = max(0.0, character.fatigue - 25.0)
        self.affection = min(100.0, self.affection + 6.0)

        msg = (
            f"You and {self.name} sat by the warm crackling fire, sharing a delicious meal. "
            f"Both hunger and exhaustion melt away, leaving you feeling invigorated and comforted!" if loc.lang == 'en' else
            f"Aap aur {self.name} ne choolhay ke paas baith kar mazedaar khana share kiya. "
            f"Bhook aur thakawat khatam ho gayi, aur dil ko azeem sukoon mila!"
        )
        if self.audio:
            self.audio.play("eat")
            self.audio.play("menu_select")
        if self.speech:
            self.speech.speak(msg)

    def _do_family_event(self, character):
        """Birth of the next human generation, advancing human civilization."""
        self.has_child = True
        self.affection = 100.0
        character.social = 100.0
        character.morale = 100.0

        msg = (
            f"A joyous historic dawn for humankind! {self.name} holds your newborn child in her arms by the warm hearth. "
            f"The sound of the baby cooing echoes inside your shelter. Humanity's legacy will continue through the ages!" if loc.lang == 'en' else
            f"Insaniyat ki tareekh ka sab se khoobsurat lamha! {self.name} ne naye bache ko choolhay ke paas godh mein utha liya hai. "
            f"Bachay ki meethi awaz panahgah mein goonj rahi hai. Ab aap ki nasl qayamat tak insaniyat ka ilm aur aag aagay barhaye gi!"
        )
        if self.audio:
            self.audio.play_baby_coo()
            self.audio.play("item_found")
        if self.speech:
            self.speech.speak(msg)
