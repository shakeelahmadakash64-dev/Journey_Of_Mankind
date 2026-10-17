"""
Journey of Mankind - GitHub Auto-Updater System
Checks GitHub repository for latest releases and updates,
downloads new files directly from GitHub, and safely updates game assets
and code without overwriting player save database (mankind_data.db).
Fully asynchronous and accessible with speech synthesizer announcements,
audio earcons, and active GUI message pumping to prevent Windows 'Not Responding' freezes.
"""

import os
import sys
import json
import ssl
import shutil
import zipfile
import tempfile
import threading
import time
import urllib.request
import pygame
from core.localization import loc

CURRENT_VERSION = "1.3.0"
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

def pump_gui_events():
    """Pumps pygame event queue so Windows knows the application is fully responsive."""
    try:
        if pygame.get_init():
            pygame.event.pump()
    except Exception:
        pass

def run_with_gui_pump(task_fn, *args, **kwargs):
    """
    Executes a blocking network or file operation in a background thread
    while continuously pumping pygame events to prevent 'Not Responding' OS freezes.
    """
    res_holder = [None]
    err_holder = [None]

    def worker():
        try:
            res_holder[0] = task_fn(*args, **kwargs)
        except Exception as e:
            err_holder[0] = e

    t = threading.Thread(target=worker, daemon=True)
    t.start()

    while t.is_alive():
        pump_gui_events()
        time.sleep(0.03)

    if err_holder[0] is not None:
        raise err_holder[0]
    return res_holder[0]

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

def _fetch_remote_version():
    """Performs HTTP fetch of version.json from GitHub."""
    ctx = get_ssl_context()
    headers = {'User-Agent': 'JourneyOfMankind-Updater/1.2.0'}
    req = urllib.request.Request(VERSION_URL, headers=headers)
    with urllib.request.urlopen(req, context=ctx, timeout=8) as resp:
        if resp.status != 200:
            raise Exception(f"HTTP Status {resp.status}")
        return json.loads(resp.read().decode('utf-8'))

def check_for_update(audio=None, speech=None, silent=False):
    """
    Checks GitHub for the latest version of Journey of Mankind.
    Keeps GUI responsive and never freezes the application.
    Returns: (has_update, remote_info, message)
    """
    if not silent and speech:
        checking_msg = "Checking GitHub for updates..." if loc.lang == 'en' else "GitHub se update check ki ja rahi hai..."
        speech.speak(checking_msg)

    try:
        data = run_with_gui_pump(_fetch_remote_version)

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
            msg = loc.tr('updater_already_latest', version=CURRENT_VERSION)
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

def _download_and_extract(progress_callback=None):
    """Downloads ZIP archive from GitHub and unpacks to temporary directory."""
    ctx = get_ssl_context()
    headers = {'User-Agent': 'JourneyOfMankind-Updater/1.2.0'}
    req = urllib.request.Request(ZIP_URL, headers=headers)

    temp_dir = tempfile.mkdtemp(prefix='mankind_update_')
    zip_path = os.path.join(temp_dir, 'latest_update.zip')

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
            pump_gui_events()
            if progress_callback:
                progress_callback(downloaded, total_size)

    extract_dir = os.path.join(temp_dir, 'extracted')
    with zipfile.ZipFile(zip_path, 'r') as zf:
        zf.extractall(extract_dir)

    inner_dirs = [os.path.join(extract_dir, d) for d in os.listdir(extract_dir) if os.path.isdir(os.path.join(extract_dir, d))]
    src_root = inner_dirs[0] if inner_dirs else extract_dir
    return temp_dir, src_root

def download_and_apply_update(audio=None, speech=None, progress_callback=None):
    """
    Downloads the latest zip repository from GitHub, extracts it,
    and updates game files while strictly preserving player database (mankind_data.db).
    Guarantees no UI freeze during download and extraction.
    Returns: (success, message)
    """
    msg_start = "Downloading latest update from GitHub..." if loc.lang == 'en' else "GitHub se taza tareen update download ho rahi hai..."
    if speech:
        speech.speak(msg_start)
    if audio:
        audio.play_sonar_beep()

    if getattr(sys, 'frozen', False):
        game_dir = os.path.dirname(sys.executable)
    else:
        game_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    temp_dir = None
    try:
        temp_dir, src_root = run_with_gui_pump(_download_and_extract, progress_callback)

        msg_extract = "Applying updated files..." if loc.lang == 'en' else "Update files install ho rahi hain..."
        if speech:
            speech.speak(msg_extract)

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
                pump_gui_events()

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
        if temp_dir and os.path.exists(temp_dir):
            try:
                shutil.rmtree(temp_dir, ignore_errors=True)
            except Exception:
                pass

def open_updater_menu(screen=None, audio=None, speech=None):
    """Interactive Accessible Menu for checking and applying GitHub updates."""
    from game.menu import AccessibleMenu

    def run_check():
        check_for_update(audio=audio, speech=speech, silent=False)
        return "CHECKED"

    def run_apply():
        # First check if an update is genuinely available without audible chime
        has_update, info, _ = check_for_update(audio=audio, speech=speech, silent=True)
        if has_update:
            download_and_apply_update(audio=audio, speech=speech)
        else:
            # Player already has the latest version: Do NOT download, speak confirmation clearly!
            latest_msg = loc.tr('updater_already_latest', version=CURRENT_VERSION)
            if audio:
                audio.play("menu_select")
            if speech:
                speech.speak(latest_msg)
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
    else:
        print("No update needed. You have the latest version.")
