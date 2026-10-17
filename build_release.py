"""
Journey of Mankind - Automated Build & Inno Setup Packaging Script
Builds standalone Windows 10 & 11 executable and accessible installer.
"""

import os
import sys
import shutil
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ISCC_PATH = r"C:\Users\Shakeel\AppData\Local\Programs\Inno Setup 6\ISCC.exe"

def build():
    print("=" * 60)
    print("1. RUNNING PYINSTALLER TO BUILD STANDALONE EXECUTABLE...")
    print("=" * 60)
    
    dist_dir = os.path.join(SCRIPT_DIR, "dist")
    build_dir = os.path.join(SCRIPT_DIR, "build")
    
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm",
        "--onedir",
        "--windowed",
        "--name", "JourneyOfMankind",
        "--icon", os.path.join(SCRIPT_DIR, "app_icon.ico"),
        "--add-data", f"{os.path.join(SCRIPT_DIR, 'sounds')};sounds",
        "--add-data", f"{os.path.join(SCRIPT_DIR, 'version.json')};.",
        "--add-data", f"{os.path.join(SCRIPT_DIR, 'README.md')};.",
        "--add-data", f"{os.path.join(SCRIPT_DIR, 'app_icon.ico')};.",
        "--collect-all", "accessible_output2",
        "--collect-all", "libloader",
        "--collect-all", "platform_utils",
        "--collect-all", "win32com",
        "--hidden-import", "pygame",
        "--hidden-import", "sqlite3",
        "--hidden-import", "win32com",
        "--hidden-import", "win32com.client",
        "--hidden-import", "pywintypes",
        "--hidden-import", "pythoncom",
        "--hidden-import", "accessible_output2.outputs.auto",
        "--hidden-import", "accessible_output2.outputs.nvda",
        "--hidden-import", "accessible_output2.outputs.jaws",
        "--hidden-import", "accessible_output2.outputs.sapi5",
        os.path.join(SCRIPT_DIR, "main.py")
    ]
    
    res = subprocess.run(cmd, cwd=SCRIPT_DIR)
    if res.returncode != 0:
        print("[FAIL] PyInstaller failed with exit code:", res.returncode)
        sys.exit(res.returncode)
        
    exe_target = os.path.join(dist_dir, "JourneyOfMankind", "JourneyOfMankind.exe")
    if not os.path.exists(exe_target):
        print("[FAIL] Executable not found at:", exe_target)
        sys.exit(1)
        
    print(f"[PASS] Successfully built {exe_target}")
    
    # Copy app_icon.ico and sounds directly to dist directory as well
    shutil.copy2(os.path.join(SCRIPT_DIR, "app_icon.ico"), os.path.join(dist_dir, "JourneyOfMankind", "app_icon.ico"))
    shutil.copy2(os.path.join(SCRIPT_DIR, "version.json"), os.path.join(dist_dir, "JourneyOfMankind", "version.json"))
    dist_sounds = os.path.join(dist_dir, "JourneyOfMankind", "sounds")
    if not os.path.exists(dist_sounds):
        shutil.copytree(os.path.join(SCRIPT_DIR, "sounds"), dist_sounds)
    
    print("=" * 60)
    print("2. PREPARING INNO SETUP SCRIPT FOR WINDOWS 10 / 11 INSTALLER...")
    print("=" * 60)
    
    iss_content = f"""
; Journey of Mankind (Safar-e-Insaan) - Inno Setup Script
; Compatible with Windows 10 & Windows 11 (x64)
; Fully accessible with NVDA, JAWS, Narrator

#define MyAppName "Journey of Mankind"
#define MyAppVersion "1.2.0"
#define MyAppPublisher "Shakeel Ahmad Akash"
#define MyAppURL "https://github.com/shakeelahmadakash64-dev/Journey_Of_Mankind"
#define MyAppExeName "JourneyOfMankind.exe"

[Setup]
AppId={{{{B73F8E4D-9321-41F6-A063-88225586B7FA}}}}
AppName={{#MyAppName}}
AppVersion={{#MyAppVersion}}
AppVerName={{#MyAppName}} v{{#MyAppVersion}}
AppPublisher={{#MyAppPublisher}}
AppPublisherURL={{#MyAppURL}}
AppSupportURL={{#MyAppURL}}
AppUpdatesURL={{#MyAppURL}}
DefaultDirName={{autopf}}\\{{#MyAppName}}
DefaultGroupName={{#MyAppName}}
AllowNoIcons=yes
LicenseFile={os.path.join(SCRIPT_DIR, 'README.md')}
OutputDir={os.path.join(SCRIPT_DIR, 'dist_installer')}
OutputBaseFilename=Journey_Of_Mankind_Setup_v1.2.0
SetupIconFile={os.path.join(SCRIPT_DIR, 'app_icon.ico')}
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
ArchitecturesInstallIn64BitMode=x64compatible
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
MinVersion=10.0

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{{cm:CreateDesktopIcon}}"; GroupDescription: "{{cm:AdditionalIcons}}"

[Files]
Source: "{os.path.join(dist_dir, 'JourneyOfMankind', '*')}"; DestDir: "{{app}}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{{group}}\\{{#MyAppName}}"; Filename: "{{app}}\\{{#MyAppExeName}}"; IconFilename: "{{app}}\\app_icon.ico"
Name: "{{group}}\\Uninstall {{#MyAppName}}"; Filename: "{{uninstallexe}}"
Name: "{{autodesktop}}\\{{#MyAppName}}"; Filename: "{{app}}\\{{#MyAppExeName}}"; IconFilename: "{{app}}\\app_icon.ico"; Tasks: desktopicon

[Run]
Filename: "{{app}}\\{{#MyAppExeName}}"; Description: "{{cm:LaunchProgram,{{#StringChange(MyAppName, '&', '&&')}}}}"; Flags: nowait postinstall skipifsilent
"""
    
    iss_file = os.path.join(SCRIPT_DIR, "installer.iss")
    with open(iss_file, "w", encoding="utf-8") as f:
        f.write(iss_content.strip())
    print("[PASS] Generated installer.iss")
    
    print("=" * 60)
    print("3. COMPILING WINDOWS 10 / 11 SETUP INSTALLER VIA INNO SETUP...")
    print("=" * 60)
    
    os.makedirs(os.path.join(SCRIPT_DIR, "dist_installer"), exist_ok=True)
    res_iss = subprocess.run([ISCC_PATH, iss_file], cwd=SCRIPT_DIR)
    if res_iss.returncode != 0:
        print("[FAIL] Inno Setup compiler failed with exit code:", res_iss.returncode)
        sys.exit(res_iss.returncode)
        
    setup_exe = os.path.join(SCRIPT_DIR, "dist_installer", "Journey_Of_Mankind_Setup_v1.2.0.exe")
    if not os.path.exists(setup_exe):
        print("[FAIL] Installer exe not found at:", setup_exe)
        sys.exit(1)
        
    size_mb = os.path.getsize(setup_exe) / (1024 * 1024)
    print("=" * 60)
    print(f"[SUCCESS] SETUP INSTALLER CREATED SUCCESSFULLY!")
    print(f"Path: {setup_exe}")
    print(f"Size: {size_mb:.2f} MB")
    print("=" * 60)

if __name__ == '__main__':
    build()
