"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  TASK PLAYBOOK LIBRARY v2 — 3-Tier Deterministic Execution Routes           ║
║                                                                              ║
║  Tier 1 (cmd)      : Pure subprocess/shell — fastest, zero screen contact   ║
║  Tier 2 (keyboard) : pyautogui hotkeys only — no mouse coordinates          ║
║  Tier 3 (gui)      : Win+S search + clipboard typing + verified clicks      ║
╚══════════════════════════════════════════════════════════════════════════════╝

Step type reference:
  cmd          → subprocess.run(command, shell=True)
  delay        → time.sleep(seconds)
  type_clip    → pyperclip.copy(text) + Ctrl+V  [Unicode-safe typing]
  hotkey       → pyautogui.hotkey(*keys)
  press        → pyautogui.press(key)
  write_file   → write content to path
  screenshot   → mss capture to path
  win_search   → Win+S → type query → Enter  [universal app launcher]
  click_pct    → click at (screen_w * px, screen_h * py) [resolution-safe]
  scroll       → scroll up/down N clicks at position

{param} placeholders are filled from router-extracted parameters at runtime.
"""

# ══════════════════════════════════════════════════════════════════════════════
#  TIER 1 — CMD (subprocess, no GUI required)
# ══════════════════════════════════════════════════════════════════════════════

CMD_PLAYBOOKS: dict = {

    # ── Open Applications ─────────────────────────────────────────────────────
    "open_notepad": {
        "tier": "cmd", "description": "Open Microsoft Notepad",
        "examples": ["open notepad", "launch notepad", "open text editor", "start notepad"],
        "params": [],
        "steps": [
            {"type": "cmd",   "command": "start notepad.exe",      "label": "Launch Notepad"},
            {"type": "delay", "seconds": 1.5,                       "label": "Wait"},
        ]
    },
    "open_calculator": {
        "tier": "cmd", "description": "Open Windows Calculator",
        "examples": ["open calculator", "launch calc", "open calc", "start calculator"],
        "params": [],
        "steps": [
            {"type": "cmd",   "command": "start calc.exe",          "label": "Launch Calculator"},
            {"type": "delay", "seconds": 1.5,                       "label": "Wait"},
        ]
    },
    "open_paint": {
        "tier": "cmd", "description": "Open Microsoft Paint",
        "examples": ["open paint", "open mspaint", "launch paint", "open drawing app"],
        "params": [],
        "steps": [
            {"type": "cmd",   "command": "start mspaint.exe",       "label": "Launch Paint"},
            {"type": "delay", "seconds": 1.5,                       "label": "Wait"},
        ]
    },
    "open_file_explorer": {
        "tier": "cmd", "description": "Open Windows File Explorer",
        "examples": ["open file explorer", "open explorer", "open my computer", "open files"],
        "params": [],
        "steps": [
            {"type": "cmd",   "command": "start explorer.exe",      "label": "Launch Explorer"},
            {"type": "delay", "seconds": 1.0,                       "label": "Wait"},
        ]
    },
    "open_task_manager": {
        "tier": "cmd", "description": "Open Windows Task Manager",
        "examples": ["open task manager", "show processes", "launch taskmgr", "show running apps"],
        "params": [],
        "steps": [
            {"type": "cmd",   "command": "start taskmgr.exe",       "label": "Launch Task Manager"},
            {"type": "delay", "seconds": 1.5,                       "label": "Wait"},
        ]
    },
    "open_cmd": {
        "tier": "cmd", "description": "Open Command Prompt",
        "examples": ["open cmd", "open command prompt", "open terminal", "open console"],
        "params": [],
        "steps": [
            {"type": "cmd",   "command": "start cmd.exe",           "label": "Launch CMD"},
            {"type": "delay", "seconds": 1.0,                       "label": "Wait"},
        ]
    },
    "open_powershell": {
        "tier": "cmd", "description": "Open PowerShell",
        "examples": ["open powershell", "launch powershell", "open ps terminal"],
        "params": [],
        "steps": [
            {"type": "cmd",   "command": "start powershell.exe",    "label": "Launch PowerShell"},
            {"type": "delay", "seconds": 1.0,                       "label": "Wait"},
        ]
    },
    "open_settings": {
        "tier": "cmd", "description": "Open Windows Settings",
        "examples": ["open settings", "open windows settings", "system preferences"],
        "params": [],
        "steps": [
            {"type": "cmd",   "command": "start ms-settings:",      "label": "Open Settings"},
            {"type": "delay", "seconds": 1.5,                       "label": "Wait"},
        ]
    },
    "open_control_panel": {
        "tier": "cmd", "description": "Open Control Panel",
        "examples": ["open control panel", "control panel", "old settings"],
        "params": [],
        "steps": [
            {"type": "cmd",   "command": "start control",           "label": "Open Control Panel"},
            {"type": "delay", "seconds": 1.5,                       "label": "Wait"},
        ]
    },
    "open_chrome": {
        "tier": "cmd", "description": "Open Google Chrome",
        "examples": ["open chrome", "launch chrome", "open google chrome", "start chrome"],
        "params": [],
        "steps": [
            {"type": "cmd",   "command": "start chrome.exe",        "label": "Launch Chrome"},
            {"type": "delay", "seconds": 2.0,                       "label": "Wait"},
        ]
    },
    "open_edge": {
        "tier": "cmd", "description": "Open Microsoft Edge",
        "examples": ["open edge", "launch edge", "open microsoft edge", "open browser"],
        "params": [],
        "steps": [
            {"type": "cmd",   "command": "start msedge.exe",        "label": "Launch Edge"},
            {"type": "delay", "seconds": 2.0,                       "label": "Wait"},
        ]
    },
    "open_firefox": {
        "tier": "cmd", "description": "Open Mozilla Firefox",
        "examples": ["open firefox", "launch firefox", "open mozilla"],
        "params": [],
        "steps": [
            {"type": "cmd",   "command": "start firefox.exe",       "label": "Launch Firefox"},
            {"type": "delay", "seconds": 2.0,                       "label": "Wait"},
        ]
    },
    "open_word": {
        "tier": "cmd", "description": "Open Microsoft Word",
        "examples": ["open word", "launch microsoft word", "open word document", "start word"],
        "params": [],
        "steps": [
            {"type": "cmd",   "command": "start winword.exe",       "label": "Launch Word"},
            {"type": "delay", "seconds": 3.0,                       "label": "Wait for Word"},
        ]
    },
    "open_excel": {
        "tier": "cmd", "description": "Open Microsoft Excel",
        "examples": ["open excel", "launch excel", "open spreadsheet", "start excel"],
        "params": [],
        "steps": [
            {"type": "cmd",   "command": "start excel.exe",         "label": "Launch Excel"},
            {"type": "delay", "seconds": 3.0,                       "label": "Wait for Excel"},
        ]
    },
    "open_powerpoint": {
        "tier": "cmd", "description": "Open Microsoft PowerPoint",
        "examples": ["open powerpoint", "open presentation", "launch ppt", "start powerpoint"],
        "params": [],
        "steps": [
            {"type": "cmd",   "command": "start powerpnt.exe",      "label": "Launch PowerPoint"},
            {"type": "delay", "seconds": 3.0,                       "label": "Wait for PPT"},
        ]
    },
    "open_vs_code": {
        "tier": "cmd", "description": "Open Visual Studio Code",
        "examples": ["open vs code", "launch vscode", "open code editor", "open visual studio code"],
        "params": [],
        "steps": [
            {"type": "cmd",   "command": "code .",                  "label": "Launch VS Code"},
            {"type": "delay", "seconds": 3.0,                       "label": "Wait"},
        ]
    },
    "open_snipping_tool": {
        "tier": "cmd", "description": "Open Snipping Tool",
        "examples": ["open snipping tool", "snipping tool", "open screenshot tool"],
        "params": [],
        "steps": [
            {"type": "cmd",   "command": "start snippingtool.exe",  "label": "Launch Snipping Tool"},
            {"type": "delay", "seconds": 1.5,                       "label": "Wait"},
        ]
    },
    "open_on_screen_keyboard": {
        "tier": "cmd", "description": "Open on-screen keyboard",
        "examples": ["open on screen keyboard", "virtual keyboard", "on screen keyboard"],
        "params": [],
        "steps": [
            {"type": "cmd",   "command": "start osk.exe",           "label": "Launch OSK"},
            {"type": "delay", "seconds": 1.0,                       "label": "Wait"},
        ]
    },
    "open_magnifier": {
        "tier": "cmd", "description": "Open Windows Magnifier",
        "examples": ["open magnifier", "zoom screen", "screen magnifier"],
        "params": [],
        "steps": [
            {"type": "cmd",   "command": "start magnify.exe",       "label": "Launch Magnifier"},
            {"type": "delay", "seconds": 1.0,                       "label": "Wait"},
        ]
    },
    "open_remote_desktop": {
        "tier": "cmd", "description": "Open Remote Desktop Connection",
        "examples": ["open remote desktop", "rdp", "remote desktop connection"],
        "params": [],
        "steps": [
            {"type": "cmd",   "command": "start mstsc.exe",         "label": "Launch RDP"},
            {"type": "delay", "seconds": 1.5,                       "label": "Wait"},
        ]
    },
    "open_device_manager": {
        "tier": "cmd", "description": "Open Device Manager",
        "examples": ["open device manager", "device manager", "hardware manager"],
        "params": [],
        "steps": [
            {"type": "cmd",   "command": "start devmgmt.msc",       "label": "Launch Device Manager"},
            {"type": "delay", "seconds": 2.0,                       "label": "Wait"},
        ]
    },
    "open_disk_management": {
        "tier": "cmd", "description": "Open Disk Management",
        "examples": ["open disk management", "disk manager", "manage disks"],
        "params": [],
        "steps": [
            {"type": "cmd",   "command": "start diskmgmt.msc",      "label": "Launch Disk Management"},
            {"type": "delay", "seconds": 2.0,                       "label": "Wait"},
        ]
    },
    "open_event_viewer": {
        "tier": "cmd", "description": "Open Event Viewer",
        "examples": ["open event viewer", "event log", "system event viewer"],
        "params": [],
        "steps": [
            {"type": "cmd",   "command": "start eventvwr.msc",      "label": "Launch Event Viewer"},
            {"type": "delay", "seconds": 2.0,                       "label": "Wait"},
        ]
    },
    "open_registry_editor": {
        "tier": "cmd", "description": "Open Registry Editor",
        "examples": ["open registry editor", "regedit", "open registry"],
        "params": [],
        "steps": [
            {"type": "cmd",   "command": "start regedit.exe",       "label": "Launch Regedit"},
            {"type": "delay", "seconds": 2.0,                       "label": "Wait"},
        ]
    },

    # ── Settings Pages ────────────────────────────────────────────────────────
    "open_settings_wifi": {
        "tier": "cmd", "description": "Open Wi-Fi network settings",
        "examples": ["open wifi settings", "wi-fi settings", "network wifi settings"],
        "params": [],
        "steps": [
            {"type": "cmd",   "command": "start ms-settings:network-wifi",   "label": "Open WiFi Settings"},
            {"type": "delay", "seconds": 1.5,                                 "label": "Wait"},
        ]
    },
    "open_settings_bluetooth": {
        "tier": "cmd", "description": "Open Bluetooth settings",
        "examples": ["open bluetooth settings", "bluetooth settings", "manage bluetooth"],
        "params": [],
        "steps": [
            {"type": "cmd",   "command": "start ms-settings:bluetooth",      "label": "Open Bluetooth Settings"},
            {"type": "delay", "seconds": 1.5,                                 "label": "Wait"},
        ]
    },
    "open_settings_display": {
        "tier": "cmd", "description": "Open Display settings",
        "examples": ["open display settings", "screen settings", "monitor settings", "screen resolution"],
        "params": [],
        "steps": [
            {"type": "cmd",   "command": "start ms-settings:display",        "label": "Open Display Settings"},
            {"type": "delay", "seconds": 1.5,                                 "label": "Wait"},
        ]
    },
    "open_settings_sound": {
        "tier": "cmd", "description": "Open Sound settings",
        "examples": ["open sound settings", "audio settings", "speaker settings", "sound control"],
        "params": [],
        "steps": [
            {"type": "cmd",   "command": "start ms-settings:sound",          "label": "Open Sound Settings"},
            {"type": "delay", "seconds": 1.5,                                 "label": "Wait"},
        ]
    },
    "open_settings_apps": {
        "tier": "cmd", "description": "Open Apps & Features settings",
        "examples": ["open apps settings", "apps and features", "installed apps", "uninstall app"],
        "params": [],
        "steps": [
            {"type": "cmd",   "command": "start ms-settings:appsfeatures",   "label": "Open Apps Settings"},
            {"type": "delay", "seconds": 1.5,                                 "label": "Wait"},
        ]
    },
    "open_settings_startup": {
        "tier": "cmd", "description": "Open Startup Apps settings",
        "examples": ["open startup apps", "manage startup", "startup programs", "startup settings"],
        "params": [],
        "steps": [
            {"type": "cmd",   "command": "start ms-settings:startupapps",    "label": "Open Startup Apps"},
            {"type": "delay", "seconds": 1.5,                                 "label": "Wait"},
        ]
    },
    "open_settings_update": {
        "tier": "cmd", "description": "Open Windows Update settings",
        "examples": ["check windows update", "open update settings", "windows update", "update windows"],
        "params": [],
        "steps": [
            {"type": "cmd",   "command": "start ms-settings:windowsupdate",  "label": "Open Windows Update"},
            {"type": "delay", "seconds": 1.5,                                 "label": "Wait"},
        ]
    },
    "open_settings_privacy": {
        "tier": "cmd", "description": "Open Privacy settings",
        "examples": ["open privacy settings", "privacy settings", "app permissions"],
        "params": [],
        "steps": [
            {"type": "cmd",   "command": "start ms-settings:privacy",        "label": "Open Privacy Settings"},
            {"type": "delay", "seconds": 1.5,                                 "label": "Wait"},
        ]
    },
    "open_settings_personalization": {
        "tier": "cmd", "description": "Open Personalization settings (wallpaper/themes)",
        "examples": ["open personalization", "change wallpaper settings", "themes settings", "background settings"],
        "params": [],
        "steps": [
            {"type": "cmd",   "command": "start ms-settings:personalization", "label": "Open Personalization"},
            {"type": "delay", "seconds": 1.5,                                  "label": "Wait"},
        ]
    },

    # ── Web Search ────────────────────────────────────────────────────────────
    "google_search": {
        "tier": "cmd", "description": "Search Google in default browser",
        "examples": ["search google for", "google search", "look up on google", "google", "find on google"],
        "params": ["query"],
        "steps": [
            {"type": "cmd",   "command": "start https://www.google.com/search?q={query_encoded}", "label": "Open Google"},
            {"type": "delay", "seconds": 2.0, "label": "Wait for browser"},
        ]
    },
    "youtube_search": {
        "tier": "cmd", "description": "Search YouTube in default browser",
        "examples": ["search youtube for", "find on youtube", "youtube search", "youtube", "watch on youtube"],
        "params": ["query"],
        "steps": [
            {"type": "cmd",   "command": "start https://www.youtube.com/results?search_query={query_encoded}", "label": "Open YouTube"},
            {"type": "delay", "seconds": 2.0, "label": "Wait for browser"},
        ]
    },
    "wikipedia_search": {
        "tier": "cmd", "description": "Search Wikipedia in default browser",
        "examples": ["search wikipedia for", "wikipedia", "look up on wikipedia", "wiki"],
        "params": ["query"],
        "steps": [
            {"type": "cmd",   "command": "start https://en.wikipedia.org/wiki/Special:Search?search={query_encoded}", "label": "Open Wikipedia"},
            {"type": "delay", "seconds": 2.0, "label": "Wait for browser"},
        ]
    },
    "github_search": {
        "tier": "cmd", "description": "Search GitHub repositories",
        "examples": ["search github for", "find on github", "github search"],
        "params": ["query"],
        "steps": [
            {"type": "cmd",   "command": "start https://github.com/search?q={query_encoded}", "label": "Open GitHub"},
            {"type": "delay", "seconds": 2.0, "label": "Wait"},
        ]
    },
    "open_url": {
        "tier": "cmd", "description": "Open a specific website URL",
        "examples": ["open website", "go to url", "navigate to", "open link", "visit website"],
        "params": ["url"],
        "steps": [
            {"type": "cmd",   "command": "start {url}",             "label": "Open URL"},
            {"type": "delay", "seconds": 2.0,                       "label": "Wait"},
        ]
    },
    "open_gmail": {
        "tier": "cmd", "description": "Open Gmail in browser",
        "examples": ["open gmail", "check gmail", "open email gmail"],
        "params": [],
        "steps": [
            {"type": "cmd",   "command": "start https://mail.google.com", "label": "Open Gmail"},
            {"type": "delay", "seconds": 2.0,                              "label": "Wait"},
        ]
    },
    "open_maps": {
        "tier": "cmd", "description": "Open Google Maps",
        "examples": ["open google maps", "open maps", "open map"],
        "params": [],
        "steps": [
            {"type": "cmd",   "command": "start https://maps.google.com", "label": "Open Maps"},
            {"type": "delay", "seconds": 2.0,                              "label": "Wait"},
        ]
    },
    "search_maps": {
        "tier": "cmd", "description": "Search a location on Google Maps",
        "examples": ["find location on maps", "search maps for", "directions to", "map search"],
        "params": ["query"],
        "steps": [
            {"type": "cmd",   "command": "start https://maps.google.com/maps?q={query_encoded}", "label": "Open Maps Search"},
            {"type": "delay", "seconds": 2.0, "label": "Wait"},
        ]
    },
    "open_chatgpt": {
        "tier": "cmd", "description": "Open ChatGPT in browser",
        "examples": ["open chatgpt", "open chat gpt", "go to chatgpt"],
        "params": [],
        "steps": [
            {"type": "cmd",   "command": "start https://chat.openai.com", "label": "Open ChatGPT"},
            {"type": "delay", "seconds": 2.0,                              "label": "Wait"},
        ]
    },

    # ── Notepad & Files ───────────────────────────────────────────────────────
    "notepad_type_text": {
        "tier": "cmd", "description": "Open Notepad and type text",
        "examples": ["open notepad and type", "type in notepad", "write in notepad", "notepad write", "type text in notepad"],
        "params": ["text"],
        "steps": [
            {"type": "cmd",    "command": "start notepad.exe",      "label": "Launch Notepad"},
            {"type": "delay",  "seconds": 2.0,                      "label": "Wait for Notepad"},
            {"type": "type_clip", "text": "{text}",                 "label": "Type text (via clipboard)"},
        ]
    },
    "create_text_file": {
        "tier": "cmd", "description": "Create a text file with content",
        "examples": ["create text file", "make new file", "save text to file", "create file with content"],
        "params": ["filename", "content"],
        "steps": [
            {"type": "write_file", "path": "{filename}", "content": "{content}", "label": "Write file"},
        ]
    },
    "open_file": {
        "tier": "cmd", "description": "Open a specific file",
        "examples": ["open file", "launch file", "open document", "open path"],
        "params": ["filepath"],
        "steps": [
            {"type": "cmd",   "command": "start \"\" \"{filepath}\"", "label": "Open file"},
            {"type": "delay", "seconds": 1.5,                          "label": "Wait"},
        ]
    },
    "open_folder": {
        "tier": "cmd", "description": "Open a folder in File Explorer",
        "examples": ["open folder", "open directory", "show folder", "explore folder"],
        "params": ["folderpath"],
        "steps": [
            {"type": "cmd",   "command": "start explorer \"{folderpath}\"", "label": "Open folder"},
            {"type": "delay", "seconds": 1.0,                                "label": "Wait"},
        ]
    },
    "open_desktop_folder": {
        "tier": "cmd", "description": "Open the Desktop folder",
        "examples": ["open desktop folder", "show desktop files", "explore desktop"],
        "params": [],
        "steps": [
            {"type": "cmd",   "command": "start explorer %USERPROFILE%\\Desktop", "label": "Open Desktop"},
            {"type": "delay", "seconds": 1.0,                                      "label": "Wait"},
        ]
    },
    "open_downloads_folder": {
        "tier": "cmd", "description": "Open the Downloads folder",
        "examples": ["open downloads", "show downloads", "open downloads folder", "go to downloads"],
        "params": [],
        "steps": [
            {"type": "cmd",   "command": "start explorer %USERPROFILE%\\Downloads", "label": "Open Downloads"},
            {"type": "delay", "seconds": 1.0,                                        "label": "Wait"},
        ]
    },
    "open_documents_folder": {
        "tier": "cmd", "description": "Open the Documents folder",
        "examples": ["open documents", "show documents", "open my documents"],
        "params": [],
        "steps": [
            {"type": "cmd",   "command": "start explorer %USERPROFILE%\\Documents", "label": "Open Documents"},
            {"type": "delay", "seconds": 1.0,                                        "label": "Wait"},
        ]
    },
    "list_directory": {
        "tier": "cmd", "description": "List files in a directory",
        "examples": ["list files in", "show files in", "what is in folder", "ls directory"],
        "params": ["folderpath"],
        "steps": [
            {"type": "cmd",   "command": "dir \"{folderpath}\"",
             "label": "List directory", "capture_output": True},
        ]
    },

    # ── System Info & Control ─────────────────────────────────────────────────
    "check_ip_address": {
        "tier": "cmd", "description": "Check IP address and network info",
        "examples": ["check ip address", "what is my ip", "show ip", "ipconfig", "network info"],
        "params": [],
        "steps": [
            {"type": "cmd",   "command": "ipconfig",
             "label": "Run ipconfig", "capture_output": True},
        ]
    },
    "check_battery": {
        "tier": "cmd", "description": "Check battery level",
        "examples": ["check battery", "battery status", "battery level", "how much battery"],
        "params": [],
        "steps": [
            {"type": "cmd",   "command": "powershell -command \"Get-WmiObject Win32_Battery | Select-Object EstimatedChargeRemaining,BatteryStatus | Format-List\"",
             "label": "Battery status", "capture_output": True},
        ]
    },
    "check_disk_space": {
        "tier": "cmd", "description": "Check disk space on all drives",
        "examples": ["check disk space", "storage info", "how much storage", "disk usage", "free space"],
        "params": [],
        "steps": [
            {"type": "cmd",   "command": "wmic logicaldisk get caption,freespace,size /format:list",
             "label": "Check disk space", "capture_output": True},
        ]
    },
    "check_system_info": {
        "tier": "cmd", "description": "Show system specs and info",
        "examples": ["system info", "computer specs", "what are my specs", "show system info"],
        "params": [],
        "steps": [
            {"type": "cmd",   "command": "systeminfo | findstr /C:\"OS\" /C:\"RAM\" /C:\"Processor\" /C:\"Total Physical Memory\"",
             "label": "System info", "capture_output": True},
        ]
    },
    "check_cpu_ram": {
        "tier": "cmd", "description": "Check current CPU and RAM usage",
        "examples": ["cpu usage", "ram usage", "memory usage", "check cpu", "performance stats"],
        "params": [],
        "steps": [
            {"type": "cmd",   "command": "powershell -command \"Get-WmiObject Win32_Processor | Select-Object LoadPercentage; Get-WmiObject Win32_OperatingSystem | Select-Object @{N='RAM_Used_GB';E={[math]::round(($_.TotalVisibleMemorySize - $_.FreePhysicalMemory)/1MB,2)}},@{N='RAM_Total_GB';E={[math]::round($_.TotalVisibleMemorySize/1MB,2)}} | Format-List\"",
             "label": "CPU+RAM usage", "capture_output": True},
        ]
    },
    "check_windows_version": {
        "tier": "cmd", "description": "Show Windows version",
        "examples": ["check windows version", "what version of windows", "windows version", "winver"],
        "params": [],
        "steps": [
            {"type": "cmd",   "command": "winver",                  "label": "Show Windows version"},
            {"type": "delay", "seconds": 1.0,                       "label": "Wait"},
        ]
    },
    "ping_host": {
        "tier": "cmd", "description": "Ping a host to check connectivity",
        "examples": ["ping google", "ping host", "check connection to", "test network ping"],
        "params": ["host"],
        "steps": [
            {"type": "cmd",   "command": "ping -n 4 {host}",
             "label": "Ping {host}", "capture_output": True},
        ]
    },
    "flush_dns": {
        "tier": "cmd", "description": "Flush DNS resolver cache",
        "examples": ["flush dns", "clear dns cache", "reset dns"],
        "params": [],
        "steps": [
            {"type": "cmd",   "command": "ipconfig /flushdns",
             "label": "Flush DNS", "capture_output": True},
        ]
    },
    "list_processes": {
        "tier": "cmd", "description": "List all running processes",
        "examples": ["list processes", "running processes", "show running apps", "tasklist", "what is running"],
        "params": [],
        "steps": [
            {"type": "cmd",   "command": "tasklist /fo table /nh",
             "label": "List processes", "capture_output": True},
        ]
    },
    "kill_process": {
        "tier": "cmd", "description": "Force close / kill a process by name",
        "examples": ["kill process", "close process", "force close", "kill app", "terminate app"],
        "params": ["process_name"],
        "steps": [
            {"type": "cmd",   "command": "taskkill /F /IM {process_name}",
             "label": "Kill {process_name}", "capture_output": True},
        ]
    },
    "empty_recycle_bin": {
        "tier": "cmd", "description": "Empty the Recycle Bin",
        "examples": ["empty recycle bin", "clear recycle bin", "delete recycle bin"],
        "params": [],
        "steps": [
            {"type": "cmd",   "command": "powershell -command \"Clear-RecycleBin -Force -ErrorAction SilentlyContinue\"",
             "label": "Empty Recycle Bin", "capture_output": True},
        ]
    },
    "lock_screen": {
        "tier": "cmd", "description": "Lock the Windows screen",
        "examples": ["lock screen", "lock computer", "lock pc", "lock workstation"],
        "params": [],
        "steps": [
            {"type": "cmd",   "command": "rundll32.exe user32.dll,LockWorkStation", "label": "Lock screen"},
        ]
    },
    "shutdown": {
        "tier": "cmd", "description": "Shutdown the computer",
        "examples": ["shutdown computer", "turn off computer", "shutdown pc", "power off"],
        "params": [],
        "steps": [
            {"type": "cmd",   "command": "shutdown /s /t 10",       "label": "Schedule shutdown in 10s"},
        ]
    },
    "restart": {
        "tier": "cmd", "description": "Restart the computer",
        "examples": ["restart computer", "reboot", "restart pc", "reboot computer"],
        "params": [],
        "steps": [
            {"type": "cmd",   "command": "shutdown /r /t 10",       "label": "Schedule restart in 10s"},
        ]
    },
    "cancel_shutdown": {
        "tier": "cmd", "description": "Cancel a pending shutdown or restart",
        "examples": ["cancel shutdown", "abort shutdown", "stop shutdown", "cancel restart"],
        "params": [],
        "steps": [
            {"type": "cmd",   "command": "shutdown /a",
             "label": "Cancel shutdown", "capture_output": True},
        ]
    },
    "take_screenshot": {
        "tier": "cmd", "description": "Take a screenshot and save to Desktop",
        "examples": ["take screenshot", "capture screen", "screenshot", "save screen"],
        "params": [],
        "steps": [
            {"type": "screenshot", "path": "~/Desktop/screenshot_{timestamp}.png", "label": "Capture screen"},
        ]
    },
    "run_custom_command": {
        "tier": "cmd", "description": "Run a custom shell command",
        "examples": ["run command", "execute command", "shell command", "cmd command"],
        "params": ["command"],
        "steps": [
            {"type": "cmd",   "command": "{command}",
             "label": "Run: {command}", "capture_output": True},
        ]
    },
}


# ══════════════════════════════════════════════════════════════════════════════
#  TIER 2 — KEYBOARD (pyautogui hotkeys only, NO mouse coordinates)
# ══════════════════════════════════════════════════════════════════════════════

KEYBOARD_PLAYBOOKS: dict = {

    # ── System & Window Control ───────────────────────────────────────────────
    "show_desktop": {
        "tier": "keyboard", "description": "Minimize all windows and show desktop",
        "examples": ["show desktop", "minimize all windows", "go to desktop", "hide all windows"],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["win", "d"], "label": "Show Desktop (Win+D)"},
        ]
    },
    "maximize_window": {
        "tier": "keyboard", "description": "Maximize the current active window",
        "examples": ["maximize window", "make window full screen", "maximize current window"],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["win", "up"], "label": "Maximize (Win+Up)"},
        ]
    },
    "minimize_window": {
        "tier": "keyboard", "description": "Minimize the current active window",
        "examples": ["minimize window", "minimize current window", "hide window"],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["win", "down"], "label": "Minimize (Win+Down)"},
        ]
    },
    "snap_window_left": {
        "tier": "keyboard", "description": "Snap current window to left half of screen",
        "examples": ["snap window left", "move window to left", "split screen left", "tile left"],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["win", "left"], "label": "Snap Left (Win+Left)"},
        ]
    },
    "snap_window_right": {
        "tier": "keyboard", "description": "Snap current window to right half of screen",
        "examples": ["snap window right", "move window to right", "split screen right", "tile right"],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["win", "right"], "label": "Snap Right (Win+Right)"},
        ]
    },
    "close_window": {
        "tier": "keyboard", "description": "Close the current active window",
        "examples": ["close window", "close current window", "close app", "close this", "exit window"],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["alt", "f4"], "label": "Close Window (Alt+F4)"},
        ]
    },
    "switch_windows": {
        "tier": "keyboard", "description": "Open Alt+Tab window switcher",
        "examples": ["switch windows", "alt tab", "switch app", "switch between windows", "change window"],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["alt", "tab"], "label": "Alt+Tab — switch windows"},
        ]
    },
    "task_view": {
        "tier": "keyboard", "description": "Open Task View (all open windows overview)",
        "examples": ["task view", "open task view", "show all windows", "windows overview", "win tab"],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["win", "tab"], "label": "Task View (Win+Tab)"},
        ]
    },
    "open_run_dialog": {
        "tier": "keyboard", "description": "Open the Windows Run dialog",
        "examples": ["open run dialog", "win r", "open run", "run command dialog"],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["win", "r"],  "label": "Open Run Dialog (Win+R)"},
        ]
    },
    "run_app_via_run": {
        "tier": "keyboard", "description": "Open Run dialog and launch any app or command",
        "examples": ["run app via run dialog", "win r then type", "open app with run command"],
        "params": ["command"],
        "steps": [
            {"type": "hotkey",    "keys": ["win", "r"],  "label": "Open Run Dialog"},
            {"type": "delay",     "seconds": 0.8,         "label": "Wait for dialog"},
            {"type": "type_clip", "text": "{command}",    "label": "Type command"},
            {"type": "press",     "key": "enter",         "label": "Press Enter"},
        ]
    },
    "new_virtual_desktop": {
        "tier": "keyboard", "description": "Create a new virtual desktop",
        "examples": ["new virtual desktop", "create virtual desktop", "add desktop"],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["win", "ctrl", "d"], "label": "New Virtual Desktop"},
        ]
    },
    "next_virtual_desktop": {
        "tier": "keyboard", "description": "Switch to next virtual desktop",
        "examples": ["next desktop", "switch to next desktop", "go to next virtual desktop"],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["win", "ctrl", "right"], "label": "Next Virtual Desktop"},
        ]
    },
    "prev_virtual_desktop": {
        "tier": "keyboard", "description": "Switch to previous virtual desktop",
        "examples": ["previous desktop", "go back desktop", "switch previous virtual desktop"],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["win", "ctrl", "left"], "label": "Previous Virtual Desktop"},
        ]
    },
    "open_action_center": {
        "tier": "keyboard", "description": "Open Windows Action Center (Quick Settings)",
        "examples": ["open action center", "open quick settings", "notification panel", "action center"],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["win", "a"], "label": "Action Center (Win+A)"},
        ]
    },
    "open_notification_center": {
        "tier": "keyboard", "description": "Open Notification Center",
        "examples": ["open notifications", "notification center", "show notifications"],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["win", "n"], "label": "Notification Center (Win+N)"},
        ]
    },
    "open_emoji_picker": {
        "tier": "keyboard", "description": "Open the emoji picker",
        "examples": ["open emoji picker", "insert emoji", "emoji keyboard", "open emojis"],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["win", "."], "label": "Emoji Picker (Win+.)"},
        ]
    },
    "open_clipboard_history": {
        "tier": "keyboard", "description": "Open clipboard history",
        "examples": ["open clipboard history", "show clipboard", "clipboard history", "paste history"],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["win", "v"], "label": "Clipboard History (Win+V)"},
        ]
    },
    "open_windows_search": {
        "tier": "keyboard", "description": "Open Windows Search bar",
        "examples": ["open search", "open windows search", "windows search bar", "open start search"],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["win", "s"], "label": "Windows Search (Win+S)"},
        ]
    },
    "screen_zoom_in": {
        "tier": "keyboard", "description": "Zoom in the screen using Magnifier",
        "examples": ["zoom in screen", "magnify screen", "zoom in", "increase zoom"],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["win", "="],    "label": "Zoom In (Win+=)"},
        ]
    },
    "screen_zoom_out": {
        "tier": "keyboard", "description": "Zoom out the screen",
        "examples": ["zoom out screen", "zoom out", "decrease zoom", "reduce magnification"],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["win", "-"],    "label": "Zoom Out (Win+-)"},
        ]
    },

    # ── Volume Control ────────────────────────────────────────────────────────
    "mute_volume": {
        "tier": "keyboard", "description": "Mute/unmute system volume",
        "examples": ["mute volume", "mute audio", "mute sound", "silence", "unmute"],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["volumemute"], "label": "Mute (VolumeMute key)"},
        ]
    },
    "volume_up": {
        "tier": "keyboard", "description": "Increase system volume",
        "examples": ["volume up", "increase volume", "louder", "turn up volume"],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["volumeup"], "label": "Vol Up"},
            {"type": "hotkey", "keys": ["volumeup"], "label": "Vol Up"},
            {"type": "hotkey", "keys": ["volumeup"], "label": "Vol Up"},
            {"type": "hotkey", "keys": ["volumeup"], "label": "Vol Up"},
            {"type": "hotkey", "keys": ["volumeup"], "label": "Vol Up"},
        ]
    },
    "volume_down": {
        "tier": "keyboard", "description": "Decrease system volume",
        "examples": ["volume down", "decrease volume", "quieter", "turn down volume", "lower volume"],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["volumedown"], "label": "Vol Down"},
            {"type": "hotkey", "keys": ["volumedown"], "label": "Vol Down"},
            {"type": "hotkey", "keys": ["volumedown"], "label": "Vol Down"},
            {"type": "hotkey", "keys": ["volumedown"], "label": "Vol Down"},
            {"type": "hotkey", "keys": ["volumedown"], "label": "Vol Down"},
        ]
    },

    # ── Text Editing Shortcuts ────────────────────────────────────────────────
    "select_all": {
        "tier": "keyboard", "description": "Select all text or items (Ctrl+A)",
        "examples": ["select all", "select all text", "ctrl a", "select everything"],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["ctrl", "a"], "label": "Select All (Ctrl+A)"},
        ]
    },
    "copy": {
        "tier": "keyboard", "description": "Copy selected content to clipboard",
        "examples": ["copy", "copy selection", "ctrl c", "copy selected text", "copy to clipboard"],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["ctrl", "c"], "label": "Copy (Ctrl+C)"},
        ]
    },
    "paste": {
        "tier": "keyboard", "description": "Paste from clipboard",
        "examples": ["paste", "ctrl v", "paste clipboard", "paste here", "paste text"],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["ctrl", "v"], "label": "Paste (Ctrl+V)"},
        ]
    },
    "cut": {
        "tier": "keyboard", "description": "Cut selected content",
        "examples": ["cut", "ctrl x", "cut selection", "cut text"],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["ctrl", "x"], "label": "Cut (Ctrl+X)"},
        ]
    },
    "undo": {
        "tier": "keyboard", "description": "Undo the last action",
        "examples": ["undo", "undo last action", "ctrl z", "go back", "revert"],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["ctrl", "z"], "label": "Undo (Ctrl+Z)"},
        ]
    },
    "redo": {
        "tier": "keyboard", "description": "Redo the last undone action",
        "examples": ["redo", "redo last action", "ctrl y", "redo change"],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["ctrl", "y"], "label": "Redo (Ctrl+Y)"},
        ]
    },
    "save_file": {
        "tier": "keyboard", "description": "Save the current file (Ctrl+S)",
        "examples": ["save file", "ctrl s", "save document", "save current file", "save"],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["ctrl", "s"], "label": "Save (Ctrl+S)"},
        ]
    },
    "save_file_as": {
        "tier": "keyboard", "description": "Save file as new name (Ctrl+Shift+S)",
        "examples": ["save as", "save file as", "ctrl shift s", "save copy as"],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["ctrl", "shift", "s"], "label": "Save As (Ctrl+Shift+S)"},
        ]
    },
    "find_in_document": {
        "tier": "keyboard", "description": "Open Find dialog in current app",
        "examples": ["find in document", "find text", "search in document", "ctrl f", "find word"],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["ctrl", "f"], "label": "Find (Ctrl+F)"},
        ]
    },
    "find_and_replace": {
        "tier": "keyboard", "description": "Open Find & Replace dialog",
        "examples": ["find and replace", "replace text", "ctrl h", "find replace"],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["ctrl", "h"], "label": "Find & Replace (Ctrl+H)"},
        ]
    },
    "new_file": {
        "tier": "keyboard", "description": "Create a new file/document in current app",
        "examples": ["new file", "new document", "ctrl n", "create new", "open new"],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["ctrl", "n"], "label": "New (Ctrl+N)"},
        ]
    },
    "open_file_dialog": {
        "tier": "keyboard", "description": "Open the Open File dialog",
        "examples": ["open file dialog", "ctrl o", "open document dialog"],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["ctrl", "o"], "label": "Open File Dialog (Ctrl+O)"},
        ]
    },
    "print_document": {
        "tier": "keyboard", "description": "Print the current document",
        "examples": ["print document", "ctrl p", "print", "print file", "send to printer"],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["ctrl", "p"], "label": "Print (Ctrl+P)"},
        ]
    },
    "bold_text": {
        "tier": "keyboard", "description": "Toggle bold formatting on selected text",
        "examples": ["bold text", "make text bold", "ctrl b", "bold selected"],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["ctrl", "b"], "label": "Bold (Ctrl+B)"},
        ]
    },
    "italic_text": {
        "tier": "keyboard", "description": "Toggle italic formatting on selected text",
        "examples": ["italic text", "make text italic", "ctrl i", "italicize"],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["ctrl", "i"], "label": "Italic (Ctrl+I)"},
        ]
    },
    "underline_text": {
        "tier": "keyboard", "description": "Toggle underline on selected text",
        "examples": ["underline text", "ctrl u", "underline selected"],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["ctrl", "u"], "label": "Underline (Ctrl+U)"},
        ]
    },

    # ── Browser Shortcuts ─────────────────────────────────────────────────────
    "browser_new_tab": {
        "tier": "keyboard", "description": "Open a new browser tab",
        "examples": ["new tab", "open new tab", "ctrl t", "new browser tab"],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["ctrl", "t"], "label": "New Tab (Ctrl+T)"},
        ]
    },
    "browser_close_tab": {
        "tier": "keyboard", "description": "Close the current browser tab",
        "examples": ["close tab", "close browser tab", "ctrl w", "close current tab"],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["ctrl", "w"], "label": "Close Tab (Ctrl+W)"},
        ]
    },
    "browser_reopen_tab": {
        "tier": "keyboard", "description": "Reopen the last closed browser tab",
        "examples": ["reopen tab", "restore closed tab", "ctrl shift t", "undo close tab"],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["ctrl", "shift", "t"], "label": "Reopen Tab (Ctrl+Shift+T)"},
        ]
    },
    "browser_refresh": {
        "tier": "keyboard", "description": "Refresh the current browser page",
        "examples": ["refresh page", "reload page", "f5", "browser refresh", "refresh website"],
        "params": [],
        "steps": [
            {"type": "press", "key": "f5",                           "label": "Refresh (F5)"},
        ]
    },
    "browser_hard_refresh": {
        "tier": "keyboard", "description": "Hard refresh (clear cache) the browser page",
        "examples": ["hard refresh", "force refresh", "ctrl f5", "clear cache refresh"],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["ctrl", "f5"], "label": "Hard Refresh (Ctrl+F5)"},
        ]
    },
    "browser_address_bar": {
        "tier": "keyboard", "description": "Focus the browser address bar",
        "examples": ["go to address bar", "focus address bar", "ctrl l", "browser url bar"],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["ctrl", "l"], "label": "Address Bar (Ctrl+L)"},
        ]
    },
    "browser_navigate_to": {
        "tier": "keyboard", "description": "Navigate browser to a URL by focusing address bar",
        "examples": ["navigate browser to", "type url in browser", "go to url in browser", "open url in current browser"],
        "params": ["url"],
        "steps": [
            {"type": "hotkey",    "keys": ["ctrl", "l"],  "label": "Focus address bar"},
            {"type": "delay",     "seconds": 0.4,          "label": "Wait"},
            {"type": "type_clip", "text": "{url}",         "label": "Type URL"},
            {"type": "press",     "key": "enter",          "label": "Navigate"},
        ]
    },
    "browser_zoom_in": {
        "tier": "keyboard", "description": "Zoom in on browser page",
        "examples": ["zoom in browser", "make text bigger", "browser zoom in", "ctrl plus"],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["ctrl", "="], "label": "Zoom In (Ctrl++)"},
            {"type": "hotkey", "keys": ["ctrl", "="], "label": "Zoom In"},
        ]
    },
    "browser_zoom_out": {
        "tier": "keyboard", "description": "Zoom out on browser page",
        "examples": ["zoom out browser", "make text smaller", "browser zoom out", "ctrl minus"],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["ctrl", "-"], "label": "Zoom Out (Ctrl+-)"},
            {"type": "hotkey", "keys": ["ctrl", "-"], "label": "Zoom Out"},
        ]
    },
    "browser_zoom_reset": {
        "tier": "keyboard", "description": "Reset browser zoom to 100%",
        "examples": ["reset zoom", "reset browser zoom", "100 percent zoom", "ctrl 0"],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["ctrl", "0"], "label": "Reset Zoom (Ctrl+0)"},
        ]
    },
    "browser_incognito": {
        "tier": "keyboard", "description": "Open incognito/private browser window",
        "examples": ["open incognito", "private window", "private browsing", "incognito mode"],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["ctrl", "shift", "n"], "label": "Incognito (Ctrl+Shift+N)"},
        ]
    },
    "browser_dev_tools": {
        "tier": "keyboard", "description": "Open browser Developer Tools",
        "examples": ["open dev tools", "developer tools", "f12", "inspect element", "open console"],
        "params": [],
        "steps": [
            {"type": "press", "key": "f12", "label": "Dev Tools (F12)"},
        ]
    },
    "browser_back": {
        "tier": "keyboard", "description": "Go back in browser history",
        "examples": ["go back", "browser back", "previous page", "navigate back"],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["alt", "left"], "label": "Back (Alt+Left)"},
        ]
    },
    "browser_forward": {
        "tier": "keyboard", "description": "Go forward in browser history",
        "examples": ["go forward", "browser forward", "next page", "navigate forward"],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["alt", "right"], "label": "Forward (Alt+Right)"},
        ]
    },

    # ── File Manager Shortcuts ────────────────────────────────────────────────
    "explorer_new_folder": {
        "tier": "keyboard", "description": "Create a new folder in File Explorer",
        "examples": ["new folder", "create folder", "make new folder", "ctrl shift n in explorer"],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["ctrl", "shift", "n"], "label": "New Folder (Ctrl+Shift+N)"},
        ]
    },
    "explorer_delete": {
        "tier": "keyboard", "description": "Delete selected file/folder (send to Recycle Bin)",
        "examples": ["delete selected file", "delete file", "move to recycle bin", "delete item"],
        "params": [],
        "steps": [
            {"type": "press", "key": "delete", "label": "Delete (Del key)"},
        ]
    },
    "explorer_rename": {
        "tier": "keyboard", "description": "Rename the selected file or folder",
        "examples": ["rename file", "rename folder", "rename selected", "f2 rename"],
        "params": [],
        "steps": [
            {"type": "press", "key": "f2", "label": "Rename (F2)"},
        ]
    },
    "explorer_properties": {
        "tier": "keyboard", "description": "Open properties of selected file/folder",
        "examples": ["file properties", "show properties", "alt enter properties"],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["alt", "enter"], "label": "Properties (Alt+Enter)"},
        ]
    },
    "explorer_search": {
        "tier": "keyboard", "description": "Focus search bar in File Explorer",
        "examples": ["search in explorer", "explorer search", "find file in explorer"],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["ctrl", "f"], "label": "Explorer Search (Ctrl+F)"},
        ]
    },
    "screenshot_snip": {
        "tier": "keyboard", "description": "Take screenshot using Snip & Sketch shortcut",
        "examples": ["snip screenshot", "win shift s screenshot", "region screenshot", "snip and sketch"],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["win", "shift", "s"], "label": "Snip & Sketch (Win+Shift+S)"},
        ]
    },
}

# ── Merged view (all playbooks, searchable by ID) ─────────────────────────────
ALL_PLAYBOOKS: dict = {**CMD_PLAYBOOKS, **KEYBOARD_PLAYBOOKS}
ALL_TASK_IDS   = list(ALL_PLAYBOOKS.keys())


def build_routing_summary() -> str:
    """Build a compact routing summary for the LLM classifier prompt."""
    lines: list[str] = []
    for task_id, pb in ALL_PLAYBOOKS.items():
        tier = pb.get("tier", "cmd").upper()
        exs  = " | ".join(pb["examples"][:3])
        lines.append(f'  [{tier}] "{task_id}" — {pb["description"]}')
        lines.append(f'         e.g. "{exs}"')
    return "\n".join(lines)
