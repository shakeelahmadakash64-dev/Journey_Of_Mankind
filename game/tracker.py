"""
Journey of Mankind - 3D Audio Sonar Item Radar & Tracking System
Allows blind players to press 'M' to track and navigate to ground resources via 3D stereo pings.
Provides continuous audio guidance until the player reaches and collects the item with Spacebar.
"""

import math
from core.localization import loc

class ItemTracker:
    def __init__(self, audio=None, speech=None):
        self.audio = audio
        self.speech = speech
        self.active_target = None  # (x, y, item_display_name, item_id)
        self.last_ping_time = 0

    def track_nearest_item(self, world, character):
        """Scans the active map for ground resources and sets directional audio tracking."""
        cur_tile = world.get_tile(character.pos_x, character.pos_y)
        
        # 1. Check if already standing on resources
        if cur_tile and (cur_tile.resources or cur_tile.can_drink):
            if self.audio:
                self.audio.play_item_found()
            if cur_tile.resources:
                items_str = ", ".join([f"{qty} {loc.tr(name_key)}" for _, name_key, qty in cur_tile.resources])
                msg = f"You are standing right on: {items_str}! Press Spacebar to pick them up." if loc.lang == 'en' else f"Aap bilkul {items_str} ke upar kharay hain! Uthanay ke liay Spacebar dabayein."
            else:
                msg = "You are standing right at a freshwater drinking source! Press Spacebar to drink." if loc.lang == 'en' else "Aap saaf paani ke chashmay par kharay hain! Peenay ke liay Spacebar dabayein."
            if self.speech:
                self.speech.speak(msg)
            self.active_target = None
            return

        # 2. Search entire map for closest resource
        closest_dist = float('inf')
        closest_coord = None
        closest_item_name = None
        closest_item_id = None

        for (tx, ty), tile in world.grid.items():
            if tile.resources:
                dist = abs(tx - character.pos_x) + abs(ty - character.pos_y)
                if dist < closest_dist:
                    closest_dist = dist
                    closest_coord = (tx, ty)
                    closest_item_name = loc.tr(tile.resources[0][1])
                    closest_item_id = tile.resources[0][0]
            elif tile.can_drink:
                dist = abs(tx - character.pos_x) + abs(ty - character.pos_y)
                if dist < closest_dist:
                    closest_dist = dist
                    closest_coord = (tx, ty)
                    closest_item_name = "Freshwater" if loc.lang == 'en' else "Saaf Paani"
                    closest_item_id = "water"

        if not closest_coord:
            msg = "No ground items or resources detected in this entire area." if loc.lang == 'en' else "Is ilaqay mein zameen par mazeed koi samaan nahi mila."
            if self.speech:
                self.speech.speak(msg)
            if self.audio:
                self.audio.play_error()
            self.active_target = None
            return

        # 3. Calculate direction and stereo pan
        tx, ty = closest_coord
        dx = tx - character.pos_x
        dy = ty - character.pos_y
        
        dir_name = self._get_direction_name(dx, dy)
        pan = self._calc_pan(dx, dy, character.facing)

        if self.audio:
            self.audio.play_sonar_beep(pan=pan)

        self.active_target = (tx, ty, closest_item_name, closest_item_id, 'item', None)

        msg = f"Tracking {closest_item_name}: {closest_dist} steps to the {dir_name}. Follow the audio pings to reach it!" if loc.lang == 'en' else f"{closest_item_name} track ho gaya: {dir_name} ki taraf {closest_dist} qadam. Aawaz ki pings sun kar agay barhein!"
        if self.speech:
            self.speech.speak(msg)

    def set_target(self, tx, ty, name, target_type='travel_point', realm_dest=None):
        """Sets an explicit navigation target, such as a map Travel Point gateway."""
        self.active_target = (tx, ty, name, name, target_type, realm_dest)
        if self.audio:
            self.audio.play_item_found()

    def set_creature_target(self, creature, dist=0, dir_name=""):
        """Locks tracking onto a live prehistoric creature."""
        self.active_target = (creature.x, creature.y, creature.name, creature.creature_id, 'creature', creature)
        if self.audio:
            self.audio.play_item_found()

    def report_target_status(self, world, character):
        """Called on key 'O': Speaks distance and compass direction to active tracked target."""
        if not self.active_target:
            msg = "No active tracking target. Press A to track beasts, K for Travel Points, or M for ground items." if loc.lang == 'en' else "Koi manzil track nahi ho rahi. Janwaron ke liay A, Travel Points ke liay K, ya samaan ke liay M dabayein."
            if self.speech:
                self.speech.speak(msg)
            if self.audio:
                self.audio.play_error()
            return

        tx, ty, target_name, _, target_type, extra_ref = self.active_target
        if target_type == 'creature' and extra_ref:
            if not getattr(extra_ref, 'is_alive', True):
                msg = f"{target_name} has fallen and is no longer active." if loc.lang == 'en' else f"{target_name} dharram se gir chuka hai aur zinda nahi hai."
                if self.speech:
                    self.speech.speak(msg)
                self.active_target = None
                return
            tx, ty = extra_ref.x, extra_ref.y

        dx = tx - character.pos_x
        dy = ty - character.pos_y
        dist = abs(dx) + abs(dy)

        pan = self._calc_pan(dx, dy, character.facing)
        if self.audio:
            self.audio.play_sonar_beep(pan=pan)

        if dist == 0:
            if target_type == 'travel_point':
                if self.audio:
                    self.audio.play_portalopen()
                dest_str = world.get_realm_display_name(extra_ref) if (extra_ref and hasattr(world, 'get_realm_display_name')) else target_name
                msg = f"You are standing right at the {target_name}! Press Shift + Enter to cross into {dest_str}." if loc.lang == 'en' else f"Aap {target_name} par kharay hain! {dest_str} mein dakhil honay ke liay Shift + Enter dabayein."
            elif target_type == 'creature':
                msg = f"You are standing right with the {target_name}! Press Spacebar to attack or hunt." if loc.lang == 'en' else f"Aap bilkul {target_name} ke paas kharay hain! Hamla ya shikar karne ke liay Spacebar dabayein."
            else:
                msg = f"You are standing right on the {target_name}! Press Enter to collect it." if loc.lang == 'en' else f"Aap {target_name} par kharay hain! Uthanay ke liay Enter dabayein."
            if self.speech:
                self.speech.speak(msg)
            return

        dir_name = self._get_direction_name(dx, dy)
        rel_facing = self._get_relative_facing(dx, dy, character.facing)

        msg = f"Target: {target_name} is {dist} tiles away to the {dir_name} ({rel_facing})." if loc.lang == 'en' else f"Manzil: {target_name} {dist} tiles door {dir_name} ({rel_facing}) mein hai."
        if self.speech:
            self.speech.speak(msg)

    def update_ping(self, world, character):
        """Called periodically while walking to play directional sonar beeps toward target."""
        if not self.active_target:
            return

        tx, ty, item_name, _, target_type, extra_ref = self.active_target
        if target_type == 'creature' and extra_ref:
            if not getattr(extra_ref, 'is_alive', True):
                self.active_target = None
                return
            tx, ty = extra_ref.x, extra_ref.y

        dx = tx - character.pos_x
        dy = ty - character.pos_y

        # Reached destination!
        if dx == 0 and dy == 0:
            if target_type == 'travel_point':
                if self.audio:
                    self.audio.play_portalopen()
                dest_str = world.get_realm_display_name(extra_ref) if (extra_ref and hasattr(world, 'get_realm_display_name')) else item_name
                msg = f"You have reached the {item_name}! Press Shift + Enter to cross into {dest_str}." if loc.lang == 'en' else f"Aap {item_name} par pohanch gaye hain! {dest_str} mein dakhil honay ke liay Shift + Enter dabayein."
            elif target_type == 'creature':
                if self.audio:
                    self.audio.play_item_found()
                msg = f"You have reached the {item_name}! Press Spacebar to attack or hunt." if loc.lang == 'en' else f"Aap {item_name} ke paas pohanch gaye hain! Hamla ya shikar karne ke liay Spacebar dabayein."
            else:
                if self.audio:
                    self.audio.play_item_found()
                msg = f"You have reached the {item_name}! Press Enter to collect it." if loc.lang == 'en' else f"Aap {item_name} ke paas pohanch gaye hain! Uthanay ke liay Enter dabayein."
            
            if self.speech:
                self.speech.speak(msg)
            if target_type != 'creature':
                self.active_target = None
            return

        pan = self._calc_pan(dx, dy, character.facing)
        if self.audio:
            self.audio.play_sonar_beep(pan=pan)

    def _calc_pan(self, dx, dy, facing):
        """Calculates stereo pan (-1.0 to +1.0) relative to player's facing direction."""
        if facing == 'North':
            rel_x, rel_y = dx, dy
        elif facing == 'South':
            rel_x, rel_y = -dx, -dy
        elif facing == 'East':
            rel_x, rel_y = -dy, dx
        elif facing == 'West':
            rel_x, rel_y = dy, -dx
        else:
            rel_x, rel_y = dx, dy

        total = abs(rel_x) + abs(rel_y)
        if total == 0:
            return 0.0
        return max(-1.0, min(1.0, rel_x / total))

    def _get_relative_facing(self, dx, dy, facing):
        """Calculates direction relative to player's current orientation (ahead, behind, right, left)."""
        if facing == 'North':
            rel_x, rel_y = dx, dy
        elif facing == 'South':
            rel_x, rel_y = -dx, -dy
        elif facing == 'East':
            rel_x, rel_y = -dy, dx
        elif facing == 'West':
            rel_x, rel_y = dy, -dx
        else:
            rel_x, rel_y = dx, dy

        if abs(rel_y) >= abs(rel_x):
            if rel_y > 0:
                return "directly ahead" if loc.lang == 'en' else "seedha samnay"
            else:
                return "behind you" if loc.lang == 'en' else "aap ke peeche"
        else:
            if rel_x > 0:
                return "to your right" if loc.lang == 'en' else "aap ke daen taraf"
            else:
                return "to your left" if loc.lang == 'en' else "aap ke baen taraf"

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
