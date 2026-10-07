"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  SMART TASK ROUTER v4 — Hybrid: Python Rules + LLM Param Extraction         ║
╚══════════════════════════════════════════════════════════════════════════════╝

PROBLEM: gemma4:e2b (7B) returns empty responses when given a task list of
248 items — even the "compact" list is ~20,000 chars, which is too long.

SOLUTION — Hybrid two-phase approach:
  Phase 1: Python keyword rules → instant, 100% reliable classification
  Phase 2: LLM param extraction → tiny focused prompt per task family only
  Phase 3: LLM content generation → actual document/letter/essay writing
"""

from __future__ import annotations

import json
import logging
import re
import time
from typing import Optional

import ollama

from playbooks     import ALL_PLAYBOOKS, CMD_PLAYBOOKS, KEYBOARD_PLAYBOOKS
from gui_playbooks import GUI_PLAYBOOKS
from executor      import PlaybookRunner

logger = logging.getLogger("ComputerUseAgent.router")


def _has(t: str, *phrases: str) -> bool:
    """True only if a phrase appears as whole word(s). 'ping' will NOT match 'shopping'."""
    return any(re.search(r"\b" + re.escape(p) + r"\b", t) for p in phrases)


_QUESTION_RE = re.compile(r"^\s*(how|what|why|when|where|which|who|explain|tell me)\b")


def _is_question(t: str) -> bool:
    """'how to shutdown a pc' is a question, not a command."""
    return bool(_QUESTION_RE.match(t))


# ══════════════════════════════════════════════════════════════════════════════
#  PHASE 1: PYTHON KEYWORD RULES — No LLM, instant classification
# ══════════════════════════════════════════════════════════════════════════════

def _normalize(task: str) -> str:
    """Lowercase, strip punctuation for matching."""
    return re.sub(r"[^\w\s]", " ", task.lower()).strip()


def classify_by_rules(task: str) -> tuple[str, str, str]:
    """
    Returns (task_id, tier, confidence) using pure Python rules.
    Covers ~95% of everyday tasks instantly, no LLM needed.
    """
    t = _normalize(task)
    words = set(t.split())

    # ── AI CONTENT GENERATION (highest priority) ──────────────────────────
    # Must check BEFORE simpler "write/open" rules

    writing_verbs   = {"write", "compose", "draft", "create", "generate", "make"}
    has_writing     = bool(writing_verbs & words)
    has_letter      = any(w in t for w in ["letter", "application", "complaint", "resignation",
                                           "apology", "recommendation", "request", "proposal"])
    has_email       = any(w in t for w in ["email", "mail", "message"])
    has_essay       = any(w in t for w in ["essay", "report", "article", "paragraph", "thesis"])
    has_speech      = any(w in t for w in ["speech", "script", "presentation", "talk"])
    has_todo        = any(w in t for w in ["todo", "to-do", "plan", "schedule", "list", "tasks"])
    has_code        = any(w in t for w in ["code", "program", "script", "function", "class",
                                           "python", "javascript", "html", "java"])
    in_word         = any(w in t for w in ["word", "microsoft word", "docx"])
    in_notepad      = any(w in t for w in ["notepad", "txt", "text file"])
    in_vscode       = any(w in t for w in ["vscode", "vs code", "code editor", "visual studio"])

    if has_writing:
        if has_code and in_vscode:
            return "write_code_in_vscode",      "gui", "high"
        if has_code:
            return "write_code_in_vscode",      "gui", "medium"
        if has_speech:
            return "write_speech_word",         "gui", "high"
        if has_essay:
            return "write_essay_word",          "gui", "high"
        if has_email and in_word:
            return "write_email_draft_word",    "gui", "high"
        if has_todo and in_notepad:
            return "write_todo_list_notepad",   "gui", "high"
        if has_todo:
            return "write_todo_list_notepad",   "gui", "medium"
        if has_letter and in_notepad:
            return "write_document_notepad",    "gui", "high"
        if has_letter:
            return "write_document_word",       "gui", "high"  # default to Word for letters
        if in_notepad:
            return "write_document_notepad",    "gui", "medium"
        if in_word:
            return "write_document_word",       "gui", "medium"

    # ── BROWSER TASKS ─────────────────────────────────────────────────────
    if "youtube" in t:
        if any(w in t for w in ["search", "find", "look", "play"]):
            return "youtube_search",            "cmd",  "high"
    if "google" in t and any(w in t for w in ["search", "find", "look"]):
        return "google_search",                 "cmd",  "high"
    if "wikipedia" in t:
        return "wikipedia_search",              "cmd",  "high"
    if "github" in t and any(w in t for w in ["search", "open", "find"]):
        return "github_search",                 "cmd",  "high"
    if "stackoverflow" in t or "stack overflow" in t:
        return "stackoverflow_search",          "cmd",  "high"
    if "reddit" in t:
        return "reddit_search",                 "cmd",  "high"

    if any(w in t for w in ["incognito", "private window", "private browsing"]):
        return "browser_open_incognito",        "gui",  "high"
    if any(w in t for w in ["bookmark", "add to bookmarks"]):
        return "browser_bookmark_current",      "gui",  "high"
    if any(w in t for w in ["browser history", "browsing history", "view history"]):
        return "browser_open_history",          "gui",  "high"
    if any(w in t for w in ["browser downloads", "view downloads", "open downloads"]):
        return "browser_open_downloads",        "gui",  "high"
    if "print" in t and any(w in t for w in ["page", "tab"]):
        return "browser_print_page",            "gui",  "high"
    if any(w in t for w in ["reader mode", "reading mode", "reading view"]):
        return "browser_reader_mode",           "gui",  "high"
    if any(w in t for w in ["find on page", "find in page", "search in page"]):
        return "browser_find_on_page",          "gui",  "high"
    if any(w in t for w in ["new tab"]) and any(w in t for w in ["search", "open"]):
        return "browser_new_tab_and_search",    "gui",  "high"
    if any(w in t for w in ["scroll to top", "go to top"]):
        return "browser_scroll_to_top",         "keyboard", "high"
    if any(w in t for w in ["scroll to bottom", "go to bottom"]):
        return "browser_scroll_to_bottom",      "keyboard", "high"

    # ── SCREENSHOTS ───────────────────────────────────────────────────────
    if any(w in t for w in ["screenshot", "screen capture", "screen shot"]):
        if any(w in t for w in ["paint", "annotate", "draw"]):
            return "screenshot_then_paint",     "gui",  "high"
        if any(w in t for w in ["region", "area", "part", "snip", "crop"]):
            return "screenshot_region",         "gui",  "high"
        if any(w in t for w in ["window only", "active window"]):
            return "screenshot_active_window",  "gui",  "high"
        if any(w in t for w in ["save", "auto"]):
            return "screenshot_full_screen_save", "gui", "high"
        return "take_screenshot",               "cmd",  "high"
    if "snipping tool" in t:
        return "screenshot_open_snipping_tool", "gui",  "high"
    if "snip" in t and any(w in t for w in ["sketch", "annotate"]):
        return "open_snip_sketch_and_annotate", "gui",  "high"

    # ── NOTEPAD TASKS ─────────────────────────────────────────────────────
    if "notepad" in t:
        if any(w in t for w in ["find", "replace"]):
            return "notepad_find_and_replace",  "gui",  "high"
        if any(w in t for w in ["type", "write", "add"]) and any(w in t for w in ["save"]):
            return "notepad_full_workflow",     "gui",  "high"
        if any(w in t for w in ["type", "write", "add"]):
            return "notepad_open_and_type_only","gui",  "high"
        if any(w in t for w in ["select all", "copy all"]):
            return "notepad_select_all_copy",   "gui",  "high"
        return "open_notepad",                  "cmd",  "high"

    # ── CALCULATOR ────────────────────────────────────────────────────────
    if _has(t, "calculator", "calculate", "calculating", "compute", "computation"):
        if any(w in t for w in ["scientific"]):
            return "calculator_scientific_mode","gui",  "high"
        if any(w in t for w in ["currency", "convert"]):
            return "calculator_currency_converter", "gui", "high"
        return "calculator_compute",            "gui",  "high"

    # ── SYSTEM SETTINGS ───────────────────────────────────────────────────
    if any(w in t for w in ["wallpaper", "background", "desktop background"]):
        return "settings_change_wallpaper",     "gui",  "high"
    if any(w in t for w in ["brightness", "screen brightness"]):
        return "adjust_brightness_search",      "gui",  "high"
    if any(w in t for w in ["dark mode", "light mode", "night mode"]):
        return "settings_dark_mode",            "gui",  "high"
    if any(w in t for w in ["night light", "blue light"]):
        return "settings_night_light",          "gui",  "high"
    if any(w in t for w in ["wifi", "wi-fi", "wireless network"]):
        return "settings_wifi",                 "gui",  "high"
    if "bluetooth" in t:
        return "settings_bluetooth",            "gui",  "high"
    if any(w in t for w in ["sound settings", "audio settings", "speaker settings"]):
        return "settings_sound",                "gui",  "high"
    if any(w in t for w in ["display settings", "resolution", "screen resolution"]):
        return "settings_display",              "gui",  "high"
    if any(w in t for w in ["default apps", "default browser", "default applications"]):
        return "settings_default_apps",         "gui",  "high"
    if any(w in t for w in ["language settings", "language region"]):
        return "settings_language",             "gui",  "high"
    if any(w in t for w in ["power settings", "sleep settings", "screen timeout"]):
        return "settings_power_sleep",          "gui",  "high"
    if any(w in t for w in ["storage settings", "disk usage", "free space"]):
        return "settings_storage",              "gui",  "high"
    if any(w in t for w in ["focus assist", "do not disturb", "dnd"]):
        return "settings_focus_assist",         "gui",  "high"
    if any(w in t for w in ["accessibility", "ease of access"]):
        return "settings_accessibility",        "gui",  "high"
    if any(w in t for w in ["mouse settings", "pointer speed"]):
        return "settings_mouse",                "gui",  "high"

    # ── MEDIA ─────────────────────────────────────────────────────────────
    if any(w in t for w in ["play pause", "pause music", "play music", "toggle music"]):
        return "media_play_pause",              "gui",  "high"
    if any(w in t for w in ["next song", "next track", "skip track", "skip song"]):
        return "media_next_track",              "gui",  "high"
    if any(w in t for w in ["previous song", "previous track", "last song", "go back song"]):
        return "media_previous_track",          "gui",  "high"
    if any(w in t for w in ["stop music", "stop media"]):
        return "media_stop",                    "gui",  "high"

    # ── WINDOW MANAGEMENT ─────────────────────────────────────────────────
    if any(w in t for w in ["show desktop", "minimize all"]):
        return "show_desktop",                  "keyboard", "high"
    if any(w in t for w in ["maximize window", "maximize this"]):
        return "maximize_window",               "keyboard", "high"
    if any(w in t for w in ["minimize window", "minimize this", "hide window"]):
        return "window_minimize_current",       "gui",  "high"
    if any(w in t for w in ["close window", "close this", "exit app"]):
        return "close_window",                  "keyboard", "high"
    if any(w in t for w in ["snap left", "window left", "move window left"]):
        return "snap_window_left",              "keyboard", "high"
    if any(w in t for w in ["snap right", "window right", "move window right"]):
        return "snap_window_right",             "keyboard", "high"
    if any(w in t for w in ["split screen", "side by side", "two windows"]):
        return "window_split_side_by_side",     "gui",  "high"
    if any(w in t for w in ["switch window", "alt tab", "previous window"]):
        return "switch_to_window_by_app",       "gui",  "high"
    if any(w in t for w in ["other monitor", "second screen", "next monitor"]):
        return "window_move_to_next_monitor",   "gui",  "high"
    if "fullscreen" in t or "full screen" in t:
        return "open_app_fullscreen",           "gui",  "high"

    # ── CLIPBOARD & QUICK ACTIONS ─────────────────────────────────────────
    if any(w in t for w in ["clipboard history", "win v", "paste history"]):
        return "clipboard_history",             "gui",  "high"
    if any(w in t for w in ["emoji", "emoji picker", "insert emoji"]):
        return "emoji_picker",                  "gui",  "high"
    if any(w in t for w in ["run dialog", "run command", "win r"]):
        return "open_run_and_execute",          "gui",  "high"

    # ── TASK MANAGER ──────────────────────────────────────────────────────
    if any(w in t for w in ["task manager", "force close", "kill app", "end task", "end process"]):
        return "task_manager_open",             "gui",  "high"

    # ── KEYBOARD SHORTCUTS ────────────────────────────────────────────────
    if any(w in t for w in ["save file", "ctrl s", "save the file"]):
        return "save_file",                     "keyboard", "high"
    if any(w in t for w in ["new tab", "open tab"]):
        return "browser_new_tab",               "keyboard", "high"
    if any(w in t for w in ["close tab", "ctrl w"]):
        return "browser_close_tab",             "keyboard", "high"
    if any(w in t for w in ["volume up", "increase volume", "louder"]):
        return "volume_up",                     "keyboard", "high"
    if any(w in t for w in ["volume down", "decrease volume", "quieter"]):
        return "volume_down",                   "keyboard", "high"
    if any(w in t for w in ["mute", "unmute"]):
        return "mute_volume",                   "keyboard", "high"
    if any(w in t for w in ["undo", "ctrl z"]):
        return "undo",                          "keyboard", "high"
    if any(w in t for w in ["redo", "ctrl y"]):
        return "redo",                          "keyboard", "high"
    if any(w in t for w in ["copy all", "select all", "ctrl a"]):
        return "select_all",                    "keyboard", "high"
    if any(w in t for w in ["zoom in", "increase zoom"]):
        return "zoom_in",                       "keyboard", "high"
    if any(w in t for w in ["zoom out", "decrease zoom"]):
        return "zoom_out",                      "keyboard", "high"
    if any(w in t for w in ["lock screen", "lock computer", "lock pc"]):
        return "lock_screen",                   "keyboard", "high"
    if any(w in t for w in ["virtual desktop", "task view", "new desktop"]):
        return "virtual_desktop_new",           "keyboard", "high"

    # ── STICKY NOTES & CALENDAR ───────────────────────────────────────────
    if any(w in t for w in ["sticky note", "sticky notes"]):
        if any(w in t for w in ["type", "write", "with text"]):
            return "sticky_notes_type",         "gui",  "high"
        return "sticky_notes_new",              "gui",  "high"
    if any(w in t for w in ["calendar", "my calendar"]):
        if any(w in t for w in ["event", "appointment", "add", "new", "create"]):
            return "calendar_new_event",        "gui",  "high"
        return "calendar_open",                 "gui",  "high"

    # ── CLOCK / TIMER / ALARM ─────────────────────────────────────────────
    if any(w in t for w in ["timer"]):
        return "clock_open_timer_tab",          "gui",  "high"
    if any(w in t for w in ["alarm", "set alarm"]):
        return "clock_open_alarm_tab",          "gui",  "high"
    if any(w in t for w in ["stopwatch"]):
        return "clock_open_stopwatch",          "gui",  "high"
    if any(w in t for w in ["clock"]):
        return "clock_open",                    "gui",  "high"

    # ── OFFICE APPS ───────────────────────────────────────────────────────
    if any(w in t for w in ["microsoft word", "open word", "launch word"]):
        if any(w in t for w in ["type", "write"]):
            return "word_open_and_type",        "gui",  "high"
        return "word_open_and_type",            "gui",  "medium"
    if any(w in t for w in ["excel", "spreadsheet"]):
        if any(w in t for w in ["type", "enter data", "open existing"]):
            return "excel_open_and_type",       "gui",  "high"
        return "excel_open_and_type",           "gui",  "medium"
    if any(w in t for w in ["powerpoint", "ppt", "presentation"]):
        if any(w in t for w in ["new slide", "add slide"]):
            return "powerpoint_add_slide",      "gui",  "high"
        return "powerpoint_new_presentation",   "gui",  "high"
    if any(w in t for w in ["onenote", "one note"]):
        return "open_onenote",                  "gui",  "high"

    # ── COMMUNICATION APPS ────────────────────────────────────────────────
    if "outlook" in t:
        return "open_outlook_compose",          "gui",  "high"
    if any(w in t for w in ["teams", "microsoft teams", "ms teams"]):
        return "open_teams",                    "gui",  "high"
    if "whatsapp" in t:
        return "open_whatsapp",                 "gui",  "high"
    if "zoom" in t:
        return "open_zoom_new_meeting",         "gui",  "high"
    if "discord" in t:
        return "open_discord",                  "gui",  "high"
    if "slack" in t:
        return "open_any_app_search",           "gui",  "medium"
    if "telegram" in t:
        return "open_any_app_search",           "gui",  "medium"
    if "skype" in t:
        return "open_any_app_search",           "gui",  "medium"

    # ── FILE EXPLORER ─────────────────────────────────────────────────────
    if any(w in t for w in ["file explorer", "explorer", "my files", "file manager"]):
        if any(w in t for w in ["create folder", "new folder", "make folder"]):
            return "explorer_create_folder",    "gui",  "high"
        if any(w in t for w in ["rename", "change name"]):
            return "explorer_rename_file",      "gui",  "high"
        if any(w in t for w in ["search", "find file"]):
            return "explorer_search_files",     "gui",  "high"
        if any(w in t for w in ["delete", "remove"]):
            return "explorer_delete_selected",  "gui",  "high"
        if any(w in t for w in ["navigate", "go to", "open path"]):
            return "explorer_go_to_path",       "gui",  "high"
        if any(w in t for w in ["select all"]):
            return "explorer_select_all",       "gui",  "high"
        if any(w in t for w in ["copy"]):
            return "explorer_copy_selected",    "gui",  "high"
        if any(w in t for w in ["paste"]):
            return "explorer_paste_here",       "gui",  "high"
        if any(w in t for w in ["properties"]):
            return "explorer_open_properties",  "gui",  "high"
        if any(w in t for w in ["zip", "compress", "archive"]):
            return "explorer_zip_selected",     "gui",  "high"
    if any(w in t for w in ["create folder", "new folder", "make folder"]):
        return "explorer_create_folder",        "gui",  "high"
    if any(w in t for w in ["rename file", "rename folder", "rename selected"]):
        return "explorer_rename_file",          "gui",  "high"

    # ── SYSTEM COMMANDS ───────────────────────────────────────────────────
    if any(w in t for w in ["ip address", "my ip", "ipconfig"]):
        return "show_ip_address",               "cmd",  "high"
    if _has(t, "ping", "check connection", "network test"):
        return "ping_host",                     "cmd",  "high"
    if any(w in t for w in ["disk space", "drive space", "free space"]):
        return "show_disk_usage",               "cmd",  "high"
    if any(w in t for w in ["cpu usage", "memory usage", "ram usage"]):
        return "show_system_info",              "cmd",  "high"
    if any(w in t for w in ["running processes", "process list", "tasklist"]):
        return "list_running_processes",        "cmd",  "high"
    if any(w in t for w in ["current directory", "pwd", "where am i"]):
        return "show_current_directory",        "cmd",  "high"
    if any(w in t for w in ["list files", "ls ", "dir "]):
        return "list_directory_contents",       "cmd",  "high"
    if any(w in t for w in ["system info", "computer info", "pc info"]):
        return "show_system_info",              "cmd",  "high"
    if any(w in t for w in ["date and time", "current time", "what time", "what date"]):
        return "show_date_time",                "cmd",  "high"
    if not _is_question(t) and _has(t, "restart", "reboot"):
        return "restart_computer",              "cmd",  "high"
    if not _is_question(t) and _has(t, "shutdown", "shut down", "turn off"):
        return "shutdown_computer",             "cmd",  "high"
    if not _is_question(t) and _has(t, "sleep", "hibernate"):
        return "sleep_computer",                "cmd",  "high"
    if any(w in t for w in ["clear clipboard", "clear clip"]):
        return "clear_clipboard",               "cmd",  "high"
    if any(w in t for w in ["type text", "paste text", "type this"]):
        return "paste_text_to_focused",         "gui",  "high"

    # ── GENERIC APP OPEN (last resort before unknown) ─────────────────────
    open_words = {"open", "launch", "start", "run", "open up"}
    if open_words & words:
        # Extract what they want to open
        for word in ["open", "launch", "start", "run"]:
            if f"{word} " in t:
                app = t.split(f"{word} ", 1)[1].strip()
                # Known special apps
                if any(w in app for w in ["vlc", "media player"]):
                    return "open_vlc_play_file", "gui", "medium"
                if any(w in app for w in ["spotify", "music"]):
                    return "open_any_app_search", "gui", "high"
                if "github desktop" in app:
                    return "open_github_desktop", "gui", "high"
                if "chrome" in app or "edge" in app or "firefox" in app:
                    return "browser_search_and_navigate", "gui", "medium"
                # Generic app
                if len(app) > 1:
                    return "open_any_app_search", "gui", "medium"

    # ── NO MATCH ──────────────────────────────────────────────────────────
    return "unknown", "vision", "low"

# =============================================================================
#  PHASE 2: INSTANT PYTHON PARAM EXTRACTION  (zero LLM, < 1ms total)
#
#  LLM is ONLY called by executor.py for the "generate_content" step.
#  Routing itself is now completely instant — no model warmup, no latency.
# =============================================================================

# Default filenames for AI writing tasks
AI_DEFAULT_FILENAMES = {
    "write_document_word":     "document.docx",
    "write_document_notepad":  "document.txt",
    "write_email_draft_word":  "email_draft.docx",
    "write_essay_word":        "essay.docx",
    "write_speech_word":       "speech.docx",
    "write_todo_list_notepad": "todo_list.txt",
    "write_code_in_vscode":    "script.py",
    "generate_save_text_file": "output.txt",
}

_STRIP_PHRASES = [
    "open word and", "open notepad and", "open vscode and",
    "in microsoft word", "in word", "in notepad", "in vscode", "in vs code",
    "in a word document", "in a text file",
    "write a ", "write an ", "compose a ", "compose an ",
    "draft a ", "draft an ", "create a ", "create an ",
    "generate a ", "generate an ", "make a ", "make an ",
]

_CONTENT_PREFIXES = {
    "write_document_word": (
        "Write a formal, professionally structured document. "
        "Include: date at top, proper salutation, clear body paragraphs, "
        "and a formal closing with signature placeholder. "
        "Leave blank lines between sections. Document topic:"
    ),
    "write_document_notepad": (
        "Write a clear, well-structured plain-text document. "
        "Include a title, organized sections, and a conclusion. Topic:"
    ),
    "write_email_draft_word": (
        "Write a professional email. Include: Subject line, formal greeting, "
        "clear body stating purpose in first paragraph, action items, "
        "professional closing and signature. Email topic:"
    ),
    "write_essay_word": (
        "Write a well-structured academic essay. "
        "Include: introduction with thesis, 3-4 body paragraphs each with "
        "a clear point and supporting details, and a conclusion. Essay topic:"
    ),
    "write_speech_word": (
        "Write an engaging speech. Include: strong opening hook, "
        "3-4 main points with transitions, relevant examples, "
        "and a memorable closing. Speech topic:"
    ),
    "write_todo_list_notepad": (
        "Create a detailed numbered to-do list or action plan. "
        "Group related items. Include time estimates where relevant. Plan for:"
    ),
    "write_code_in_vscode": (
        "Write complete, working, well-commented code. "
        "Include imports, proper structure, error handling, and a usage example. Code task:"
    ),
    "generate_save_text_file": (
        "Write a complete, well-formatted document with clear headings. Content:"
    ),
}


def _extract_core(task: str) -> str:
    result = task.lower()
    for phrase in _STRIP_PHRASES:
        result = result.replace(phrase, " ")
    result = re.sub(r"\s+", " ", result).strip()
    result = re.sub(r"^(a |an |the )", "", result).strip()
    return result or task


def _smart_filename(task: str, ext: str) -> str:
    core = _extract_core(task)
    stop = {"for","and","the","about","with","from","that","this",
            "your","our","its","their","some","into","over","my","me"}
    words = [w for w in core.split() if len(w) > 2 and w not in stop]
    name = "_".join(words[:5]) if words else "document"
    name = re.sub(r"[^\w_]", "", name)
    return f"{name}.{ext}" if name else f"document.{ext}"


def extract_params_instant(task_id: str, user_task: str) -> dict:
    """Pure Python extraction — zero LLM, completes in < 1ms."""
    t    = user_task.strip()
    tl   = t.lower()
    core = _extract_core(t)

    # AI content writing
    if task_id in AI_DEFAULT_FILENAMES:
        ext    = AI_DEFAULT_FILENAMES[task_id].rsplit(".", 1)[-1]
        prefix = _CONTENT_PREFIXES.get(task_id, "Write content about:")
        content_request = (
            f"{prefix} {core}. "
            "Use formal, professional language with proper structure. "
            "Format with blank lines between sections. "
            "Make it complete and immediately usable."
        )
        return {"content_request": content_request, "filename": _smart_filename(t, ext)}

    # Search queries
    if task_id in (
        "google_search", "youtube_search", "wikipedia_search",
        "github_search", "reddit_search", "stackoverflow_search",
        "browser_find_on_page", "browser_new_tab_and_search",
        "browser_search_in_current", "browser_open_youtube_search",
        "explorer_search_files", "type_in_search_bar",
        "browser_zoom_in_then_navigate"
    ):
        for pat in [
            r"(?:search\s+(?:\w+\s+)?for|find|look\s+up|look\s+for)\s+(.+)",
            r"(?:find on page|find in page)[:\s]+(.+)"
        ]:
            m = re.search(pat, tl)
            if m:
                return {"query": m.group(1).strip()}
        return {"query": core}

    # Open app
    if task_id in (
        "open_any_app_search", "open_app_fullscreen",
        "open_app_snap_left", "open_app_snap_right",
        "window_always_on_top_toggle", "switch_to_window_by_app"
    ):
        m = re.search(r"(?:open|launch|start|run|switch\s+to)\s+(.+)", tl)
        app = m.group(1).strip() if m else core
        for noise in ["and type", "and write", "fullscreen", "snap left", "snap right"]:
            app = app.replace(noise, "").strip()
        return {"app_name": app}

    # Split screen
    if task_id == "window_split_side_by_side":
        m = re.search(r"split\s+(.+?)\s+and\s+(.+)", tl)
        if m:
            return {"app1": m.group(1).strip(), "app2": m.group(2).strip()}
        parts = core.split(" and ")
        return {"app1": parts[0].strip(), "app2": parts[1].strip() if len(parts) > 1 else ""}

    # Text to type
    if task_id in ("paste_text_to_focused", "notepad_open_and_type_only", "word_open_and_type"):
        m = re.search(r"(?:type|write|paste|add)\s+(.+?)(?:\s+and\s+save|\s+to\s+|$)", tl)
        return {"text": m.group(1).strip() if m else core}

    # Sticky note
    if task_id == "sticky_notes_type":
        m = re.search(r"(?:write|add|type|with text)\s+(.+)", tl)
        return {"note_text": m.group(1).strip() if m else core}

    # Notepad full workflow
    if task_id == "notepad_full_workflow":
        text_m = re.search(r"(?:type|write|add)\s+(.+?)(?:\s+and\s+save|\s+save|$)", tl)
        file_m = re.search(r"(?:save as|save to|filename)[:\s]+([^\s]+\.txt)", tl)
        text     = text_m.group(1).strip() if text_m else core
        filename = file_m.group(1).strip() if file_m else _smart_filename(t, "txt")
        return {"text": text, "filename": filename}

    # Find & replace
    if task_id == "notepad_find_and_replace":
        m = re.search(
            r"find\s+['\"]?(.+?)['\"]?\s+(?:and\s+)?replace\s+(?:with\s+)?['\"]?(.+?)['\"]?$",
            tl
        )
        if m:
            return {"find_text": m.group(1).strip(), "replace_text": m.group(2).strip()}
        return {"find_text": "", "replace_text": ""}

    # Calculator
    if task_id == "calculator_compute":
        m = re.search(r"(?:compute|calculate|eval(?:uate)?|do|solve)\s+(.+)", tl)
        expr = m.group(1).strip() if m else core
        # Extract just the math characters if there's still text
        m_math = re.search(r"([0-9\+\-\*\/\(\)\.\^x]+)", expr)
        if m_math:
            expr = m_math.group(1).strip()
        # Replace 'x' with '*' for multiplication
        expr = expr.replace("x", "*")
        return {"expression": expr}

    # Explorer create folder
    if task_id == "explorer_create_folder":
        name_m = re.search(r"(?:called|named|name)[:\s]+([^\s]+)", tl)
        path_m = re.search(r"(?:in|at|under)\s+([C-Zc-z]:[/\\].+)", t)
        return {
            "folder_name": name_m.group(1).strip() if name_m else "New Folder",
            "folderpath":  path_m.group(1).strip() if path_m else ".",
        }

    if task_id == "explorer_rename_file":
        m = re.search(r"(?:rename|to|as)\s+['\"]?([^'\"]+)['\"]?$", tl)
        return {"new_name": m.group(1).strip() if m else "new_name"}

    if task_id == "explorer_go_to_path":
        m = re.search(r"(?:go to|navigate to|open|path)[:\s]+([C-Zc-z]:[/\\].+)", t)
        return {"folderpath": m.group(1).strip() if m else "."}

    # Calendar event
    if task_id == "calendar_new_event":
        m = re.search(r"(?:event|appointment|meeting|add|new|create)\s+(?:called\s+|named\s+)?(.+)", tl)
        return {"event_title": m.group(1).strip() if m else core}

    # Run dialog
    if task_id == "open_run_and_execute":
        m = re.search(r"(?:run|execute|open)\s+(.+)", tl)
        cmd = m.group(1).strip() if m else ""
        for noise in ["run dialog", "dialog", "the "]:
            cmd = cmd.replace(noise, "").strip()
        return {"command": cmd}

    # Ping
    if task_id == "ping_host":
        m = re.search(r"ping\s+([^\s]+)", tl)
        return {"host": m.group(1).strip() if m else "google.com"}

    # Word heading
    if task_id == "word_insert_heading":
        m = re.search(r"(?:heading|title)[:\s]+(.+)", tl)
        return {"heading_text": m.group(1).strip() if m else core}

    # Excel
    if task_id == "excel_open_and_type":
        m = re.search(r"(?:type|enter|add|input)\s+(.+)", tl)
        return {"content": m.group(1).strip() if m else core}

    # VLC
    if task_id == "open_vlc_play_file":
        m = re.search(r"(?:play|open|file)[:\s]+([C-Zc-z]:[/\\].+\.\w+)", t)
        return {"filepath": m.group(1).strip() if m else ""}

    # Browser URL
    if task_id in ("browser_search_and_navigate", "browser_go_to_address"):
        m = re.search(r"(https?://[^\s]+)", tl)
        url = m.group(1) if m else f"https://www.google.com/search?q={core.replace(' ', '+')}"
        return {"browser": "Chrome", "url": url}

    return {}


# =============================================================================
#  TASK ROUTER — fully instant, no LLM during routing
# =============================================================================

class TaskRouter:
    """
    Phase 1 : Python keyword rules   -> task_id + tier   (< 1ms)
    Phase 2 : Python regex extraction -> params           (< 1ms)
    Total routing time: < 5ms regardless of hardware.
    """

    def __init__(self, model: str, ollama_host: str = "http://localhost:11434") -> None:
        self.model  = model
        self.client = ollama.Client(host=ollama_host)

    def route(self, task: str) -> dict:
        task_id, tier, confidence = classify_by_rules(task)
        params = extract_params_instant(task_id, task) if task_id != "unknown" else {}
        if task_id in AI_DEFAULT_FILENAMES and "filename" not in params:
            params["filename"] = AI_DEFAULT_FILENAMES[task_id]
        return {
            "task_id":    task_id,
            "tier":       tier,
            "confidence": confidence,
            "params":     params,
            "reason":     f"Matched by rules: {task_id}",
        }


# =============================================================================
#  SMART AGENT
# =============================================================================

class SmartAgent:
    """Dispatcher: rules classify -> regex extracts params -> executor runs steps."""

    def __init__(self, model: str, ollama_host: str = "http://localhost:11434") -> None:
        self.router = TaskRouter(model, ollama_host)
        self.runner = PlaybookRunner(model=model, ollama_host=ollama_host)

    def run(self, task: str) -> dict:
        print(f"\n  Routing: '{task[:80]}'")
        route = self.router.route(task)

        task_id    = route.get("task_id",    "unknown")
        tier       = route.get("tier",       "vision")
        confidence = route.get("confidence", "low")
        params     = route.get("params",     {})

        tier_icon = {"cmd": "[CMD]", "keyboard": "[KB]",
                     "gui": "[GUI]", "vision": "[VISION]"}.get(tier, "[?]")
        print(f"  {tier_icon} {task_id}  ({confidence})")
        for k, v in params.items():
            v_str = str(v)[:100] + ("..." if len(str(v)) > 100 else "")
            print(f"    {k}: {v_str}")

        playbook = GUI_PLAYBOOKS.get(task_id) or ALL_PLAYBOOKS.get(task_id)

        if playbook and confidence in ("high", "medium"):
            print(f"\n  Running {len(playbook['steps'])} steps...")
            results = self.runner.run(playbook, params)
            return {
                "mode": "playbook", "task_id": task_id, "tier": tier,
                "confidence": confidence, "params": params, "results": results,
                "reason": route.get("reason", ""),
            }

        print(f"\n  No playbook match.")
        return {
            "mode": "vision_fallback", "task_id": task_id, "tier": tier,
            "confidence": confidence, "params": params, "results": [],
            "reason": route.get("reason", ""),
        }