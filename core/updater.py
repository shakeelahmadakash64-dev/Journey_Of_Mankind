"""
Journey of Mankind - GitHub Auto-Updater System
Checks GitHub repository for latest releases and updates,
downloads new files directly from GitHub, and safely updates game assets
and code without overwriting player save database (mankind_data.db).
Accessible with full speech synthesizer announcements and audio earcons.
"""

import os
import sys
import json
import ssl
import shutil
import zipfile
import tempfile
import urllib.request
from core.localization import loc

CURRENT_VERSION = "1.2.0"
GITHUB_OWNER = "shakeelahmadakash64-dev"
GITHUB_REPO = "Journey_Of_Mankind"
VERSION_URL = f"https://raw.githubusercontent.com/{GITHUB_OWNER}/{GITHUB_REPO}/main/version.json"
ZIP_URL = f"https://github.com/{GITHUB_OWNER}/{GITHUB_REPO}/archive/refs/heads/main.zip"

PRESERVED_FILES = {
    'mankind_data.db',
    'error.log',
    '.git',
    '__pycache__'
}

def parse_version(ver_str):
    """Parses semantic version string like '1.2.0' into tuple of integers."""
    try:
        parts = ver_str.strip().lstrip('v').split('.')
        return tuple(int(p) for p in parts if p.isdigit())
    except Exception:
        return (0, 0, 0)

def get_ssl_context():
    """Returns SSL context that works reliably across diverse Windows setups."""
    try:
        return ssl.create_default_context()
    except Exception:
        return ssl._create_unverified_context()

def check_for_update(audio=None, speech=None, silent=False):
    """
    Checks GitHub for the latest version of Journey of Mankind.
    Returns: (has_update, remote_info, message)
    """
    if not silent and speech:
        checking_msg = "Checking GitHub for updates..." if loc.lang == 'en' else "GitHub se update check ki ja rahi hai..."
        speech.speak(checking_msg)

    ctx = get_ssl_context()
    headers = {'User-Agent': 'JourneyOfMankind-Updater/1.2.0'}
    req = urllib.request.Request(VERSION_URL, headers=headers)

    try:
        with urllib.request.urlopen(req, context=ctx, timeout=8) as resp:
            if resp.status != 200:
                raise Exception(f"HTTP Status {resp.status}")
            data = json.loads(resp.read().decode('utf-8'))

        remote_ver_str = data.get('version', '1.0.0')
        remote_ver = parse_version(remote_ver_str)
        local_ver = parse_version(CURRENT_VERSION)

        changelog = data.get('changelog_ur' if loc.lang == 'ur' else 'changelog_en', '')

        if remote_ver > local_ver:
            msg = (
                f"A new update v{remote_ver_str} is available on GitHub! Your version: v{CURRENT_VERSION}. "
                f"Changes: {changelog}" if loc.lang == 'en' else
                f"GitHub par nayi update v{remote_ver_str} dastiyab hai! Aap ka version: v{CURRENT_VERSION}. "
                f"Tabdeeliyan: {changelog}"
            )
            if not silent:
                if audio:
                    audio.play("item_found")
                if speech:
                    speech.speak(msg)
            return (True, data, msg)
        else:
            msg = (
                f"Your game is up to date (Version {CURRENT_VERSION}). No new updates available." if loc.lang == 'en' else
                f"Aap ki game bilkul updated hai (Version {CURRENT_VERSION}). Koi nayi update darkaar nahi."
            )
            if not silent:
                if audio:
                    audio.play("menu_select")
                if speech:
                    speech.speak(msg)
            return (False, data, msg)

    except Exception as e:
        err_msg = (
            f"Could not connect to GitHub updater: {e}" if loc.lang == 'en' else
            f"GitHub updater se rabta nahi ho saka: {e}"
        )
        if not silent:
            if audio:
                audio.play_error()
            if speech:
                speech.speak(err_msg)
        return (False, None, err_msg)

