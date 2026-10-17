# 🌍 Journey of Mankind (Safar-e-Insaan)
### The Ultimate Accessible Audio Survival & Historical Evolution RPG
**Version: 1.2.0** | Built for Blind and Visually Impaired Gamers with Full NVDA, JAWS & SAPI5 Integration and 3D Binaural Positional Audio.

---

## 🌟 What is Journey of Mankind?
**Journey of Mankind (Safar-e-Insaan)** is a deeply immersive, narrative-driven audio RPG where players guide humanity from the harsh survival of the primordial Stone Age through 5 monumental historical epochs to the dawn of civilizations.

Every element is designed from the ground up for complete blindness accessibility:
* **True 3D Spatial Audio & Binaural Panning**: Footsteps, creature roars, running water, wind, and mechanical sounds are dynamically panned across stereo headphones.
* **Seamless Screen Reader Speech**: Full support for NVDA screen reader, JAWS, and universal Windows SAPI5 voice fallback.
* **Authentic Studio Foley**: Realistic mechanical metal zippers for satchel management, heavy oak door creaks, crackling campfires, and authentic tactile audio feedback.
* **Direct GitHub Auto-Updater**: Directly check, download, and apply updates from within the game menus without losing player databases or save files.

---

## 🏛️ The 5 Historical Epochs (Insaniyat Ke 5 Azeem Adwaar)
Players progress through history by accomplishing landmark survival feats:
1. **Era 1: Lower Paleolithic (Aag aur Qadeem Shikar)**
   * Strike spark with flint, craft hardwood spears, hunt prehistoric beasts, and roast meat over flames.
2. **Era 2: Upper Paleolithic (Barafani Dasht aur Mammoth Hunt)**
   * Brave the glacial winds, track woolly mammoths, construct bone clubs, and sew warm hide clothing.
3. **Era 3: Mesolithic & Neolithic (Ziraat, Janwaron Ki Parwarish aur Panahgah)**
   * Domesticate wild wolves into loyal hunting companions, farm fertile riverbeds, and construct a 5x5 secure wooden shelter.
4. **Era 4: Chalcolithic & Bronze Age (Dhaat-kari aur Obsidian)**
   * Mine volcanic obsidian, smelt bronze ingots, forge daggers, and build stone fortifications.
5. **Era 5: Iron Age & Dawn of Civilizations (Tehzeeb ka Aaghaz)**
   * Forge iron swords, establish trading routes across continents, write records in the historic diary, and build permanent settlements.

---

## 🎒 Books in the Player's Satchel (Player ka Bag)
Your bag opens and closes with realistic studio mechanical zipper audio (`bag_open.wav` / `bag_close.wav`). Inside, you carry:
* **📖 Survival Guide (Rahnuma Kitab)**: Text guide explaining all survival mechanics, navigation, and tips.
* **🔨 Crafting Guide (Dastkari Kitab)**: Step-by-step recipes for fires, spears, daggers, torches, and tools.
* **📜 Journey Diary (Safar-Nama)**: Automatically updates as you achieve epoch milestones, recording your historical legacy.
* **Navigation Inside Books**:
  * `Tab` / `Shift + Tab`: Read next and previous pages with page-turn audio (`page_turn.wav`).
  * `G`: Listen to item usage details and historical purpose.
  * `Enter`: Hold/Equip item in hand.

---

## 🏕️ 5x5 Shelter Interior & Exploration
* Build a sturdy shelter on any open terrain.
* Press `Shift + Enter` while standing on a shelter to step inside.
* Realistic interior features:
  * Cozy shelter ambient audio (`ambience_shelter.wav`).
  * Footsteps on wooden planks (`footstep_wood`).
  * Explore Hearth `(0, 0)`, Bedroll `(0, 1)`, Meat Rack `(1, 0)`, Workbench `(0, -1)`, and Water Pitcher `(-1, 0)`.
  * **Secure Oak Door**: To exit, step to the doorway at `(0, -2)` and press `Shift + Enter`. Walking South does not accidentally trigger exit.

