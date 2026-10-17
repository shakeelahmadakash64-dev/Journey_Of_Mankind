"""
Journey of Mankind - Stone Age Weapon & Tool Crafting System
Enables early humans to fashion spears, obsidian daggers, fire torches, bone clubs, and slings.
Fully accessible with voice narration, recipe checks, and audio knapping effects.
"""

from core.localization import loc
from game.menu import AccessibleMenu

class CraftingRecipe:
    def __init__(self, recipe_id, name_key, desc_key, req_key, ingredients, yield_item_id, yield_key, requires_fire=False, damage=10):
        self.recipe_id = recipe_id
        self.name_key = name_key
        self.desc_key = desc_key
        self.req_key = req_key
        self.ingredients = ingredients  # list of tuples: [('item_id', required_qty), ...]
        self.yield_item_id = yield_item_id
        self.yield_key = yield_key
        self.requires_fire = requires_fire
        self.damage = damage

class CraftingSystem:
    def __init__(self, audio=None, speech=None, quest_system=None):
        self.audio = audio
        self.speech = speech
        self.quest_system = quest_system
        self.recipes = [
            CraftingRecipe(
                recipe_id='spear',
                name_key='craft_spear_name',
                desc_key='craft_spear_desc',
                req_key='craft_spear_req',
                ingredients=[('wood_stick', 2), ('flint_stone', 1)],
                yield_item_id='spear',
                yield_key='item_spear',
                damage=25
            ),
            CraftingRecipe(
                recipe_id='obsidian_dagger',
                name_key='craft_dagger_name',
                desc_key='craft_dagger_desc',
                req_key='craft_dagger_req',
                ingredients=[('obsidian_shard', 1), ('wood_stick', 1), ('reed_fiber', 1)],
                yield_item_id='obsidian_dagger',
                yield_key='item_obsidian_dagger',
                damage=35
            ),
            CraftingRecipe(
                recipe_id='torch',
                name_key='craft_torch_name',
                desc_key='craft_torch_desc',
                req_key='craft_torch_req',
                ingredients=[('wood_stick', 1), ('reed_fiber', 1)],
                yield_item_id='torch',
                yield_key='item_torch',
                requires_fire=True,
                damage=15
            ),
            CraftingRecipe(
                recipe_id='bone_club',
                name_key='craft_club_name',
                desc_key='craft_club_desc',
                req_key='craft_club_req',
                ingredients=[('animal_bone', 1), ('reed_fiber', 1)],
                yield_item_id='bone_club',
                yield_key='item_bone_club',
                damage=30
            ),
            CraftingRecipe(
                recipe_id='sling',
                name_key='craft_sling_name',
                desc_key='craft_sling_desc',
                req_key='craft_sling_req',
                ingredients=[('reed_fiber', 2), ('flint_stone', 1)],
                yield_item_id='sling',
                yield_key='item_sling',
                damage=18
            )
        ]

    def has_ingredients(self, recipe, character):
        """Check if character has all required materials."""
        if recipe.requires_fire and not character.has_fire:
            return False, loc.tr('craft_missing_mat', req=loc.tr(recipe.req_key))

        for item_id, req_qty in recipe.ingredients:
            item = next((i for i in character.inventory if i['id'] == item_id), None)
            if not item or item['quantity'] < req_qty:
                return False, loc.tr('craft_missing_mat', req=loc.tr(recipe.req_key))
        return True, ""

    def craft_item(self, recipe, character):
        """Consume materials and craft the weapon/tool."""
        ok, err_msg = self.has_ingredients(recipe, character)
        if not ok:
            if self.speech:
                self.speech.speak(err_msg)
            if self.audio:
                self.audio.play_error()
            return False

        # Deduct materials
        for item_id, req_qty in recipe.ingredients:
            item = next(i for i in character.inventory if i['id'] == item_id)
            item['quantity'] -= req_qty
            if item['quantity'] <= 0:
                character.inventory.remove(item)

        # Add crafted weapon
        yield_name = loc.tr(recipe.yield_key)
        character.add_item(recipe.yield_item_id, yield_name, 1)
        character.equipped_weapon = recipe.yield_item_id
        character.weapon_damage = recipe.damage

        if self.audio:
            self.audio.play_craft()

        success_msg = loc.tr('craft_success', item=yield_name)
        if self.speech:
            self.speech.speak(f"{success_msg} {loc.tr('craft_equipped', weapon=yield_name)}")

        qs = getattr(self, 'quest_system', None) or getattr(character, 'quest_system', None)
        if qs:
            if recipe.recipe_id == 'spear':
                qs.check_milestone(character, 'spear')
            elif recipe.recipe_id == 'obsidian_dagger':
                qs.check_milestone(character, 'craft_dagger')
            elif recipe.recipe_id == 'bone_club':
                qs.check_milestone(character, 'craft_club')

        return True

    def open_crafting_menu(self, character, screen=None):
        """Interactive audio menu for selecting and forging weapons."""
        options = []
        for recipe in self.recipes:
            label = f"{loc.tr(recipe.name_key)} - {loc.tr(recipe.req_key)}"
            def make_craft_fn(r=recipe):
                return lambda: self.craft_item(r, character)
            options.append((label, make_craft_fn()))
            
        options.append((loc.tr('back'), lambda: "BACK"))

        menu = AccessibleMenu(loc.tr('craft_menu_title'), options, self.audio, self.speech)
        menu.run(screen)