def download_and_apply_update(audio=None, speech=None, progress_callback=None):
    """
    Downloads the latest zip repository from GitHub, extracts it,
    and updates game files while strictly preserving player database (mankind_data.db).
    Returns: (success, message)
    """
    msg_start = "Downloading latest update from GitHub..." if loc.lang == 'en' else "GitHub se taza tareen update download ho rahi hai..."
    if speech:
        speech.speak(msg_start)
    if audio:
        audio.play_sonar_beep()

    ctx = get_ssl_context()
    headers = {'User-Agent': 'JourneyOfMankind-Updater/1.2.0'}
    req = urllib.request.Request(ZIP_URL, headers=headers)

    if getattr(sys, 'frozen', False):
        game_dir = os.path.dirname(sys.executable)
    else:
        game_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    temp_dir = tempfile.mkdtemp(prefix='mankind_update_')
    zip_path = os.path.join(temp_dir, 'latest_update.zip')

    try:
        # Download ZIP
        with urllib.request.urlopen(req, context=ctx, timeout=30) as resp, open(zip_path, 'wb') as out_f:
            total_size = resp.getheader('Content-Length')
            total_size = int(total_size) if total_size else None
            downloaded = 0
            block_size = 65536
            while True:
                chunk = resp.read(block_size)
                if not chunk:
                    break
                out_f.write(chunk)
                downloaded += len(chunk)
                if progress_callback:
                    progress_callback(downloaded, total_size)

        msg_extract = "Extracting and applying update..." if loc.lang == 'en' else "Update files extract aur install ho rahi hain..."
        if speech:
            speech.speak(msg_extract)

        # Unzip
        extract_dir = os.path.join(temp_dir, 'extracted')
        with zipfile.ZipFile(zip_path, 'r') as zf:
            zf.extractall(extract_dir)

        # Find the inner directory created by GitHub (e.g. Journey_Of_Mankind-main)
        inner_dirs = [os.path.join(extract_dir, d) for d in os.listdir(extract_dir) if os.path.isdir(os.path.join(extract_dir, d))]
        src_root = inner_dirs[0] if inner_dirs else extract_dir

        # Copy updated files over game_dir, skipping preserved files
        copied_count = 0
        for root, dirs, files in os.walk(src_root):
            rel_path = os.path.relpath(root, src_root)
            dest_dir = os.path.join(game_dir, rel_path)
            
            # Skip .git or __pycache__
            if '.git' in rel_path.split(os.sep) or '__pycache__' in rel_path.split(os.sep):
                continue
            
            os.makedirs(dest_dir, exist_ok=True)
            for f in files:
                if f in PRESERVED_FILES or f.endswith('.db') or f.endswith('.log'):
                    # Strictly preserve player save file
                    continue
                src_file = os.path.join(root, f)
                dest_file = os.path.join(dest_dir, f)
                shutil.copy2(src_file, dest_file)
                copied_count += 1

        success_msg = (
            f"Update completed successfully ({copied_count} files updated)! Your save data is safe. Please restart the game." if loc.lang == 'en' else
            f"Update kamyabi se mukammal ho gayi ({copied_count} files update huin)! Aap ka record mehfooz hai. Khel dobara shuru karein."
        )
        if audio:
            audio.play("craft_weapon")
            audio.play_item_found()
        if speech:
            speech.speak(success_msg)

        return (True, success_msg)

    except Exception as e:
        fail_msg = (
            f"Update installation failed: {e}" if loc.lang == 'en' else
            f"Update install karne mein khata aayi: {e}"
        )
        if audio:
            audio.play_error()
        if speech:
            speech.speak(fail_msg)
        return (False, fail_msg)

    finally:
        try:
            shutil.rmtree(temp_dir, ignore_errors=True)
        except Exception:
            pass

def open_updater_menu(screen=None, audio=None, speech=None):
    """Interactive Accessible Menu for checking and applying GitHub updates."""
    from game.menu import AccessibleMenu

    def run_check():
        has_update, info, msg = check_for_update(audio=audio, speech=speech, silent=False)
        return "CHECKED"

    def run_apply():
        has_update, info, _ = check_for_update(audio=audio, speech=speech, silent=True)
        if has_update:
            download_and_apply_update(audio=audio, speech=speech)
        else:
            msg = (
                f"You already have the latest version (v{CURRENT_VERSION})! Re-installing latest build from GitHub..." if loc.lang == 'en' else
                f"Aap ke paas pehle se latest version (v{CURRENT_VERSION}) mojood hai! Dobara reinstall kiya ja raha hai..."
            )
            if speech:
                speech.speak(msg)
            download_and_apply_update(audio=audio, speech=speech)
        return "APPLIED"

    options = [
        (loc.tr('updater_check'), run_check),
        (loc.tr('updater_install'), run_apply),
        (loc.tr('back'), lambda: "BACK")
    ]

    title = f"GitHub Auto-Updater (v{CURRENT_VERSION})" if loc.lang == 'en' else f"GitHub Auto-Updater (Version {CURRENT_VERSION})"
    menu = AccessibleMenu(title, options, audio, speech)
    menu.run(screen)

if __name__ == '__main__':
    print(f"Journey of Mankind - Auto-Updater CLI (v{CURRENT_VERSION})")
    has_update, info, msg = check_for_update(silent=False)
    print(msg)
    if has_update:
        ans = input("Do you want to download and install this update now? [y/N]: ").strip().lower()
        if ans == 'y':
            ok, res = download_and_apply_update()
            print(res)
