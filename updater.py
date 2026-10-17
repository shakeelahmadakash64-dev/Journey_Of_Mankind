"""
Journey of Mankind - Standalone GitHub Auto-Updater
Run this script or double-click update.bat anytime to check and download updates directly from GitHub.
"""
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from core.updater import CURRENT_VERSION, check_for_update, download_and_apply_update

if __name__ == '__main__':
    print(f"Checking for Journey of Mankind updates from GitHub (Current Version: v{CURRENT_VERSION})...")
    has_up, info, msg = check_for_update(silent=False)
    print(msg)
    if has_up:
        ans = input("Download and install this update now? [Y/n]: ").strip().lower()
        if ans in ('', 'y', 'yes'):
            ok, res = download_and_apply_update()
            print(res)
    else:
        ans = input("Do you want to reinstall/verify latest files from GitHub? [y/N]: ").strip().lower()
        if ans in ('y', 'yes'):
            ok, res = download_and_apply_update()
            print(res)
