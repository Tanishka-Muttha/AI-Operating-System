"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  TIER 3 GUI PLAYBOOKS v2 — 100 Everyday Tasks                               ║
║                                                                              ║
║  Key principles:                                                             ║
║  1. Win+S (Windows Search) as universal launcher — never click desktop icons ║
║  2. Clipboard paste (type_clip) for ALL typing — Unicode-safe, 100% accurate ║
║  3. Keyboard navigation over mouse wherever possible                         ║
║  4. verify steps confirm GUI state before continuing                         ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

GUI_PLAYBOOKS: dict = {

    # ══════════════════════════════════════════════════════════════════════
    #  SECTION 1 — APP LAUNCHER (Win+S based)
    # ══════════════════════════════════════════════════════════════════════

    "open_any_app_search": {
        "tier": "gui",
        "description": "Open any application by name using Windows Search",
        "examples": [
            "open spotify", "launch vlc", "open discord", "start steam",
            "open whatsapp", "launch telegram", "open zoom", "start obs",
            "open slack", "launch skype"
        ],
        "params": ["app_name"],
        "steps": [
            {"type": "win_search", "query": "{app_name}",  "label": "Search for {app_name}"},
            {"type": "delay",      "seconds": 1.5,          "label": "Wait for results"},
            {"type": "press",      "key": "enter",           "label": "Open top result"},
            {"type": "delay",      "seconds": 2.0,           "label": "Wait for app"},
        ]
    },

    "open_app_fullscreen": {
        "tier": "gui",
        "description": "Open any app via Windows Search and maximize it",
        "examples": [
            "open chrome fullscreen", "launch notepad maximized",
            "open discord full screen", "start zoom maximized"
        ],
        "params": ["app_name"],
        "steps": [
            {"type": "win_search", "query": "{app_name}",    "label": "Search for {app_name}"},
            {"type": "delay",      "seconds": 1.5,            "label": "Wait"},
            {"type": "press",      "key": "enter",             "label": "Open app"},
            {"type": "delay",      "seconds": 2.5,             "label": "Wait for app"},
            {"type": "hotkey",     "keys": ["win", "up"],      "label": "Maximize (Win+Up)"},
        ]
    },

    "open_app_snap_left": {
        "tier": "gui",
        "description": "Open an app and snap it to the left half of screen",
        "examples": [
            "open notepad on left side", "snap chrome to left",
            "open word snapped left"
        ],
        "params": ["app_name"],
        "steps": [
            {"type": "win_search", "query": "{app_name}",      "label": "Search for {app_name}"},
            {"type": "delay",      "seconds": 1.5,              "label": "Wait"},
            {"type": "press",      "key": "enter",               "label": "Open app"},
            {"type": "delay",      "seconds": 2.0,               "label": "Wait"},
            {"type": "hotkey",     "keys": ["win", "left"],      "label": "Snap Left (Win+Left)"},
        ]
    },

    "open_app_snap_right": {
        "tier": "gui",
        "description": "Open an app and snap it to the right half of screen",
        "examples": [
            "open chrome on right side", "snap edge to right",
            "open word on the right"
        ],
        "params": ["app_name"],
        "steps": [
            {"type": "win_search", "query": "{app_name}",       "label": "Search for {app_name}"},
            {"type": "delay",      "seconds": 1.5,               "label": "Wait"},
            {"type": "press",      "key": "enter",                "label": "Open app"},
            {"type": "delay",      "seconds": 2.0,                "label": "Wait"},
            {"type": "hotkey",     "keys": ["win", "right"],      "label": "Snap Right (Win+Right)"},
        ]
    },

    # ══════════════════════════════════════════════════════════════════════
    #  SECTION 2 — BROWSER WORKFLOWS
    # ══════════════════════════════════════════════════════════════════════

    "browser_search_and_navigate": {
        "tier": "gui",
        "description": "Open a specific browser and navigate to a URL",
        "examples": [
            "open chrome and go to youtube",
            "open edge and navigate to google.com",
            "launch firefox and visit reddit"
        ],
        "params": ["browser", "url"],
        "steps": [
            {"type": "win_search", "query": "{browser}",        "label": "Search for {browser}"},
            {"type": "delay",      "seconds": 1.5,               "label": "Wait"},
            {"type": "press",      "key": "enter",                "label": "Open browser"},
            {"type": "delay",      "seconds": 3.0,                "label": "Wait for browser"},
            {"type": "hotkey",     "keys": ["ctrl", "l"],         "label": "Focus address bar"},
            {"type": "delay",      "seconds": 0.5,                "label": "Wait"},
            {"type": "type_clip",  "text": "{url}",               "label": "Type URL"},
            {"type": "press",      "key": "enter",                 "label": "Navigate"},
            {"type": "delay",      "seconds": 2.0,                 "label": "Wait for page"},
        ]
    },

    "browser_search_in_current": {
        "tier": "gui",
        "description": "In the currently open browser, search for a query",
        "examples": [
            "search in current browser for python tutorial",
            "google something in open browser",
            "look up in the browser that is open"
        ],
        "params": ["query"],
        "steps": [
            {"type": "hotkey",    "keys": ["ctrl", "l"],           "label": "Focus address bar"},
            {"type": "delay",     "seconds": 0.4,                   "label": "Wait"},
            {"type": "type_clip", "text": "https://www.google.com/search?q={query_encoded}", "label": "Type search URL"},
            {"type": "press",     "key": "enter",                    "label": "Navigate"},
            {"type": "delay",     "seconds": 2.0,                    "label": "Wait for results"},
        ]
    },

    "browser_new_tab_and_search": {
        "tier": "gui",
        "description": "Open a new browser tab and search for something",
        "examples": [
            "new tab and search for python",
            "open new tab and look up weather",
            "new tab google search for news"
        ],
        "params": ["query"],
        "steps": [
            {"type": "hotkey",    "keys": ["ctrl", "t"],            "label": "New Tab"},
            {"type": "delay",     "seconds": 0.5,                    "label": "Wait"},
            {"type": "type_clip", "text": "https://www.google.com/search?q={query_encoded}", "label": "Type search URL"},
            {"type": "press",     "key": "enter",                     "label": "Search"},
            {"type": "delay",     "seconds": 2.0,                     "label": "Wait for results"},
        ]
    },

    "browser_open_youtube_search": {
        "tier": "gui",
        "description": "Open new browser tab and search YouTube for a video",
        "examples": [
            "new tab youtube search lofi music",
            "open youtube and find python tutorial",
            "search youtube for cooking recipes in browser"
        ],
        "params": ["query"],
        "steps": [
            {"type": "hotkey",    "keys": ["ctrl", "t"],            "label": "New Tab"},
            {"type": "delay",     "seconds": 0.5,                    "label": "Wait"},
            {"type": "type_clip", "text": "https://www.youtube.com/results?search_query={query_encoded}", "label": "Type YouTube URL"},
            {"type": "press",     "key": "enter",                    "label": "Search YouTube"},
            {"type": "delay",     "seconds": 2.0,                    "label": "Wait for results"},
        ]
    },

    "browser_open_incognito": {
        "tier": "gui",
        "description": "Open a new incognito/private browser window",
        "examples": [
            "open incognito window",
            "private browser window",
            "open chrome incognito", "open private browsing"
        ],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["ctrl", "shift", "n"], "label": "Open Incognito Window"},
            {"type": "delay",  "seconds": 1.5,                  "label": "Wait for window"},
        ]
    },

    "browser_bookmark_current": {
        "tier": "gui",
        "description": "Bookmark the current browser page",
        "examples": [
            "bookmark this page", "add to bookmarks",
            "save this website", "bookmark current tab"
        ],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["ctrl", "d"],           "label": "Bookmark (Ctrl+D)"},
            {"type": "delay",  "seconds": 0.5,                   "label": "Wait for dialog"},
            {"type": "press",  "key": "enter",                    "label": "Confirm bookmark"},
        ]
    },

    "browser_print_page": {
        "tier": "gui",
        "description": "Print or save the current browser page as PDF",
        "examples": [
            "print this page", "save page as pdf",
            "print current tab", "print to pdf"
        ],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["ctrl", "p"],           "label": "Open Print dialog"},
            {"type": "delay",  "seconds": 1.5,                   "label": "Wait for print dialog"},
        ]
    },

    "browser_find_on_page": {
        "tier": "gui",
        "description": "Find and highlight a word on the current browser page",
        "examples": [
            "find word on page",
            "search for text in webpage",
            "ctrl f find in browser",
            "find on page in browser"
        ],
        "params": ["query"],
        "steps": [
            {"type": "hotkey",    "keys": ["ctrl", "f"],          "label": "Open Find bar"},
            {"type": "delay",     "seconds": 0.4,                  "label": "Wait"},
            {"type": "type_clip", "text": "{query}",               "label": "Type search term"},
            {"type": "press",     "key": "enter",                   "label": "Find next"},
        ]
    },

    "browser_open_history": {
        "tier": "gui",
        "description": "Open browser history page",
        "examples": [
            "open browser history", "view history",
            "show browsing history", "open history tab"
        ],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["ctrl", "h"],           "label": "Open History (Ctrl+H)"},
            {"type": "delay",  "seconds": 1.0,                   "label": "Wait"},
        ]
    },

    "browser_open_downloads": {
        "tier": "gui",
        "description": "Open browser downloads page",
        "examples": [
            "open downloads", "show browser downloads",
            "view my downloads", "open download page"
        ],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["ctrl", "j"],           "label": "Open Downloads (Ctrl+J)"},
            {"type": "delay",  "seconds": 1.0,                   "label": "Wait"},
        ]
    },

    "browser_duplicate_tab": {
        "tier": "gui",
        "description": "Duplicate the current browser tab",
        "examples": [
            "duplicate this tab", "open same page in new tab",
            "clone current tab"
        ],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["ctrl", "l"],           "label": "Focus address bar"},
            {"type": "delay",  "seconds": 0.3,                   "label": "Wait"},
            {"type": "hotkey", "keys": ["alt", "enter"],         "label": "Open in new tab"},
            {"type": "delay",  "seconds": 1.0,                   "label": "Wait"},
        ]
    },

    "browser_go_to_address": {
        "tier": "gui",
        "description": "Navigate current browser to a specific URL by typing in address bar",
        "examples": [
            "navigate browser to github.com",
            "go to website in current browser",
            "type url in current browser"
        ],
        "params": ["url"],
        "steps": [
            {"type": "hotkey",    "keys": ["ctrl", "l"],         "label": "Focus address bar"},
            {"type": "delay",     "seconds": 0.4,                 "label": "Wait"},
            {"type": "type_clip", "text": "{url}",                "label": "Type URL"},
            {"type": "press",     "key": "enter",                  "label": "Navigate"},
            {"type": "delay",     "seconds": 2.0,                  "label": "Wait for page"},
        ]
    },

    "browser_scroll_to_top": {
        "tier": "gui",
        "description": "Scroll the browser page back to the top",
        "examples": [
            "scroll to top of page", "go to top of page",
            "scroll back to beginning"
        ],
        "params": [],
        "steps": [
            {"type": "press",  "key": "ctrl",                    "label": "Hold Ctrl"},
            {"type": "hotkey", "keys": ["ctrl", "home"],          "label": "Scroll to top (Ctrl+Home)"},
        ]
    },

    "browser_scroll_to_bottom": {
        "tier": "gui",
        "description": "Scroll the browser page all the way to the bottom",
        "examples": [
            "scroll to bottom of page", "go to end of page",
            "scroll down to bottom"
        ],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["ctrl", "end"],           "label": "Scroll to bottom (Ctrl+End)"},
        ]
    },

    "browser_reader_mode": {
        "tier": "gui",
        "description": "Toggle Reader/Reading mode in Edge browser (F9)",
        "examples": [
            "enable reader mode", "reading view",
            "turn on reading mode", "distraction free mode"
        ],
        "params": [],
        "steps": [
            {"type": "press",  "key": "f9",                      "label": "Toggle Reader Mode (F9)"},
            {"type": "delay",  "seconds": 0.5,                    "label": "Wait"},
        ]
    },

    "browser_zoom_in_then_navigate": {
        "tier": "gui",
        "description": "Zoom into a page then search for content",
        "examples": [
            "zoom in and search page",
            "increase zoom and find text"
        ],
        "params": ["query"],
        "steps": [
            {"type": "hotkey",    "keys": ["ctrl", "="],          "label": "Zoom In"},
            {"type": "hotkey",    "keys": ["ctrl", "="],          "label": "Zoom In again"},
            {"type": "hotkey",    "keys": ["ctrl", "f"],          "label": "Open Find"},
            {"type": "delay",     "seconds": 0.4,                  "label": "Wait"},
            {"type": "type_clip", "text": "{query}",               "label": "Search text"},
        ]
    },

    # ══════════════════════════════════════════════════════════════════════
    #  SECTION 3 — NOTEPAD & TEXT
    # ══════════════════════════════════════════════════════════════════════

    "notepad_full_workflow": {
        "tier": "gui",
        "description": "Open Notepad, type content, and save with a filename",
        "examples": [
            "open notepad type and save",
            "write in notepad and save file",
            "notepad type text and save"
        ],
        "params": ["text", "filename"],
        "steps": [
            {"type": "win_search", "query": "Notepad",              "label": "Search Notepad"},
            {"type": "delay",      "seconds": 1.5,                   "label": "Wait"},
            {"type": "press",      "key": "enter",                    "label": "Open Notepad"},
            {"type": "delay",      "seconds": 2.0,                    "label": "Wait for Notepad"},
            {"type": "type_clip",  "text": "{text}",                  "label": "Type content"},
            {"type": "hotkey",     "keys": ["ctrl", "s"],             "label": "Save (Ctrl+S)"},
            {"type": "delay",      "seconds": 1.0,                    "label": "Wait for dialog"},
            {"type": "hotkey",     "keys": ["ctrl", "a"],             "label": "Select all in filename box"},
            {"type": "type_clip",  "text": "{filename}",              "label": "Type filename"},
            {"type": "press",      "key": "enter",                     "label": "Confirm save"},
            {"type": "verify",     "expected": "Notepad title bar shows the saved filename",
             "label": "Verify file saved"},
        ]
    },

    "notepad_open_and_type_only": {
        "tier": "gui",
        "description": "Open Notepad and type text without saving",
        "examples": [
            "open notepad and type",
            "write text in notepad",
            "type something in notepad"
        ],
        "params": ["text"],
        "steps": [
            {"type": "win_search", "query": "Notepad",              "label": "Search Notepad"},
            {"type": "delay",      "seconds": 1.5,                   "label": "Wait"},
            {"type": "press",      "key": "enter",                    "label": "Open Notepad"},
            {"type": "delay",      "seconds": 2.0,                    "label": "Wait"},
            {"type": "type_clip",  "text": "{text}",                  "label": "Type text"},
        ]
    },

    "notepad_find_and_replace": {
        "tier": "gui",
        "description": "Open Notepad Find & Replace dialog and replace text",
        "examples": [
            "find and replace in notepad",
            "replace text in notepad",
            "notepad find replace"
        ],
        "params": ["find_text", "replace_text"],
        "steps": [
            {"type": "hotkey",    "keys": ["ctrl", "h"],             "label": "Open Find & Replace"},
            {"type": "delay",     "seconds": 0.8,                    "label": "Wait for dialog"},
            {"type": "type_clip", "text": "{find_text}",             "label": "Type find text"},
            {"type": "press",     "key": "tab",                       "label": "Move to Replace field"},
            {"type": "type_clip", "text": "{replace_text}",          "label": "Type replace text"},
            {"type": "hotkey",    "keys": ["alt", "a"],              "label": "Replace All"},
            {"type": "press",     "key": "escape",                    "label": "Close dialog"},
        ]
    },

    "notepad_select_all_copy": {
        "tier": "gui",
        "description": "In Notepad, select all text and copy it to clipboard",
        "examples": [
            "select all and copy in notepad",
            "copy all notepad text",
            "copy everything from notepad"
        ],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["ctrl", "a"],               "label": "Select All"},
            {"type": "hotkey", "keys": ["ctrl", "c"],               "label": "Copy"},
        ]
    },

    "paste_text_to_focused": {
        "tier": "gui",
        "description": "Paste any text into whatever window is currently active",
        "examples": [
            "type this text into the current app",
            "paste text here in the open window",
            "write this in the current window"
        ],
        "params": ["text"],
        "steps": [
            {"type": "type_clip",  "text": "{text}",  "label": "Paste text via clipboard"},
        ]
    },

    # ══════════════════════════════════════════════════════════════════════
    #  SECTION 4 — FILE EXPLORER
    # ══════════════════════════════════════════════════════════════════════

    "explorer_create_folder": {
        "tier": "gui",
        "description": "Navigate to a folder in Explorer and create a new subfolder",
        "examples": [
            "create a new folder in downloads",
            "make folder called projects in documents",
            "new folder on desktop"
        ],
        "params": ["folderpath", "folder_name"],
        "steps": [
            {"type": "win_search", "query": "File Explorer",       "label": "Search Explorer"},
            {"type": "delay",      "seconds": 1.5,                  "label": "Wait"},
            {"type": "press",      "key": "enter",                   "label": "Open Explorer"},
            {"type": "delay",      "seconds": 1.5,                   "label": "Wait"},
            {"type": "hotkey",     "keys": ["ctrl", "l"],            "label": "Focus address bar"},
            {"type": "delay",      "seconds": 0.4,                   "label": "Wait"},
            {"type": "type_clip",  "text": "{folderpath}",           "label": "Type path"},
            {"type": "press",      "key": "enter",                    "label": "Navigate"},
            {"type": "delay",      "seconds": 1.0,                    "label": "Wait"},
            {"type": "hotkey",     "keys": ["ctrl", "shift", "n"],   "label": "New Folder"},
            {"type": "delay",      "seconds": 0.5,                    "label": "Wait for name box"},
            {"type": "hotkey",     "keys": ["ctrl", "a"],             "label": "Select default name"},
            {"type": "type_clip",  "text": "{folder_name}",          "label": "Type folder name"},
            {"type": "press",      "key": "enter",                     "label": "Confirm"},
        ]
    },

    "explorer_rename_file": {
        "tier": "gui",
        "description": "Rename the currently selected file or folder (F2)",
        "examples": [
            "rename this file",
            "rename selected file to something",
            "change name of selected folder"
        ],
        "params": ["new_name"],
        "steps": [
            {"type": "press",      "key": "f2",                      "label": "Start Rename (F2)"},
            {"type": "delay",      "seconds": 0.4,                    "label": "Wait"},
            {"type": "hotkey",     "keys": ["ctrl", "a"],             "label": "Select all"},
            {"type": "type_clip",  "text": "{new_name}",              "label": "Type new name"},
            {"type": "press",      "key": "enter",                     "label": "Confirm"},
        ]
    },

    "explorer_go_to_path": {
        "tier": "gui",
        "description": "In the open File Explorer, navigate to a specific folder path",
        "examples": [
            "navigate to a folder in explorer",
            "go to path in file explorer",
            "open folder path in explorer"
        ],
        "params": ["folderpath"],
        "steps": [
            {"type": "hotkey",    "keys": ["ctrl", "l"],             "label": "Focus address bar"},
            {"type": "delay",     "seconds": 0.4,                     "label": "Wait"},
            {"type": "type_clip", "text": "{folderpath}",             "label": "Type path"},
            {"type": "press",     "key": "enter",                      "label": "Navigate"},
            {"type": "delay",     "seconds": 1.0,                      "label": "Wait"},
        ]
    },

    "explorer_search_files": {
        "tier": "gui",
        "description": "Search for files by name in current Explorer window",
        "examples": [
            "search for file in explorer",
            "find file called report in this folder",
            "search files in explorer"
        ],
        "params": ["query"],
        "steps": [
            {"type": "hotkey",    "keys": ["ctrl", "f"],             "label": "Open Explorer search"},
            {"type": "delay",     "seconds": 0.4,                     "label": "Wait"},
            {"type": "type_clip", "text": "{query}",                  "label": "Type search term"},
            {"type": "press",     "key": "enter",                      "label": "Search"},
            {"type": "delay",     "seconds": 2.0,                      "label": "Wait for results"},
        ]
    },

    "explorer_select_all": {
        "tier": "gui",
        "description": "Select all files in the current Explorer window",
        "examples": [
            "select all files in explorer",
            "select everything in this folder",
            "ctrl a in file explorer"
        ],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["ctrl", "a"],                 "label": "Select All (Ctrl+A)"},
        ]
    },

    "explorer_copy_selected": {
        "tier": "gui",
        "description": "Copy selected files in Explorer to clipboard",
        "examples": [
            "copy selected files",
            "copy files to clipboard in explorer",
            "ctrl c in file explorer"
        ],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["ctrl", "c"],                 "label": "Copy (Ctrl+C)"},
        ]
    },

    "explorer_paste_here": {
        "tier": "gui",
        "description": "Paste files from clipboard into current Explorer folder",
        "examples": [
            "paste files here",
            "paste copied files into this folder",
            "ctrl v in file explorer"
        ],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["ctrl", "v"],                 "label": "Paste (Ctrl+V)"},
            {"type": "delay",  "seconds": 1.0,                         "label": "Wait for paste"},
        ]
    },

    "explorer_cut_selected": {
        "tier": "gui",
        "description": "Cut/move selected files in Explorer",
        "examples": [
            "cut selected files",
            "move files to clipboard",
            "cut file in explorer"
        ],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["ctrl", "x"],                 "label": "Cut (Ctrl+X)"},
        ]
    },

    "explorer_delete_selected": {
        "tier": "gui",
        "description": "Delete selected files (send to Recycle Bin)",
        "examples": [
            "delete selected file",
            "move to recycle bin",
            "delete selected in explorer"
        ],
        "params": [],
        "steps": [
            {"type": "press",  "key": "delete",                        "label": "Delete (Del key)"},
            {"type": "delay",  "seconds": 0.3,                         "label": "Wait"},
        ]
    },

    "explorer_permanent_delete": {
        "tier": "gui",
        "description": "Permanently delete selected files (bypasses Recycle Bin)",
        "examples": [
            "permanently delete file",
            "delete without recycle bin",
            "shift delete file"
        ],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["shift", "delete"],            "label": "Permanent Delete"},
            {"type": "delay",  "seconds": 0.5,                          "label": "Wait for confirm"},
            {"type": "press",  "key": "enter",                           "label": "Confirm deletion"},
        ]
    },

    "explorer_zip_selected": {
        "tier": "gui",
        "description": "Compress/zip selected files using Windows built-in",
        "examples": [
            "zip selected files",
            "compress selected files",
            "create zip archive"
        ],
        "params": [],
        "steps": [
            {"type": "hotkey",    "keys": ["ctrl", "shift", "z"],     "label": "Try zip shortcut"},
            # Most Windows 11 systems support this; older ones need right-click context menu
        ]
    },

    "explorer_open_properties": {
        "tier": "gui",
        "description": "Open properties of selected file or folder",
        "examples": [
            "show file properties",
            "open properties of selected",
            "check file properties"
        ],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["alt", "enter"],               "label": "Open Properties (Alt+Enter)"},
            {"type": "delay",  "seconds": 0.5,                          "label": "Wait"},
        ]
    },

    "explorer_new_text_file": {
        "tier": "gui",
        "description": "Create a new text file in the current Explorer folder",
        "examples": [
            "create new text file in this folder",
            "new txt file here"
        ],
        "params": ["filename"],
        "steps": [
            {"type": "hotkey",    "keys": ["ctrl", "shift", "n"],     "label": "Create new folder first"},
            # Note: Windows doesn't have direct keyboard shortcut for new .txt
            # Use the right-click context menu via application key instead
            {"type": "press",     "key": "apps",                       "label": "Open context menu"},
            {"type": "delay",     "seconds": 0.5,                       "label": "Wait"},
        ]
    },

    "explorer_undo_action": {
        "tier": "gui",
        "description": "Undo the last file operation in Explorer (rename/delete/move)",
        "examples": [
            "undo file operation in explorer",
            "undo rename in explorer",
            "ctrl z in file explorer"
        ],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["ctrl", "z"],                  "label": "Undo (Ctrl+Z)"},
        ]
    },

    # ══════════════════════════════════════════════════════════════════════
    #  SECTION 5 — SCREENSHOTS & SNIPPING
    # ══════════════════════════════════════════════════════════════════════

    "screenshot_full_screen_save": {
        "tier": "gui",
        "description": "Capture full screen and auto-save to Pictures/Screenshots",
        "examples": [
            "save full screenshot automatically",
            "take screenshot and save it",
            "win prtsc screenshot"
        ],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["win", "prtsc"],              "label": "Screenshot (Win+PrtSc)"},
            {"type": "delay",  "seconds": 0.5,                         "label": "Wait — saved to Pictures/Screenshots"},
        ]
    },

    "screenshot_region": {
        "tier": "gui",
        "description": "Take a region screenshot using Snip & Sketch",
        "examples": [
            "take region screenshot",
            "screenshot part of screen",
            "snip region of screen",
            "win shift s screenshot"
        ],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["win", "shift", "s"],         "label": "Open Snip & Sketch"},
        ]
    },

    "screenshot_then_paint": {
        "tier": "gui",
        "description": "Take a screenshot and open in Paint for annotation",
        "examples": [
            "screenshot and annotate in paint",
            "take screenshot open in paint",
            "snip and draw"
        ],
        "params": [],
        "steps": [
            {"type": "hotkey",    "keys": ["win", "shift", "s"],      "label": "Snip & Sketch"},
            {"type": "delay",     "seconds": 3.0,                      "label": "Take screenshot, it copies to clipboard"},
            {"type": "win_search","query": "Paint",                    "label": "Search Paint"},
            {"type": "delay",     "seconds": 1.0,                      "label": "Wait"},
            {"type": "press",     "key": "enter",                       "label": "Open Paint"},
            {"type": "delay",     "seconds": 2.0,                       "label": "Wait for Paint"},
            {"type": "hotkey",    "keys": ["ctrl", "v"],                "label": "Paste screenshot"},
            {"type": "verify",    "expected": "Paint is open with screenshot pasted on canvas",
             "label": "Verify screenshot in Paint"},
        ]
    },

    "screenshot_active_window": {
        "tier": "gui",
        "description": "Capture only the currently active window to clipboard",
        "examples": [
            "screenshot this window only",
            "capture active window",
            "alt print screen"
        ],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["alt", "prtsc"],               "label": "Capture Active Window"},
        ]
    },

    "screenshot_open_snipping_tool": {
        "tier": "gui",
        "description": "Open the full Snipping Tool app for advanced screenshots",
        "examples": [
            "open snipping tool",
            "open snip app",
            "launch snipping tool"
        ],
        "params": [],
        "steps": [
            {"type": "win_search", "query": "Snipping Tool",           "label": "Search Snipping Tool"},
            {"type": "delay",      "seconds": 1.0,                      "label": "Wait"},
            {"type": "press",      "key": "enter",                       "label": "Open Snipping Tool"},
            {"type": "delay",      "seconds": 1.5,                       "label": "Wait"},
        ]
    },

    # ══════════════════════════════════════════════════════════════════════
    #  SECTION 6 — SYSTEM SETTINGS
    # ══════════════════════════════════════════════════════════════════════

    "settings_change_wallpaper": {
        "tier": "gui",
        "description": "Open Personalization settings to change desktop wallpaper",
        "examples": [
            "change desktop wallpaper",
            "change background image",
            "set new wallpaper"
        ],
        "params": [],
        "steps": [
            {"type": "win_search", "query": "background settings",     "label": "Search personalization"},
            {"type": "delay",      "seconds": 1.5,                      "label": "Wait"},
            {"type": "press",      "key": "enter",                       "label": "Open Personalization"},
            {"type": "delay",      "seconds": 2.0,                       "label": "Wait"},
            {"type": "verify",     "expected": "Personalization Background settings page is open",
             "label": "Verify wallpaper settings"},
        ]
    },

    "adjust_brightness_search": {
        "tier": "gui",
        "description": "Open display settings to adjust screen brightness",
        "examples": [
            "adjust screen brightness",
            "change brightness",
            "increase brightness",
            "decrease brightness"
        ],
        "params": [],
        "steps": [
            {"type": "win_search", "query": "Change brightness",       "label": "Search brightness"},
            {"type": "delay",      "seconds": 1.5,                      "label": "Wait"},
            {"type": "press",      "key": "enter",                       "label": "Open Display Settings"},
            {"type": "delay",      "seconds": 2.0,                       "label": "Wait"},
            {"type": "verify",     "expected": "Display settings showing brightness slider",
             "label": "Verify brightness settings"},
        ]
    },

    "settings_dark_mode": {
        "tier": "gui",
        "description": "Open Color settings to toggle Windows dark mode",
        "examples": [
            "enable dark mode",
            "switch to dark mode",
            "turn on dark mode",
            "open dark mode settings"
        ],
        "params": [],
        "steps": [
            {"type": "win_search", "query": "dark mode settings",      "label": "Search dark mode"},
            {"type": "delay",      "seconds": 1.5,                      "label": "Wait"},
            {"type": "press",      "key": "enter",                       "label": "Open Colors Settings"},
            {"type": "delay",      "seconds": 2.0,                       "label": "Wait"},
            {"type": "verify",     "expected": "Windows Colors settings page with dark/light mode option",
             "label": "Verify colors settings"},
        ]
    },

    "settings_night_light": {
        "tier": "gui",
        "description": "Open Night Light settings to reduce blue light",
        "examples": [
            "enable night light",
            "turn on night mode",
            "blue light filter",
            "open night light settings"
        ],
        "params": [],
        "steps": [
            {"type": "win_search", "query": "night light settings",    "label": "Search night light"},
            {"type": "delay",      "seconds": 1.5,                      "label": "Wait"},
            {"type": "press",      "key": "enter",                       "label": "Open Night Light"},
            {"type": "delay",      "seconds": 2.0,                       "label": "Wait"},
        ]
    },

    "settings_wifi": {
        "tier": "gui",
        "description": "Open WiFi network settings page",
        "examples": [
            "open wifi settings",
            "manage wifi networks",
            "wifi settings page"
        ],
        "params": [],
        "steps": [
            {"type": "win_search", "query": "wifi settings",           "label": "Search WiFi settings"},
            {"type": "delay",      "seconds": 1.5,                      "label": "Wait"},
            {"type": "press",      "key": "enter",                       "label": "Open WiFi Settings"},
            {"type": "delay",      "seconds": 2.0,                       "label": "Wait"},
        ]
    },

    "settings_bluetooth": {
        "tier": "gui",
        "description": "Open Bluetooth settings to pair/manage devices",
        "examples": [
            "open bluetooth settings",
            "add bluetooth device",
            "manage bluetooth",
            "pair bluetooth"
        ],
        "params": [],
        "steps": [
            {"type": "win_search", "query": "bluetooth settings",      "label": "Search Bluetooth"},
            {"type": "delay",      "seconds": 1.5,                      "label": "Wait"},
            {"type": "press",      "key": "enter",                       "label": "Open Bluetooth Settings"},
            {"type": "delay",      "seconds": 2.0,                       "label": "Wait"},
        ]
    },

    "settings_sound": {
        "tier": "gui",
        "description": "Open Sound settings to manage audio devices",
        "examples": [
            "open sound settings",
            "audio output settings",
            "change sound device",
            "speaker settings"
        ],
        "params": [],
        "steps": [
            {"type": "win_search", "query": "sound settings",          "label": "Search Sound settings"},
            {"type": "delay",      "seconds": 1.5,                      "label": "Wait"},
            {"type": "press",      "key": "enter",                       "label": "Open Sound Settings"},
            {"type": "delay",      "seconds": 2.0,                       "label": "Wait"},
        ]
    },

    "settings_display": {
        "tier": "gui",
        "description": "Open Display settings (resolution, scaling, multiple monitors)",
        "examples": [
            "open display settings",
            "screen resolution settings",
            "monitor settings",
            "change screen resolution"
        ],
        "params": [],
        "steps": [
            {"type": "win_search", "query": "display settings",        "label": "Search Display settings"},
            {"type": "delay",      "seconds": 1.5,                      "label": "Wait"},
            {"type": "press",      "key": "enter",                       "label": "Open Display Settings"},
            {"type": "delay",      "seconds": 2.0,                       "label": "Wait"},
        ]
    },

    "settings_default_apps": {
        "tier": "gui",
        "description": "Open Default Apps settings to change default browser, email, etc.",
        "examples": [
            "change default browser",
            "default apps settings",
            "set default applications",
            "change default email app"
        ],
        "params": [],
        "steps": [
            {"type": "win_search", "query": "default apps",            "label": "Search Default Apps"},
            {"type": "delay",      "seconds": 1.5,                      "label": "Wait"},
            {"type": "press",      "key": "enter",                       "label": "Open Default Apps"},
            {"type": "delay",      "seconds": 2.0,                       "label": "Wait"},
        ]
    },

    "settings_language": {
        "tier": "gui",
        "description": "Open Language & Region settings",
        "examples": [
            "open language settings",
            "change language",
            "language and region settings",
            "add new language"
        ],
        "params": [],
        "steps": [
            {"type": "win_search", "query": "language settings",       "label": "Search Language"},
            {"type": "delay",      "seconds": 1.5,                      "label": "Wait"},
            {"type": "press",      "key": "enter",                       "label": "Open Language Settings"},
            {"type": "delay",      "seconds": 2.0,                       "label": "Wait"},
        ]
    },

    "settings_power_sleep": {
        "tier": "gui",
        "description": "Open Power & Sleep settings",
        "examples": [
            "power and sleep settings",
            "change sleep settings",
            "screen timeout settings",
            "power plan settings"
        ],
        "params": [],
        "steps": [
            {"type": "win_search", "query": "power and sleep settings","label": "Search Power settings"},
            {"type": "delay",      "seconds": 1.5,                      "label": "Wait"},
            {"type": "press",      "key": "enter",                       "label": "Open Power Settings"},
            {"type": "delay",      "seconds": 2.0,                       "label": "Wait"},
        ]
    },

    "settings_storage": {
        "tier": "gui",
        "description": "Open Storage settings to check disk usage and clean up",
        "examples": [
            "check storage settings",
            "disk usage settings",
            "storage sense settings",
            "free up disk space settings"
        ],
        "params": [],
        "steps": [
            {"type": "win_search", "query": "storage settings",        "label": "Search Storage"},
            {"type": "delay",      "seconds": 1.5,                      "label": "Wait"},
            {"type": "press",      "key": "enter",                       "label": "Open Storage Settings"},
            {"type": "delay",      "seconds": 2.0,                       "label": "Wait"},
        ]
    },

    "settings_focus_assist": {
        "tier": "gui",
        "description": "Open Focus Assist / Do Not Disturb settings",
        "examples": [
            "open focus assist",
            "do not disturb settings",
            "turn on focus mode",
            "notification settings"
        ],
        "params": [],
        "steps": [
            {"type": "win_search", "query": "focus assist",            "label": "Search Focus Assist"},
            {"type": "delay",      "seconds": 1.5,                      "label": "Wait"},
            {"type": "press",      "key": "enter",                       "label": "Open Focus Assist"},
            {"type": "delay",      "seconds": 2.0,                       "label": "Wait"},
        ]
    },

    "settings_accessibility": {
        "tier": "gui",
        "description": "Open Accessibility settings",
        "examples": [
            "open accessibility settings",
            "ease of access",
            "accessibility options"
        ],
        "params": [],
        "steps": [
            {"type": "win_search", "query": "accessibility settings",  "label": "Search Accessibility"},
            {"type": "delay",      "seconds": 1.5,                      "label": "Wait"},
            {"type": "press",      "key": "enter",                       "label": "Open Accessibility"},
            {"type": "delay",      "seconds": 2.0,                       "label": "Wait"},
        ]
    },

    "settings_accounts": {
        "tier": "gui",
        "description": "Open Accounts settings (Microsoft account, sign-in options)",
        "examples": [
            "open accounts settings",
            "sign in options",
            "microsoft account settings",
            "change account settings"
        ],
        "params": [],
        "steps": [
            {"type": "win_search", "query": "accounts settings",       "label": "Search Accounts"},
            {"type": "delay",      "seconds": 1.5,                      "label": "Wait"},
            {"type": "press",      "key": "enter",                       "label": "Open Accounts"},
            {"type": "delay",      "seconds": 2.0,                       "label": "Wait"},
        ]
    },

    "settings_mouse": {
        "tier": "gui",
        "description": "Open Mouse settings to change pointer speed, scroll etc.",
        "examples": [
            "mouse settings",
            "change mouse speed",
            "pointer settings",
            "scroll speed settings"
        ],
        "params": [],
        "steps": [
            {"type": "win_search", "query": "mouse settings",          "label": "Search Mouse settings"},
            {"type": "delay",      "seconds": 1.5,                      "label": "Wait"},
            {"type": "press",      "key": "enter",                       "label": "Open Mouse Settings"},
            {"type": "delay",      "seconds": 2.0,                       "label": "Wait"},
        ]
    },

    "settings_keyboard": {
        "tier": "gui",
        "description": "Open Keyboard settings (repeat delay, input language)",
        "examples": [
            "keyboard settings",
            "keyboard input settings",
            "change keyboard layout"
        ],
        "params": [],
        "steps": [
            {"type": "win_search", "query": "keyboard settings",       "label": "Search Keyboard settings"},
            {"type": "delay",      "seconds": 1.5,                      "label": "Wait"},
            {"type": "press",      "key": "enter",                       "label": "Open Keyboard Settings"},
            {"type": "delay",      "seconds": 2.0,                       "label": "Wait"},
        ]
    },

    # ══════════════════════════════════════════════════════════════════════
    #  SECTION 7 — OFFICE (Word, Excel, PowerPoint)
    # ══════════════════════════════════════════════════════════════════════

    "word_open_and_type": {
        "tier": "gui",
        "description": "Open Microsoft Word and type content in a new document",
        "examples": [
            "open word and write a letter",
            "type something in microsoft word",
            "write content in word document"
        ],
        "params": ["content"],
        "steps": [
            {"type": "win_search", "query": "Microsoft Word",          "label": "Search Word"},
            {"type": "delay",      "seconds": 1.5,                      "label": "Wait"},
            {"type": "press",      "key": "enter",                       "label": "Open Word"},
            {"type": "delay",      "seconds": 4.0,                       "label": "Wait for Word"},
            {"type": "press",      "key": "escape",                      "label": "Dismiss splash"},
            {"type": "delay",      "seconds": 0.5,                       "label": "Wait"},
            {"type": "type_clip",  "text": "{content}",                  "label": "Type content"},
            {"type": "hotkey",     "keys": ["ctrl", "s"],                "label": "Save"},
            {"type": "verify",     "expected": "Word document with typed content visible",
             "label": "Verify Word content"},
        ]
    },

    "word_new_document": {
        "tier": "gui",
        "description": "In an open Word window, create a brand new blank document",
        "examples": [
            "new word document",
            "create blank word document",
            "open new document in word"
        ],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["ctrl", "n"],                   "label": "New Document (Ctrl+N)"},
            {"type": "delay",  "seconds": 1.0,                           "label": "Wait"},
        ]
    },

    "word_save_document": {
        "tier": "gui",
        "description": "Save the current Word document",
        "examples": [
            "save word document",
            "ctrl s in word",
            "save current word file"
        ],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["ctrl", "s"],                   "label": "Save (Ctrl+S)"},
            {"type": "delay",  "seconds": 0.5,                           "label": "Wait"},
            {"type": "press",  "key": "enter",                            "label": "Confirm if dialog appears"},
        ]
    },

    "word_format_selected_bold": {
        "tier": "gui",
        "description": "Make selected text bold in Word",
        "examples": [
            "make text bold in word",
            "bold selected text",
            "bold in word document"
        ],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["ctrl", "b"],                   "label": "Bold (Ctrl+B)"},
        ]
    },

    "word_insert_heading": {
        "tier": "gui",
        "description": "Type a heading and apply Heading 1 style in Word",
        "examples": [
            "add heading to word document",
            "insert heading 1 in word",
            "type heading in word"
        ],
        "params": ["heading_text"],
        "steps": [
            {"type": "hotkey",    "keys": ["ctrl", "alt", "1"],         "label": "Apply Heading 1"},
            {"type": "type_clip", "text": "{heading_text}",              "label": "Type heading"},
            {"type": "press",     "key": "enter",                         "label": "New line"},
            {"type": "hotkey",    "keys": ["ctrl", "alt", "n"],          "label": "Apply Normal style"},
        ]
    },

    "excel_open_and_type": {
        "tier": "gui",
        "description": "Open Excel and type data into a new spreadsheet",
        "examples": [
            "open excel and enter data",
            "type in excel spreadsheet",
            "open excel and add data"
        ],
        "params": ["content"],
        "steps": [
            {"type": "win_search", "query": "Microsoft Excel",          "label": "Search Excel"},
            {"type": "delay",      "seconds": 1.5,                       "label": "Wait"},
            {"type": "press",      "key": "enter",                        "label": "Open Excel"},
            {"type": "delay",      "seconds": 4.0,                        "label": "Wait for Excel"},
            {"type": "press",      "key": "escape",                       "label": "Dismiss splash"},
            {"type": "delay",      "seconds": 0.5,                        "label": "Wait"},
            {"type": "type_clip",  "text": "{content}",                   "label": "Type data"},
            {"type": "press",      "key": "enter",                         "label": "Confirm cell"},
            {"type": "hotkey",     "keys": ["ctrl", "s"],                 "label": "Save"},
        ]
    },

    "excel_new_sheet": {
        "tier": "gui",
        "description": "In open Excel, insert a new worksheet",
        "examples": [
            "new excel sheet",
            "add new worksheet in excel",
            "insert sheet in excel"
        ],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["shift", "f11"],                "label": "Insert New Sheet (Shift+F11)"},
            {"type": "delay",  "seconds": 0.5,                           "label": "Wait"},
        ]
    },

    "powerpoint_new_presentation": {
        "tier": "gui",
        "description": "Open PowerPoint with a new blank presentation",
        "examples": [
            "open powerpoint new presentation",
            "create new ppt presentation",
            "launch powerpoint blank"
        ],
        "params": [],
        "steps": [
            {"type": "win_search", "query": "PowerPoint",               "label": "Search PowerPoint"},
            {"type": "delay",      "seconds": 1.5,                       "label": "Wait"},
            {"type": "press",      "key": "enter",                        "label": "Open PowerPoint"},
            {"type": "delay",      "seconds": 4.0,                        "label": "Wait for PPT"},
            {"type": "press",      "key": "escape",                       "label": "Dismiss splash"},
            {"type": "delay",      "seconds": 0.5,                        "label": "Wait"},
        ]
    },

    "powerpoint_add_slide": {
        "tier": "gui",
        "description": "Add a new slide in the open PowerPoint presentation",
        "examples": [
            "add new slide in powerpoint",
            "insert slide in ppt",
            "new slide in presentation"
        ],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["ctrl", "m"],                   "label": "New Slide (Ctrl+M)"},
            {"type": "delay",  "seconds": 0.5,                           "label": "Wait"},
        ]
    },

    # ══════════════════════════════════════════════════════════════════════
    #  SECTION 8 — CALCULATOR
    # ══════════════════════════════════════════════════════════════════════

    "calculator_compute": {
        "tier": "gui",
        "description": "Open Calculator and evaluate a math expression",
        "examples": [
            "calculate 42 times 7",
            "compute 100 divided by 4",
            "what is 25 plus 75",
            "open calculator and compute expression"
        ],
        "params": ["expression"],
        "steps": [
            {"type": "win_search", "query": "Calculator",               "label": "Search Calculator"},
            {"type": "delay",      "seconds": 1.5,                       "label": "Wait"},
            {"type": "press",      "key": "enter",                        "label": "Open Calculator"},
            {"type": "delay",      "seconds": 2.0,                        "label": "Wait"},
            {"type": "type_clip",  "text": "{expression}",                "label": "Type expression"},
            {"type": "press",      "key": "enter",                         "label": "Calculate"},
            {"type": "verify",     "expected": "Calculator showing numeric result",
             "label": "Verify result"},
        ]
    },

    "calculator_scientific_mode": {
        "tier": "gui",
        "description": "Open Calculator in Scientific mode",
        "examples": [
            "open scientific calculator",
            "calculator scientific mode",
            "switch calculator to scientific"
        ],
        "params": [],
        "steps": [
            {"type": "win_search", "query": "Calculator",               "label": "Search Calculator"},
            {"type": "delay",      "seconds": 1.5,                       "label": "Wait"},
            {"type": "press",      "key": "enter",                        "label": "Open Calculator"},
            {"type": "delay",      "seconds": 2.0,                        "label": "Wait"},
            {"type": "hotkey",     "keys": ["alt", "2"],                  "label": "Switch to Scientific (Alt+2)"},
        ]
    },

    "calculator_currency_converter": {
        "tier": "gui",
        "description": "Open Calculator in Currency Converter mode",
        "examples": [
            "currency converter in calculator",
            "open currency calculator",
            "convert currency in calculator"
        ],
        "params": [],
        "steps": [
            {"type": "win_search", "query": "Calculator",               "label": "Search Calculator"},
            {"type": "delay",      "seconds": 1.5,                       "label": "Wait"},
            {"type": "press",      "key": "enter",                        "label": "Open Calculator"},
            {"type": "delay",      "seconds": 2.0,                        "label": "Wait"},
            {"type": "hotkey",     "keys": ["alt", "8"],                  "label": "Switch to Currency (Alt+8)"},
        ]
    },

    # ══════════════════════════════════════════════════════════════════════
    #  SECTION 9 — MEDIA CONTROLS
    # ══════════════════════════════════════════════════════════════════════

    "media_play_pause": {
        "tier": "gui",
        "description": "Toggle play/pause for any media currently playing",
        "examples": [
            "play pause music",
            "pause the song",
            "play music",
            "toggle media playback"
        ],
        "params": [],
        "steps": [
            {"type": "press",  "key": "playpause",                      "label": "Play/Pause media key"},
        ]
    },

    "media_next_track": {
        "tier": "gui",
        "description": "Skip to the next track",
        "examples": [
            "next song", "skip track",
            "next music track", "go to next song"
        ],
        "params": [],
        "steps": [
            {"type": "press",  "key": "nexttrack",                      "label": "Next Track"},
        ]
    },

    "media_previous_track": {
        "tier": "gui",
        "description": "Go back to the previous track",
        "examples": [
            "previous song", "go back to last song",
            "previous track", "play previous music"
        ],
        "params": [],
        "steps": [
            {"type": "press",  "key": "prevtrack",                      "label": "Previous Track"},
        ]
    },

    "media_stop": {
        "tier": "gui",
        "description": "Stop media playback completely",
        "examples": [
            "stop music", "stop media",
            "stop playing", "stop playback"
        ],
        "params": [],
        "steps": [
            {"type": "press",  "key": "stop",                           "label": "Stop media key"},
        ]
    },

    "open_vlc_play_file": {
        "tier": "gui",
        "description": "Open VLC Media Player and open a file for playback",
        "examples": [
            "open vlc and play file",
            "play video in vlc",
            "open media in vlc player"
        ],
        "params": ["filepath"],
        "steps": [
            {"type": "win_search", "query": "VLC",                      "label": "Search VLC"},
            {"type": "delay",      "seconds": 1.5,                       "label": "Wait"},
            {"type": "press",      "key": "enter",                        "label": "Open VLC"},
            {"type": "delay",      "seconds": 2.5,                        "label": "Wait for VLC"},
            {"type": "hotkey",     "keys": ["ctrl", "o"],                 "label": "Open File (Ctrl+O)"},
            {"type": "delay",      "seconds": 1.0,                        "label": "Wait for file dialog"},
            {"type": "type_clip",  "text": "{filepath}",                  "label": "Type file path"},
            {"type": "press",      "key": "enter",                         "label": "Open file"},
        ]
    },

    # ══════════════════════════════════════════════════════════════════════
    #  SECTION 10 — UTILITIES (Clock, Sticky Notes, Calendar)
    # ══════════════════════════════════════════════════════════════════════

    "clock_open": {
        "tier": "gui",
        "description": "Open the Windows Clock app",
        "examples": [
            "open clock", "open windows clock",
            "launch clock app", "open alarms and clock"
        ],
        "params": [],
        "steps": [
            {"type": "win_search", "query": "Clock",                    "label": "Search Clock"},
            {"type": "delay",      "seconds": 1.5,                       "label": "Wait"},
            {"type": "press",      "key": "enter",                        "label": "Open Clock"},
            {"type": "delay",      "seconds": 2.0,                        "label": "Wait"},
        ]
    },

    "clock_open_timer_tab": {
        "tier": "gui",
        "description": "Open Clock app and navigate to the Timer tab",
        "examples": [
            "open timer", "set a timer",
            "open clock timer", "go to timer in clock"
        ],
        "params": [],
        "steps": [
            {"type": "win_search", "query": "Clock",                    "label": "Search Clock"},
            {"type": "delay",      "seconds": 1.5,                       "label": "Wait"},
            {"type": "press",      "key": "enter",                        "label": "Open Clock"},
            {"type": "delay",      "seconds": 2.0,                        "label": "Wait"},
            {"type": "hotkey",     "keys": ["ctrl", "3"],                 "label": "Go to Timer tab (Ctrl+3)"},
        ]
    },

    "clock_open_alarm_tab": {
        "tier": "gui",
        "description": "Open Clock app and navigate to the Alarm tab",
        "examples": [
            "open alarm", "set an alarm",
            "open alarms", "add alarm in clock"
        ],
        "params": [],
        "steps": [
            {"type": "win_search", "query": "Clock",                    "label": "Search Clock"},
            {"type": "delay",      "seconds": 1.5,                       "label": "Wait"},
            {"type": "press",      "key": "enter",                        "label": "Open Clock"},
            {"type": "delay",      "seconds": 2.0,                        "label": "Wait"},
            {"type": "hotkey",     "keys": ["ctrl", "1"],                 "label": "Go to Alarm tab (Ctrl+1)"},
        ]
    },

    "clock_open_stopwatch": {
        "tier": "gui",
        "description": "Open Clock app and go to the Stopwatch tab",
        "examples": [
            "open stopwatch",
            "start stopwatch",
            "open clock stopwatch"
        ],
        "params": [],
        "steps": [
            {"type": "win_search", "query": "Clock",                    "label": "Search Clock"},
            {"type": "delay",      "seconds": 1.5,                       "label": "Wait"},
            {"type": "press",      "key": "enter",                        "label": "Open Clock"},
            {"type": "delay",      "seconds": 2.0,                        "label": "Wait"},
            {"type": "hotkey",     "keys": ["ctrl", "4"],                 "label": "Go to Stopwatch (Ctrl+4)"},
        ]
    },

    "sticky_notes_new": {
        "tier": "gui",
        "description": "Open Sticky Notes app and create a new note",
        "examples": [
            "open sticky notes",
            "create new sticky note",
            "add a sticky note",
            "new note on desktop"
        ],
        "params": [],
        "steps": [
            {"type": "win_search", "query": "Sticky Notes",             "label": "Search Sticky Notes"},
            {"type": "delay",      "seconds": 1.5,                       "label": "Wait"},
            {"type": "press",      "key": "enter",                        "label": "Open Sticky Notes"},
            {"type": "delay",      "seconds": 2.0,                        "label": "Wait"},
            {"type": "hotkey",     "keys": ["ctrl", "n"],                 "label": "New Note (Ctrl+N)"},
        ]
    },

    "sticky_notes_type": {
        "tier": "gui",
        "description": "Open Sticky Notes, create a new note, and type content",
        "examples": [
            "create sticky note with text",
            "write a sticky note saying something",
            "add note to desktop with content"
        ],
        "params": ["note_text"],
        "steps": [
            {"type": "win_search", "query": "Sticky Notes",             "label": "Search Sticky Notes"},
            {"type": "delay",      "seconds": 1.5,                       "label": "Wait"},
            {"type": "press",      "key": "enter",                        "label": "Open Sticky Notes"},
            {"type": "delay",      "seconds": 2.0,                        "label": "Wait"},
            {"type": "hotkey",     "keys": ["ctrl", "n"],                 "label": "New Note"},
            {"type": "delay",      "seconds": 0.5,                        "label": "Wait"},
            {"type": "type_clip",  "text": "{note_text}",                 "label": "Type note content"},
        ]
    },

    "calendar_open": {
        "tier": "gui",
        "description": "Open the Windows Calendar app",
        "examples": [
            "open calendar",
            "launch calendar app",
            "open windows calendar",
            "show my calendar"
        ],
        "params": [],
        "steps": [
            {"type": "win_search", "query": "Calendar",                 "label": "Search Calendar"},
            {"type": "delay",      "seconds": 1.5,                       "label": "Wait"},
            {"type": "press",      "key": "enter",                        "label": "Open Calendar"},
            {"type": "delay",      "seconds": 2.0,                        "label": "Wait"},
        ]
    },

    "calendar_new_event": {
        "tier": "gui",
        "description": "Open Calendar and create a new event",
        "examples": [
            "add event to calendar",
            "create calendar event",
            "new calendar appointment"
        ],
        "params": ["event_title"],
        "steps": [
            {"type": "win_search", "query": "Calendar",                 "label": "Search Calendar"},
            {"type": "delay",      "seconds": 1.5,                       "label": "Wait"},
            {"type": "press",      "key": "enter",                        "label": "Open Calendar"},
            {"type": "delay",      "seconds": 2.0,                        "label": "Wait"},
            {"type": "hotkey",     "keys": ["ctrl", "n"],                 "label": "New Event (Ctrl+N)"},
            {"type": "delay",      "seconds": 1.0,                        "label": "Wait for new event form"},
            {"type": "type_clip",  "text": "{event_title}",               "label": "Type event title"},
        ]
    },

    # ══════════════════════════════════════════════════════════════════════
    #  SECTION 11 — TASK MANAGER
    # ══════════════════════════════════════════════════════════════════════

    "task_manager_open": {
        "tier": "gui",
        "description": "Open Task Manager directly with Ctrl+Shift+Esc",
        "examples": [
            "open task manager",
            "ctrl shift esc",
            "launch task manager",
            "force open task manager"
        ],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["ctrl", "shift", "esc"],       "label": "Open Task Manager"},
            {"type": "delay",  "seconds": 2.0,                          "label": "Wait"},
            {"type": "verify", "expected": "Task Manager window is open showing processes",
             "label": "Verify Task Manager"},
        ]
    },

    "task_manager_end_task": {
        "tier": "gui",
        "description": "Open Task Manager via Ctrl+Shift+Esc to end a specific process",
        "examples": [
            "end task in task manager",
            "force close app via task manager",
            "kill process in task manager"
        ],
        "params": ["app_name"],
        "steps": [
            {"type": "hotkey", "keys": ["ctrl", "shift", "esc"],       "label": "Open Task Manager"},
            {"type": "delay",  "seconds": 2.0,                          "label": "Wait"},
            {"type": "verify", "expected": "Task Manager is open showing {app_name} in list",
             "label": "Verify Task Manager opened"},
        ]
    },

    "task_manager_performance": {
        "tier": "gui",
        "description": "Open Task Manager and switch to Performance tab",
        "examples": [
            "check performance in task manager",
            "cpu performance tab",
            "view system performance"
        ],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["ctrl", "shift", "esc"],       "label": "Open Task Manager"},
            {"type": "delay",  "seconds": 2.0,                          "label": "Wait"},
            {"type": "hotkey", "keys": ["ctrl", "tab"],                 "label": "Switch to next tab"},
            {"type": "delay",  "seconds": 0.3,                           "label": "Wait"},
        ]
    },

    # ══════════════════════════════════════════════════════════════════════
    #  SECTION 12 — WINDOW MANAGEMENT
    # ══════════════════════════════════════════════════════════════════════

    "window_minimize_current": {
        "tier": "gui",
        "description": "Minimize the currently focused window",
        "examples": [
            "minimize this window",
            "minimize current window",
            "hide this window",
            "minimize active app"
        ],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["win", "down"],                "label": "Minimize (Win+Down)"},
        ]
    },

    "window_maximize_current": {
        "tier": "gui",
        "description": "Maximize the currently focused window",
        "examples": [
            "maximize this window",
            "make window bigger",
            "full screen this window"
        ],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["win", "up"],                  "label": "Maximize (Win+Up)"},
        ]
    },

    "window_close_current": {
        "tier": "gui",
        "description": "Close the currently focused window",
        "examples": [
            "close this window",
            "exit current app",
            "alt f4 close window"
        ],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["alt", "f4"],                  "label": "Close Window (Alt+F4)"},
        ]
    },

    "window_split_side_by_side": {
        "tier": "gui",
        "description": "Open two apps and snap them side by side for split view",
        "examples": [
            "split screen two apps",
            "open two windows side by side",
            "snap two apps side by side"
        ],
        "params": ["app1", "app2"],
        "steps": [
            {"type": "win_search", "query": "{app1}",                  "label": "Search for {app1}"},
            {"type": "delay",      "seconds": 1.5,                      "label": "Wait"},
            {"type": "press",      "key": "enter",                       "label": "Open {app1}"},
            {"type": "delay",      "seconds": 2.0,                       "label": "Wait"},
            {"type": "hotkey",     "keys": ["win", "left"],              "label": "Snap {app1} left"},
            {"type": "delay",      "seconds": 1.0,                       "label": "Wait for snap"},
            {"type": "win_search", "query": "{app2}",                   "label": "Search for {app2}"},
            {"type": "delay",      "seconds": 1.5,                       "label": "Wait"},
            {"type": "press",      "key": "enter",                        "label": "Open {app2}"},
            {"type": "delay",      "seconds": 2.0,                        "label": "Wait"},
            {"type": "hotkey",     "keys": ["win", "right"],              "label": "Snap {app2} right"},
        ]
    },

    "window_move_to_next_monitor": {
        "tier": "gui",
        "description": "Move current window to the next monitor",
        "examples": [
            "move window to other monitor",
            "send window to second screen",
            "move to next monitor"
        ],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["win", "shift", "right"],      "label": "Move to next monitor (Win+Shift+Right)"},
        ]
    },

    "window_always_on_top_toggle": {
        "tier": "gui",
        "description": "Open a specific app via search (no always-on-top shortcut in Windows)",
        "examples": [
            "keep window on top",
            "pin window on top"
        ],
        "params": ["app_name"],
        "steps": [
            {"type": "win_search", "query": "{app_name}",               "label": "Open {app_name}"},
            {"type": "delay",      "seconds": 1.5,                       "label": "Wait"},
            {"type": "press",      "key": "enter",                        "label": "Launch"},
            {"type": "delay",      "seconds": 2.0,                        "label": "Wait"},
        ]
    },

    # ══════════════════════════════════════════════════════════════════════
    #  SECTION 13 — QUICK ACTIONS & SYSTEM CONTROLS
    # ══════════════════════════════════════════════════════════════════════

    "quick_action_wifi_toggle": {
        "tier": "gui",
        "description": "Open Action Center to toggle WiFi on or off",
        "examples": [
            "toggle wifi from action center",
            "turn on wifi via quick settings",
            "disable wifi quick settings"
        ],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["win", "a"],                   "label": "Open Action Center"},
            {"type": "delay",  "seconds": 0.8,                          "label": "Wait"},
            {"type": "verify", "expected": "Action Center is open showing quick toggle buttons",
             "label": "Verify Action Center"},
        ]
    },

    "quick_action_bluetooth_toggle": {
        "tier": "gui",
        "description": "Open Action Center to toggle Bluetooth",
        "examples": [
            "toggle bluetooth quick settings",
            "turn on bluetooth action center",
            "bluetooth quick toggle"
        ],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["win", "a"],                   "label": "Open Action Center"},
            {"type": "delay",  "seconds": 0.8,                          "label": "Wait"},
            {"type": "verify", "expected": "Action Center with Bluetooth toggle visible",
             "label": "Verify Action Center"},
        ]
    },

    "quick_action_airplane_mode": {
        "tier": "gui",
        "description": "Open Action Center for airplane mode toggle",
        "examples": [
            "airplane mode",
            "toggle flight mode",
            "enable airplane mode"
        ],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["win", "a"],                   "label": "Open Action Center"},
            {"type": "delay",  "seconds": 0.8,                          "label": "Wait"},
        ]
    },

    "clipboard_history": {
        "tier": "gui",
        "description": "Open Windows Clipboard History to paste previous items",
        "examples": [
            "open clipboard history",
            "show clipboard history",
            "paste previous item from clipboard",
            "win v clipboard"
        ],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["win", "v"],                   "label": "Clipboard History (Win+V)"},
            {"type": "delay",  "seconds": 0.5,                          "label": "Wait"},
        ]
    },

    "emoji_picker": {
        "tier": "gui",
        "description": "Open Windows Emoji Picker to insert an emoji",
        "examples": [
            "insert emoji",
            "open emoji picker",
            "emoji keyboard",
            "add emoji"
        ],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["win", "."],                   "label": "Emoji Picker (Win+.)"},
            {"type": "delay",  "seconds": 0.5,                          "label": "Wait"},
        ]
    },

    "open_run_and_execute": {
        "tier": "gui",
        "description": "Open Win+R Run dialog and execute any command",
        "examples": [
            "run command via win r",
            "open run dialog and type",
            "win r then execute"
        ],
        "params": ["command"],
        "steps": [
            {"type": "hotkey",    "keys": ["win", "r"],                "label": "Open Run Dialog"},
            {"type": "delay",     "seconds": 0.8,                       "label": "Wait"},
            {"type": "type_clip", "text": "{command}",                  "label": "Type command"},
            {"type": "press",     "key": "enter",                        "label": "Execute"},
        ]
    },

    "switch_to_window_by_app": {
        "tier": "gui",
        "description": "Use Alt+Tab to switch to the most recent window",
        "examples": [
            "switch to previous window",
            "alt tab to other app",
            "go back to last window"
        ],
        "params": [],
        "steps": [
            {"type": "hotkey", "keys": ["alt", "tab"],                 "label": "Alt+Tab to switch"},
        ]
    },

    # ══════════════════════════════════════════════════════════════════════
    #  SECTION 14 — COMMUNICATION APPS
    # ══════════════════════════════════════════════════════════════════════

    "open_outlook_compose": {
        "tier": "gui",
        "description": "Open Microsoft Outlook and compose a new email",
        "examples": [
            "open outlook compose email",
            "write new email in outlook",
            "compose email in outlook"
        ],
        "params": [],
        "steps": [
            {"type": "win_search", "query": "Outlook",                  "label": "Search Outlook"},
            {"type": "delay",      "seconds": 1.5,                       "label": "Wait"},
            {"type": "press",      "key": "enter",                        "label": "Open Outlook"},
            {"type": "delay",      "seconds": 4.0,                        "label": "Wait for Outlook to load"},
            {"type": "hotkey",     "keys": ["ctrl", "n"],                 "label": "New Email (Ctrl+N)"},
            {"type": "delay",      "seconds": 1.0,                        "label": "Wait for compose window"},
        ]
    },

    "open_teams": {
        "tier": "gui",
        "description": "Open Microsoft Teams via Windows Search",
        "examples": [
            "open teams",
            "launch microsoft teams",
            "open ms teams"
        ],
        "params": [],
        "steps": [
            {"type": "win_search", "query": "Microsoft Teams",          "label": "Search Teams"},
            {"type": "delay",      "seconds": 1.5,                       "label": "Wait"},
            {"type": "press",      "key": "enter",                        "label": "Open Teams"},
            {"type": "delay",      "seconds": 4.0,                        "label": "Wait for Teams to load"},
        ]
    },

    "open_whatsapp": {
        "tier": "gui",
        "description": "Open WhatsApp Desktop via Windows Search",
        "examples": [
            "open whatsapp",
            "launch whatsapp desktop",
            "start whatsapp"
        ],
        "params": [],
        "steps": [
            {"type": "win_search", "query": "WhatsApp",                 "label": "Search WhatsApp"},
            {"type": "delay",      "seconds": 1.5,                       "label": "Wait"},
            {"type": "press",      "key": "enter",                        "label": "Open WhatsApp"},
            {"type": "delay",      "seconds": 3.0,                        "label": "Wait for app"},
        ]
    },

    "open_zoom_new_meeting": {
        "tier": "gui",
        "description": "Open Zoom and start a new meeting",
        "examples": [
            "open zoom and start meeting",
            "start zoom meeting",
            "launch zoom new meeting"
        ],
        "params": [],
        "steps": [
            {"type": "win_search", "query": "Zoom",                     "label": "Search Zoom"},
            {"type": "delay",      "seconds": 1.5,                       "label": "Wait"},
            {"type": "press",      "key": "enter",                        "label": "Open Zoom"},
            {"type": "delay",      "seconds": 3.0,                        "label": "Wait for Zoom"},
            {"type": "verify",     "expected": "Zoom app is open with New Meeting or Home screen",
             "label": "Verify Zoom open"},
        ]
    },

    "open_discord": {
        "tier": "gui",
        "description": "Open Discord via Windows Search",
        "examples": [
            "open discord",
            "launch discord",
            "start discord app"
        ],
        "params": [],
        "steps": [
            {"type": "win_search", "query": "Discord",                  "label": "Search Discord"},
            {"type": "delay",      "seconds": 1.5,                       "label": "Wait"},
            {"type": "press",      "key": "enter",                        "label": "Open Discord"},
            {"type": "delay",      "seconds": 3.0,                        "label": "Wait for Discord"},
        ]
    },

    # ══════════════════════════════════════════════════════════════════════
    #  SECTION 15 — MISC PRODUCTIVITY
    # ══════════════════════════════════════════════════════════════════════

    "open_paint_3d": {
        "tier": "gui",
        "description": "Open Paint 3D app",
        "examples": [
            "open paint 3d",
            "launch paint 3d",
            "3d paint app"
        ],
        "params": [],
        "steps": [
            {"type": "win_search", "query": "Paint 3D",                 "label": "Search Paint 3D"},
            {"type": "delay",      "seconds": 1.5,                       "label": "Wait"},
            {"type": "press",      "key": "enter",                        "label": "Open Paint 3D"},
            {"type": "delay",      "seconds": 2.0,                        "label": "Wait"},
        ]
    },

    "open_onenote": {
        "tier": "gui",
        "description": "Open Microsoft OneNote",
        "examples": [
            "open onenote",
            "launch one note",
            "open my notes in onenote"
        ],
        "params": [],
        "steps": [
            {"type": "win_search", "query": "OneNote",                  "label": "Search OneNote"},
            {"type": "delay",      "seconds": 1.5,                       "label": "Wait"},
            {"type": "press",      "key": "enter",                        "label": "Open OneNote"},
            {"type": "delay",      "seconds": 3.0,                        "label": "Wait for OneNote"},
        ]
    },

    "windows_search_and_open_setting": {
        "tier": "gui",
        "description": "Use Windows Search to find and open any settings page by name",
        "examples": [
            "search and open any setting",
            "find setting via windows search",
            "search windows for a setting"
        ],
        "params": ["setting_name"],
        "steps": [
            {"type": "win_search", "query": "{setting_name}",           "label": "Search for {setting_name}"},
            {"type": "delay",      "seconds": 1.5,                       "label": "Wait for results"},
            {"type": "press",      "key": "enter",                        "label": "Open top result"},
            {"type": "delay",      "seconds": 2.0,                        "label": "Wait"},
        ]
    },

    "open_snip_sketch_and_annotate": {
        "tier": "gui",
        "description": "Open Snip & Sketch app to take and annotate a screenshot",
        "examples": [
            "open snip and sketch",
            "annotate screenshot",
            "open screenshot annotation tool"
        ],
        "params": [],
        "steps": [
            {"type": "win_search", "query": "Snip and Sketch",          "label": "Search Snip & Sketch"},
            {"type": "delay",      "seconds": 1.5,                       "label": "Wait"},
            {"type": "press",      "key": "enter",                        "label": "Open Snip & Sketch"},
            {"type": "delay",      "seconds": 2.0,                        "label": "Wait"},
        ]
    },

    "type_in_search_bar": {
        "tier": "gui",
        "description": "Open Windows Search and type a query to search",
        "examples": [
            "search windows for something",
            "open search and type",
            "win s then type query"
        ],
        "params": ["query"],
        "steps": [
            {"type": "win_search", "query": "{query}",                  "label": "Windows Search: {query}"},
            {"type": "delay",      "seconds": 1.5,                       "label": "Wait for results"},
        ]
    },

    "excel_open_existing_file": {
        "tier": "gui",
        "description": "Open an existing Excel file from a path",
        "examples": [
            "open excel file from path",
            "open spreadsheet at location",
            "launch excel and open file"
        ],
        "params": ["filepath"],
        "steps": [
            {"type": "win_search", "query": "Excel",                    "label": "Search Excel"},
            {"type": "delay",      "seconds": 1.5,                       "label": "Wait"},
            {"type": "press",      "key": "enter",                        "label": "Open Excel"},
            {"type": "delay",      "seconds": 3.0,                        "label": "Wait for Excel"},
            {"type": "hotkey",     "keys": ["ctrl", "o"],                 "label": "Open File (Ctrl+O)"},
            {"type": "delay",      "seconds": 1.0,                        "label": "Wait for dialog"},
            {"type": "type_clip",  "text": "{filepath}",                  "label": "Type file path"},
            {"type": "press",      "key": "enter",                         "label": "Open file"},
        ]
    },

    "open_github_desktop": {
        "tier": "gui",
        "description": "Open GitHub Desktop app",
        "examples": [
            "open github desktop",
            "launch github desktop app",
            "start github desktop"
        ],
        "params": [],
        "steps": [
            {"type": "win_search", "query": "GitHub Desktop",           "label": "Search GitHub Desktop"},
            {"type": "delay",      "seconds": 1.5,                       "label": "Wait"},
            {"type": "press",      "key": "enter",                        "label": "Open GitHub Desktop"},
            {"type": "delay",      "seconds": 3.0,                        "label": "Wait"},
        ]
    },


    # ======================================================================
    #  SECTION 16 - AI CONTENT GENERATION + GUI
    #  These playbooks use the local LLM to WRITE the content first,
    #  then automate the GUI to open the app and paste the result.
    #  The 'generate_content' step calls Ollama internally.
    # ======================================================================

    "write_document_word": {
        "tier": "gui",
        "description": "AI generates a document/letter/essay, then opens Word and pastes it",
        "examples": [
            "write a letter to principal in word",
            "write a resignation letter in word",
            "open word and write a formal letter",
            "write a leave application in word",
            "write a complaint letter in word",
            "draft a formal letter in microsoft word",
        ],
        "params": ["content_request", "filename"],
        "steps": [
            {
                "type":        "generate_content",
                "prompt":      "{content_request}",
                "param_name":  "generated_content",
                "max_tokens":  2048,
                "temperature": 0.7,
                "label":       "AI writes the document"
            },
            {"type": "win_search", "query": "Microsoft Word",          "label": "Search Microsoft Word"},
            {"type": "delay",      "seconds": 1.5,                     "label": "Wait for search"},
            {"type": "press",      "key": "enter",                      "label": "Open Word"},
            {"type": "delay",      "seconds": 5.0,                      "label": "Wait for Word to fully load"},
            {"type": "press",      "key": "escape",                     "label": "Dismiss Start Screen"},
            {"type": "delay",      "seconds": 0.8,                      "label": "Wait"},
            {"type": "press",      "key": "escape",                     "label": "Dismiss any remaining dialog"},
            {"type": "delay",      "seconds": 0.5,                      "label": "Wait"},
            {"type": "hotkey",     "keys": ["ctrl", "home"],            "label": "Focus document body (Ctrl+Home)"},
            {"type": "delay",      "seconds": 0.5,                      "label": "Wait"},
            {"type": "type_clip",  "text": "{generated_content}",       "label": "Paste AI-written content"},
            {"type": "delay",      "seconds": 0.5,                      "label": "Wait"},
            {"type": "press",      "key": "f12",                        "label": "Open Save As dialog (F12)"},
            {"type": "delay",      "seconds": 2.0,                      "label": "Wait for Save dialog"},
            {"type": "hotkey",     "keys": ["ctrl", "a"],               "label": "Select filename field"},
            {"type": "type_clip",  "text": "{filename}",                "label": "Type filename"},
            {"type": "press",      "key": "enter",                      "label": "Confirm save"},
            {"type": "delay",      "seconds": 1.0,                      "label": "Wait for save to complete"},
            {
                "type":     "verify",
                "expected": "Word document is open with text content visible",
                "label":    "Verify document saved"
            },
        ]
    },

    "write_document_notepad": {
        "tier": "gui",
        "description": "AI generates content, opens Notepad and saves it as a text file",
        "examples": [
            "write a letter in notepad",
            "create a text file with a formal letter",
            "notepad write letter and save",
            "write resignation letter in notepad",
            "draft something in notepad",
        ],
        "params": ["content_request", "filename"],
        "steps": [
            {
                "type":        "generate_content",
                "prompt":      "{content_request}",
                "param_name":  "generated_content",
                "max_tokens":  2048,
                "temperature": 0.7,
                "label":       "AI writes content"
            },
            {"type": "win_search", "query": "Notepad",              "label": "Search Notepad"},
            {"type": "delay",      "seconds": 1.5,                   "label": "Wait"},
            {"type": "press",      "key": "enter",                    "label": "Open Notepad"},
            {"type": "delay",      "seconds": 2.0,                    "label": "Wait for Notepad"},
            {"type": "type_clip",  "text": "{generated_content}",     "label": "Paste AI content"},
            {"type": "hotkey",     "keys": ["ctrl", "s"],             "label": "Save"},
            {"type": "delay",      "seconds": 1.0,                    "label": "Wait for dialog"},
            {"type": "hotkey",     "keys": ["ctrl", "a"],             "label": "Select filename"},
            {"type": "type_clip",  "text": "{filename}",              "label": "Type filename"},
            {"type": "press",      "key": "enter",                     "label": "Save"},
        ]
    },

    "write_email_draft_word": {
        "tier": "gui",
        "description": "AI writes a professional email draft, opens Word and pastes it",
        "examples": [
            "write an email to my manager about leave in word",
            "compose email to professor about assignment",
            "draft an email to HR about salary",
            "write email to boss about project delay in word",
        ],
        "params": ["content_request", "filename"],
        "steps": [
            {
                "type":        "generate_content",
                "prompt":      "{content_request}",
                "param_name":  "generated_content",
                "max_tokens":  1024,
                "temperature": 0.6,
                "label":       "AI composes the email"
            },
            {"type": "win_search", "query": "Microsoft Word",          "label": "Search Word"},
            {"type": "delay",      "seconds": 1.5,                     "label": "Wait for search"},
            {"type": "press",      "key": "enter",                      "label": "Open Word"},
            {"type": "delay",      "seconds": 5.0,                      "label": "Wait for Word to fully load"},
            {"type": "press",      "key": "escape",                     "label": "Dismiss Start Screen"},
            {"type": "delay",      "seconds": 0.8,                      "label": "Wait"},
            {"type": "press",      "key": "escape",                     "label": "Dismiss any dialog"},
            {"type": "delay",      "seconds": 0.5,                      "label": "Wait"},
            {"type": "hotkey",     "keys": ["ctrl", "home"],            "label": "Focus document body (Ctrl+Home)"},
            {"type": "delay",      "seconds": 0.5,                      "label": "Wait"},
            {"type": "type_clip",  "text": "{generated_content}",       "label": "Paste AI email"},
            {"type": "delay",      "seconds": 0.5,                      "label": "Wait"},
            {"type": "press",      "key": "f12",                        "label": "Open Save As dialog (F12)"},
            {"type": "delay",      "seconds": 2.0,                      "label": "Wait for Save dialog"},
            {"type": "hotkey",     "keys": ["ctrl", "a"],               "label": "Select filename field"},
            {"type": "type_clip",  "text": "{filename}",              "label": "Type filename"},
            {"type": "press",      "key": "enter",                     "label": "Save"},
        ]
    },

    "write_essay_word": {
        "tier": "gui",
        "description": "AI writes an essay or report, opens Word and saves it",
        "examples": [
            "write an essay on climate change in word",
            "write a report about AI in word",
            "compose an essay on technology in word",
            "write a 500 word essay in word",
            "write a short essay about friendship",
        ],
        "params": ["content_request", "filename"],
        "steps": [
            {
                "type":        "generate_content",
                "prompt":      "{content_request}",
                "param_name":  "generated_content",
                "max_tokens":  3000,
                "temperature": 0.8,
                "label":       "AI writes the essay"
            },
            {"type": "win_search", "query": "Microsoft Word",          "label": "Search Word"},
            {"type": "delay",      "seconds": 1.5,                     "label": "Wait for search"},
            {"type": "press",      "key": "enter",                      "label": "Open Word"},
            {"type": "delay",      "seconds": 5.0,                      "label": "Wait for Word to fully load"},
            {"type": "press",      "key": "escape",                     "label": "Dismiss Start Screen"},
            {"type": "delay",      "seconds": 0.8,                      "label": "Wait"},
            {"type": "press",      "key": "escape",                     "label": "Dismiss any dialog"},
            {"type": "delay",      "seconds": 0.5,                      "label": "Wait"},
            {"type": "hotkey",     "keys": ["ctrl", "home"],            "label": "Focus document body (Ctrl+Home)"},
            {"type": "delay",      "seconds": 0.5,                      "label": "Wait"},
            {"type": "type_clip",  "text": "{generated_content}",       "label": "Paste AI essay"},
            {"type": "delay",      "seconds": 0.5,                      "label": "Wait"},
            {"type": "press",      "key": "f12",                        "label": "Open Save As dialog (F12)"},
            {"type": "delay",      "seconds": 2.0,                      "label": "Wait for Save dialog"},
            {"type": "hotkey",     "keys": ["ctrl", "a"],               "label": "Select filename field"},
            {"type": "type_clip",  "text": "{filename}",                "label": "Type filename"},
            {"type": "press",      "key": "enter",                      "label": "Save"},
            {"type": "delay",      "seconds": 1.0,                      "label": "Wait for save to complete"},
        ]
    },

    "generate_save_text_file": {
        "tier": "gui",
        "description": "AI generates any content and saves it directly to a .txt file (no UI needed)",
        "examples": [
            "generate a letter and save to file",
            "create a document and write to disk",
            "ai write content and save to text file",
        ],
        "params": ["content_request", "filename"],
        "steps": [
            {
                "type":        "generate_content",
                "prompt":      "{content_request}",
                "param_name":  "generated_content",
                "max_tokens":  2048,
                "temperature": 0.7,
                "label":       "AI generates content"
            },
            {
                "type":    "write_file",
                "path":    "{filename}",
                "content": "{generated_content}",
                "label":   "Save directly to file"
            },
        ]
    },

    "write_code_in_vscode": {
        "tier": "gui",
        "description": "AI generates code, saves it to a file, then opens it in VS Code",
        "examples": [
            "write python code to sort a list in vscode",
            "generate a hello world program and open in vscode",
            "write a python script and open it in code",
            "create javascript code in vscode",
        ],
        "params": ["content_request", "filename"],
        "steps": [
            {
                "type":        "generate_content",
                "prompt":      "{content_request}",
                "param_name":  "generated_content",
                "max_tokens":  2048,
                "temperature": 0.3,
                "label":       "AI writes the code"
            },
            {
                "type":    "write_file",
                "path":    "{filename}",
                "content": "{generated_content}",
                "label":   "Save code to file"
            },
            {"type": "delay",  "seconds": 0.5,                                  "label": "Wait"},
            {"type": "cmd",    "command": "code {filename}",
             "capture_output": False,                                             "label": "Open in VS Code"},
            {"type": "delay",  "seconds": 3.0,                                   "label": "Wait for VS Code"},
        ]
    },

    "write_speech_word": {
        "tier": "gui",
        "description": "AI writes a speech or presentation script, opens Word and saves",
        "examples": [
            "write a speech for graduation ceremony in word",
            "write a farewell speech for my teacher",
            "draft a speech about independence day in word",
        ],
        "params": ["content_request", "filename"],
        "steps": [
            {
                "type":        "generate_content",
                "prompt":      "{content_request}",
                "param_name":  "generated_content",
                "max_tokens":  2048,
                "temperature": 0.8,
                "label":       "AI writes the speech"
            },
            {"type": "win_search", "query": "Microsoft Word",          "label": "Search Word"},
            {"type": "delay",      "seconds": 1.5,                     "label": "Wait for search"},
            {"type": "press",      "key": "enter",                      "label": "Open Word"},
            {"type": "delay",      "seconds": 5.0,                      "label": "Wait for Word to fully load"},
            {"type": "press",      "key": "escape",                     "label": "Dismiss Start Screen"},
            {"type": "delay",      "seconds": 0.8,                      "label": "Wait"},
            {"type": "press",      "key": "escape",                     "label": "Dismiss any dialog"},
            {"type": "delay",      "seconds": 0.5,                      "label": "Wait"},
            {"type": "hotkey",     "keys": ["ctrl", "home"],            "label": "Focus document body (Ctrl+Home)"},
            {"type": "delay",      "seconds": 0.5,                      "label": "Wait"},
            {"type": "type_clip",  "text": "{generated_content}",       "label": "Paste speech"},
            {"type": "delay",      "seconds": 0.5,                      "label": "Wait"},
            {"type": "press",      "key": "f12",                        "label": "Open Save As dialog (F12)"},
            {"type": "delay",      "seconds": 2.0,                      "label": "Wait for Save dialog"},
            {"type": "hotkey",     "keys": ["ctrl", "a"],               "label": "Select filename field"},
            {"type": "type_clip",  "text": "{filename}",                "label": "Type filename"},
            {"type": "press",      "key": "enter",                      "label": "Save"},
            {"type": "delay",      "seconds": 1.0,                      "label": "Wait for save to complete"},
        ]
    },

    "write_todo_list_notepad": {
        "tier": "gui",
        "description": "AI generates a to-do list or plan, saves to Notepad",
        "examples": [
            "create a todo list for my project in notepad",
            "make a study plan for exams in notepad",
            "write a weekly schedule in notepad",
            "create a task list for my work",
        ],
        "params": ["content_request", "filename"],
        "steps": [
            {
                "type":        "generate_content",
                "prompt":      "{content_request}",
                "param_name":  "generated_content",
                "max_tokens":  1024,
                "temperature": 0.5,
                "label":       "AI generates the list/plan"
            },
            {"type": "win_search", "query": "Notepad",              "label": "Search Notepad"},
            {"type": "delay",      "seconds": 1.5,                   "label": "Wait"},
            {"type": "press",      "key": "enter",                    "label": "Open Notepad"},
            {"type": "delay",      "seconds": 2.0,                    "label": "Wait"},
            {"type": "type_clip",  "text": "{generated_content}",     "label": "Paste list"},
            {"type": "hotkey",     "keys": ["ctrl", "s"],             "label": "Save"},
            {"type": "delay",      "seconds": 1.0,                    "label": "Wait"},
            {"type": "hotkey",     "keys": ["ctrl", "a"],             "label": "Select filename"},
            {"type": "type_clip",  "text": "{filename}",              "label": "Type filename"},
            {"type": "press",      "key": "enter",                     "label": "Save"},
        ]
    }
}
