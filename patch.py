"""Replace Phase 2 LLM extraction with instant Python regex in router.py."""
import ast, re

src = open("router.py", encoding="utf-8").read()

# Find split point — where Phase 2 starts
lines = src.splitlines(keepends=True)
split_line = None
for i, l in enumerate(lines):
    if "PHASE 2" in l and ("LLM" in l or "PARAM" in l):
        # Go back to find the === comment line above it
        for j in range(i-1, max(i-4, 0), -1):
            if "═" in lines[j] or "=" * 20 in lines[j]:
                split_line = j
                break
        if split_line is None:
            split_line = i
        break

print(f"Splitting at line {split_line+1}")
phase1 = "".join(lines[:split_line]).rstrip() + "\n\n"

phase2_new = r'''# =============================================================================
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
        m = re.search(r"(?:compute|calculate|eval(?:uate)?)\s+(.+)", tl)
        return {"expression": m.group(1).strip() if m else core}

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
'''

new_src = phase1 + phase2_new

try:
    ast.parse(new_src)
    print("Syntax OK")
except SyntaxError as e:
    lines_new = new_src.splitlines()
    ln = (e.lineno or 1) - 1
    print(f"Syntax ERROR at line {e.lineno}: {e.msg}")
    for i in range(max(0, ln-2), min(len(lines_new), ln+3)):
        print(f"  {i+1}: {lines_new[i]}")
    exit(1)

open("router.py", "w", encoding="utf-8").write(new_src)
total_lines = new_src.count("\n")
print(f"router.py written — {total_lines} lines")

# Quick import test
import importlib, sys
if "router" in sys.modules:
    del sys.modules["router"]
import router
importlib.reload(router)

# Time the routing
import time
start = time.perf_counter()
for task in [
    "open word and write a letter to principal about resignation",
    "search youtube for python tutorial",
    "take a screenshot",
    "adjust brightness",
    "volume up",
]:
    r = router.TaskRouter.__new__(router.TaskRouter)
    result = router.classify_by_rules(task)
    params = router.extract_params_instant(result[0], task)

elapsed = (time.perf_counter() - start) * 1000
print(f"5 tasks routed in {elapsed:.2f}ms  ({elapsed/5:.2f}ms avg per task)")
print("Routing is now INSTANT (no LLM calls).")