---

## 🔄 In-Game GitHub Auto-Updater
Keep your game updated directly from the official GitHub repository (`shakeelahmadakash64-dev/Journey_Of_Mankind`):
1. **Access Points**:
   * **Main Menu**: Select **"5. Check for Updates (GitHub) / Nayi Updates Check Karein"**.
   * **In-Game Tab Hub**: Press `Tab` during gameplay, select **"Check GitHub Updates"**.
   * **Standalone**: Double click `update.bat` or run `python updater.py`.
2. **Database Protection**: The updater replaces code, scripts, sounds, and assets while strictly preserving `mankind_data.db` and player accounts.

---

## 🌐 Multilingual Accessibility
Switch languages anytime on-the-fly via the Main Menu or in-game `Tab` Hub:
* 🇬🇧 **English (Primary International)**
* 🇵🇰 **Roman Urdu (Asaan Roman Urdu)**
* 🇪🇸 **Español (Spanish)**
* 🇫🇷 **Français (French)**
* 🇸🇦 **Al-Arabiya (Transliterated Arabic)**
* 🇮🇳 **Hindustani (Transliterated Hindi)**

---

## ⌨️ Controls Reference Table

| Key | Amal (Action) | Details |
| :--- | :--- | :--- |
| **Arrow Keys** | Walk / Face Direction | Step North, South, East, West with spatial footsteps |
| **Shift + Up/Down/Left/Right** | Change Direction Only | Turn facing heading (N, S, E, W) without moving |
| **Spacebar** | Use Equipped Weapon / Attack | Strike engaged predators with spear, dagger, or club |
| **Enter** | Pick Up Ground Item / Interact | Collect stones, wood, herbs, water into bag |
| **M (Tap Repeatedly)** | Scan & Cycle Ground Items | Cycles through nearby items with directional sonar ping |
| **Enter (While Scanning)** | Lock On Target Item | Locks tracking; follow the 3D pings to reach it |
| **A (Tap Repeatedly)** | Scan & Cycle Nearby Animals | Cycles through predators & wildlife with sound cues |
| **Enter (While Tracking Animal)** | Lock On Animal | Locks tracking to hunt or tame |
| **I** | Open / Close Bag | Realistic mechanical zipper sound |
| **G (Inside Bag)** | Item Explanation | Hear what the selected item does and how it is used |
| **Enter (Inside Bag)** | Hold / Equip Item | Equip weapon or tool in hand |
| **Tab** | In-Game Quick Hub | Quests, Language Switch, Diary, Updater, Weather |
| **Tab / Shift + Tab (In Books)** | Turn Pages | Navigate forward and backward through text pages |
| **Shift + Enter** | Gateway Travel / Shelter Door | Enter/Exit shelter at door, or cross map borders |
| **D** | Compass Heading | Hear current compass direction, coordinates, and elevation |
| **C** | Strike Campfire | Use flint and wood to strike a warm fire |
| **H / F / W / S / T** | Check Vitals | Health, Food, Water, Stamina, Body Temperature |
| **Q / Esc** | Save & Exit | Saves player vitals, era, and inventory to database |

---

## 🚀 Installation & Running

### Prerequisites
* Windows 10 or Windows 11
* Python 3.10+ (Recommended Python 3.12 - 3.14)
* Screen reader: NVDA (recommended), JAWS, or Windows SAPI5

### Quick Start
```powershell
# Clone the repository
git clone https://github.com/shakeelahmadakash64-dev/Journey_Of_Mankind.git
cd Journey_Of_Mankind

# Install dependencies
pip install pygame-ce

# Run the game
python main.py
```

---

## 📜 License & Credits
Developed with ❤️ by **Shakeel Ahmad Akash** for the international blind and visually impaired gaming community.
Free and Open Source under the MIT License.
