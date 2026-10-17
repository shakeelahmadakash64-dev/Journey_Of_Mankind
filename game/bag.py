"""
Journey of Mankind - Interactive Accessible Satchel & In-Bag Books System
Contains player inventory, as well as:
- 📘 Survival Guide Book (item_guide_book): Spoken chapter reader on navigation, combat, radar, vitals, day/night.
- 📜 Crafting Recipe Book (item_crafting_book): Spoken blueprint reader on tools, weapons, fire, shelters.
- 📖 Journey Diary (item_diary): Spoken record of active era goals, completed milestones, and epoch progression.
- G key: Explains detailed purpose and utility of any selected item ('wo kiss kaam aata hai').
- Enter key: Opens books/diary, eats food, roasts meat on campfire, or holds item in hand.
- I or Escape: Closes the bag.
Ensures zero main-game commands leak or apply while browsing the bag.
"""

import pygame
from core.localization import loc

class BagSystem:
    def __init__(self, audio=None, speech=None):
        self.audio = audio
        self.speech = speech
        self.font = None
        self.small_font = None

    def _init_fonts(self):
        if not self.font:
            if hasattr(pygame.font, 'SysPlusFont'):
                self.font = pygame.font.SysPlusFont("Arial", 26)
            else:
                self.font = pygame.font.SysFont("Arial", 26)
            self.small_font = pygame.font.SysFont("Arial", 18)

    def open_bag(self, character, screen=None):
        """Opens dedicated inventory satchel. Exclusively intercepts all input until closed."""
        self._init_fonts()

        if self.audio:
            self.audio.play_bag_open()

        inv_count = len(character.inventory)
        holding_name = getattr(character, 'equipped_weapon_name', 'Bare Hands')
        
        bag_msg = loc.tr('bag_opened', count=inv_count, holding=holding_name)
        if self.speech:
            self.speech.speak(bag_msg)

        selected_index = 0
        clock = pygame.time.Clock()

        while True:
            clock.tick(30)
            items = character.inventory

            # Keep index in bounds
            if items:
                selected_index = max(0, min(selected_index, len(items) - 1))
            else:
                selected_index = 0

            # Render Visual Screen
            if screen is not None:
                self._render_screen(screen, character, items, selected_index)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._close_bag()
                    return "QUIT"

                elif event.type == pygame.KEYDOWN:
                    # 1. Close Bag (I or Escape)
                    if event.key in (pygame.K_i, pygame.K_ESCAPE):
                        self._close_bag()
                        return "CLOSED"

                    # 2. Browse Previous Item (Up Arrow)
                    elif event.key == pygame.K_UP:
                        if not items:
                            continue
                        selected_index = (selected_index - 1) % len(items)
                        if self.audio:
                            self.audio.play_menu_move()
                        self._speak_item(character, items[selected_index])

                    # 3. Browse Next Item (Down Arrow)
                    elif event.key == pygame.K_DOWN:
                        if not items:
                            continue
                        selected_index = (selected_index + 1) % len(items)
                        if self.audio:
                            self.audio.play_menu_move()
                        self._speak_item(character, items[selected_index])

                    # 4. Item Purpose & Utility Details (G Key)
                    elif event.key == pygame.K_g:
                        if not items:
                            empty_str = loc.tr('bag_empty')
                            if self.speech:
                                self.speech.speak(empty_str)
                            continue
                        cur_item = items[selected_index]
                        self._speak_item_details(cur_item)

                    # 5. Enter Action: Open Books / Eat / Roast / Hold in Hand
                    elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        if not items:
                            empty_str = loc.tr('bag_empty')
                            if self.speech:
                                self.speech.speak(empty_str)
                            continue

                        cur_item = items[selected_index]
                        i_id = cur_item['id']

                        # 📘 Survival Guide Book Reader
                        if i_id == 'guide_book':
                            self.open_book_reader(screen, 'guide')

                        # 📜 Crafting Recipe Book Reader
                        elif i_id == 'crafting_book':
                            self.open_book_reader(screen, 'crafting')

                        # 📖 Personal Journey Diary
                        elif i_id == 'diary':
                            self.read_diary(character)

                        # Campfire Meat Roasting
                        elif i_id == 'meat' and character.has_fire:
                            character.roast_meat(getattr(character, 'quest_system', None))

                        # Direct Food Consumption
                        elif i_id in ('wild_berries', 'cooked_meat'):
                            character.eat_item(i_id)

                        # Hold Weapon or Resource in Hand
                        else:
                            self._hold_item_in_hand(character, cur_item)

    def read_diary(self, character):
        """Reads the player's personal Journey Diary and epoch progress."""
        if hasattr(character, 'quest_system') and character.quest_system:
            diary_text = character.quest_system.get_diary_summary()
        else:
            diary_text = f"{loc.tr('diary_title')}. {loc.tr('diary_current_era', era=loc.tr('era_1_name'))}"

        if self.audio:
            self.audio.play("menu_select")
        if self.speech:
            self.speech.speak(diary_text)

    def open_book_reader(self, screen, book_type='guide'):
        """Interactive in-bag spoken textbook page reader with Tab / Shift+Tab navigation and page-turn audio."""
        self._init_fonts()
        if self.audio:
            self.audio.play_page_turn()

        if book_type == 'guide':
            book_title = loc.tr('guide_book_title')
            pages = [
                (loc.tr('guide_ch1_title'), loc.tr('guide_ch1_body')),
                (loc.tr('guide_ch2_title'), loc.tr('guide_ch2_body')),
                (loc.tr('guide_ch3_title'), loc.tr('guide_ch3_body')),
                (loc.tr('guide_ch4_title'), loc.tr('guide_ch4_body')),
                (loc.tr('guide_ch5_title'), loc.tr('guide_ch5_body')),
                (loc.tr('guide_ch6_title'), loc.tr('guide_ch6_body'))
            ]
        else:
            book_title = loc.tr('craft_book_title')
            pages = [
                (loc.tr('craft_ch1_title'), loc.tr('craft_ch1_body')),
                (loc.tr('craft_ch2_title'), loc.tr('craft_ch2_body')),
                (loc.tr('craft_ch3_title'), loc.tr('craft_ch3_body')),
                (loc.tr('craft_ch4_title'), loc.tr('craft_ch4_body')),
                (loc.tr('craft_ch5_title'), loc.tr('craft_ch5_body')),
                (loc.tr('craft_ch6_title'), loc.tr('craft_ch6_body')),
                (loc.tr('craft_ch7_title'), loc.tr('craft_ch7_body'))
            ]

        total_pages = len(pages)
        page_index = 0

        def announce_page(idx, with_hint=False):
            t, b = pages[idx]
            p_num = idx + 1
            header = loc.tr('page_read_title', cur=p_num, total=total_pages, title=t)
            full_speech = f"{header}. {b}"
            if with_hint:
                full_speech += f" {loc.tr('page_nav_hint')}"
            if self.speech:
                self.speech.speak(full_speech)

        announce_page(0, with_hint=True)

        def wrap_lines(text, max_chars=60):
            words = text.split()
            lines = []
            curr = []
            c_len = 0
            for w in words:
                if c_len + len(w) + 1 > max_chars:
                    lines.append(" ".join(curr))
                    curr = [w]
                    c_len = len(w)
                else:
                    curr.append(w)
                    c_len += len(w) + 1
            if curr:
                lines.append(" ".join(curr))
            return lines

        clock = pygame.time.Clock()
        while True:
            clock.tick(30)

            # High-contrast visual textbook rendering
            if screen is not None:
                screen.fill((16, 20, 32))
                # Outer textbook parchment border
                pygame.draw.rect(screen, (40, 55, 80), pygame.Rect(20, 15, 720, 510), border_radius=6)
                pygame.draw.rect(screen, (22, 30, 48), pygame.Rect(25, 20, 710, 500), border_radius=6)

                # Header: Book title & page badge
                t_surf = self.font.render(f"[ {book_title.upper()} ]", True, (255, 215, 0))
                screen.blit(t_surf, (40, 30))
                
                cur_title, cur_body = pages[page_index]
                badge_text = loc.tr('page_read_title', cur=page_index + 1, total=total_pages, title=cur_title)
                badge_surf = self.small_font.render(badge_text, True, (130, 220, 255))
                screen.blit(badge_surf, (40, 70))
                pygame.draw.line(screen, (70, 95, 140), (40, 100), (720, 100), 2)

                # Wrapped body text lines
                y = 120
                body_lines = wrap_lines(cur_body, max_chars=62)
                for line in body_lines:
                    line_surf = self.small_font.render(line, True, (235, 235, 235))
                    screen.blit(line_surf, (45, y))
                    y += 28

                # Footer controls
                pygame.draw.line(screen, (70, 95, 140), (40, 475), (720, 475), 2)
                foot_text = "[Tab]=Next Page | [Shift+Tab]=Prev Page | [Space/Enter]=Re-read | [Escape]=Back to Satchel"
                foot_surf = self.small_font.render(foot_text, True, (180, 225, 180))
                screen.blit(foot_surf, (40, 488))
                pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

                elif event.type == pygame.KEYDOWN:
                    mods = pygame.key.get_mods()
                    is_shift = bool(mods & pygame.KMOD_SHIFT)

                    # 1. Close book back to bag
                    if event.key in (pygame.K_ESCAPE, pygame.K_BACKSPACE, pygame.K_i):
                        if self.audio:
                            self.audio.play_bag_open()
                        if self.speech:
                            self.speech.speak("Returned to Bag." if loc.lang == 'en' else "Bag par wapsi.")
                        return

                    # 2. Tab Navigation (Tab = Next Page, Shift + Tab = Prev Page)
                    elif event.key == pygame.K_TAB:
                        if is_shift:
                            page_index = (page_index - 1) % total_pages
                        else:
                            page_index = (page_index + 1) % total_pages
                        if self.audio:
                            self.audio.play_page_turn()
                        announce_page(page_index)

                    # 3. Arrow / Page key navigation
                    elif event.key in (pygame.K_RIGHT, pygame.K_DOWN, pygame.K_PAGEDOWN):
                        page_index = (page_index + 1) % total_pages
                        if self.audio:
                            self.audio.play_page_turn()
                        announce_page(page_index)

                    elif event.key in (pygame.K_LEFT, pygame.K_UP, pygame.K_PAGEUP):
                        page_index = (page_index - 1) % total_pages
                        if self.audio:
                            self.audio.play_page_turn()
                        announce_page(page_index)

                    # 4. Space / Enter to repeat current page
                    elif event.key in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_KP_ENTER):
                        if self.audio:
                            self.audio.play("menu_select")
                        announce_page(page_index)

    def _speak_item(self, character, item):
        """Announces the focused item name, quantity, and whether it is already held in hand."""
        name = item['name']
        qty = item['quantity']
        is_held = (character.equipped_weapon == item['id'])
        held_str = f", {loc.tr('bag_held_tag')}" if is_held else ""
        msg = f"{name}, Quantity: {qty}{held_str}" if loc.lang == 'en' else f"{name}, Tadad: {qty}{held_str}"
        if self.speech:
            self.speech.speak(msg)

    def _speak_item_details(self, item):
        """Speaks the exact prehistoric utility and purpose of the focused item (Key G)."""
        item_id = item['id']
        key = f"item_details_{item_id}"
        details = loc.tr(key)
        if details == key:
            details = f"{item['name']}: Prehistoric resource or item stored in your bag." if loc.lang == 'en' else f"{item['name']}: Qadeem daur ka zaroori samaan."

        if self.audio:
            self.audio.play("menu_select")
        if self.speech:
            self.speech.speak(details)

    def _hold_item_in_hand(self, character, item):
        """Equips and holds the selected item directly in the player's hands."""
        item_id = item['id']
        item_name = item['name']
        dmg = character.hold_item(item_id, item_name)
        
        if self.audio:
            self.audio.play_weapon_swing()

        msg = loc.tr('bag_item_held', name=item_name, dmg=dmg)
        if self.speech:
            self.speech.speak(msg)

    def _render_screen(self, screen, character, items, selected_index):
        """High-contrast visual screen render for the inventory satchel."""
        screen.fill((12, 18, 30))
        
        # Title
        title_surf = self.font.render(loc.tr('bag_title'), True, (255, 215, 0))
        screen.blit(title_surf, (30, 20))

        # Current Hand Status
        pet_str = f" | Companion: {character.pet['name']}" if getattr(character, 'pet', None) else ""
        hand_surf = self.small_font.render(
            f"Hand Status: Holding {character.equipped_weapon_name} (Damage: {character.weapon_damage}){pet_str}",
            True,
            (100, 220, 255)
        )
        screen.blit(hand_surf, (30, 56))

        # Divider
        pygame.draw.line(screen, (60, 80, 110), (30, 80), (730, 80), 2)

        # Inventory Items List
        y = 95
        if not items:
            empty_surf = self.font.render(loc.tr('bag_empty'), True, (200, 200, 200))
            screen.blit(empty_surf, (30, y))
        else:
            for idx, item in enumerate(items):
                is_selected = (idx == selected_index)
                is_held = (character.equipped_weapon == item['id'])
                held_str = f" {loc.tr('bag_held_tag')}" if is_held else ""
                cursor = ">> " if is_selected else "   "
                line_text = f"{cursor}{item['name']} (x{item['quantity']}){held_str}"
                
                if is_selected:
                    color = (255, 235, 100)
                    bg_rect = pygame.Rect(25, y - 2, 700, 24)
                    pygame.draw.rect(screen, (35, 50, 80), bg_rect)
                else:
                    color = (215, 215, 215)
                
                item_surf = self.small_font.render(line_text, True, color)
                screen.blit(item_surf, (30, y))
                y += 28

        # Footer controls
        pygame.draw.line(screen, (60, 80, 110), (30, 480), (730, 480), 2)
        footer_text = "[Up/Down]=Browse | [Enter]=Open Book / Hold | [G]=Details & Purpose | [I/Escape]=Close"
        footer_surf = self.small_font.render(footer_text, True, (180, 220, 180))
        screen.blit(footer_surf, (30, 495))

        pygame.display.flip()

    def _close_bag(self):
        if self.audio:
            self.audio.play_bag_close()
        msg = "Bag closed." if loc.lang == 'en' else "Bag band ho gaya."
        if self.speech:
            self.speech.speak(msg)
