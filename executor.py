"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  UNIFIED STEP EXECUTOR v2 — Precise, Verified, Unicode-Safe Execution       ║
╚══════════════════════════════════════════════════════════════════════════════╝

Core fixes over the old executor:
  1. type_clip  → clipboard paste instead of typewrite() — handles ANY text
  2. win_search → Win+S + clipboard type → Enter (universal, reliable launcher)
  3. click_pct  → percentage-based coords (works on every resolution)
  4. verify     → mss screenshot + LLM check after important GUI steps
  5. All steps return detailed log strings for the dashboard
"""

from __future__ import annotations

import base64
import io
import json
import logging
import os
import re
import subprocess
import time
import urllib.parse
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger("ComputerUseAgent.executor")

# ── Optional imports (graceful fallback if not available) ────────────────────
try:
    import pyautogui
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.05
    SCREEN_W, SCREEN_H = pyautogui.size()
    logger.debug(f"pyautogui ready. Screen: {SCREEN_W}x{SCREEN_H}")
except ImportError:
    pyautogui = None  # type: ignore
    SCREEN_W, SCREEN_H = 1920, 1080

try:
    import pyperclip
    _CLIP_OK = True
except ImportError:
    _CLIP_OK = False
    logger.warning("pyperclip not found. Installing: pip install pyperclip")

try:
    import mss
    from PIL import Image
    _MSS_OK = True
except ImportError:
    mss = None  # type: ignore
    _MSS_OK = False

try:
    import ollama as _ollama_lib
    _OLLAMA_OK = True
except ImportError:
    _OLLAMA_OK = False


# ══════════════════════════════════════════════════════════════════════════════
#  STEP EXECUTOR
# ══════════════════════════════════════════════════════════════════════════════

class StepExecutor:
    """
    Executes individual playbook steps with full Unicode support, clipboard-
    based typing, and optional LLM verification after GUI actions.
    """

    def __init__(
        self,
        model: str = "gemma4:e2b",
        ollama_host: str = "http://localhost:11434",
    ) -> None:
        self.model       = model
        self.ollama_host = ollama_host
        self._ollama_client = None

        if _OLLAMA_OK:
            import ollama
            self._ollama_client = ollama.Client(host=ollama_host)

    # ─────────────────────────────────────────────────────────────────────────
    #  PUBLIC: run a single step dict
    # ─────────────────────────────────────────────────────────────────────────

    def run(self, step: dict, params: dict) -> str:
        """
        Dispatch a step to the right handler.
        Returns a human-readable result string for the dashboard.
        """
        t = step["type"]
        label = step.get("label", t)

        handlers = {
            "cmd":               self._cmd,
            "delay":             self._delay,
            "type_clip":         self._type_clip,
            "hotkey":            self._hotkey,
            "press":             self._press,
            "write_file":        self._write_file,
            "screenshot":        self._screenshot,
            "win_search":        self._win_search,
            "click_pct":         self._click_pct,
            "right_click_pct":   self._right_click_pct,
            "double_click_pct":  self._double_click_pct,
            "scroll_at":         self._scroll_at,
            "verify":            self._verify,
            "generate_content":  self._generate_content,   # AI content writer
        }

        handler = handlers.get(t)
        if not handler:
            return f"[SKIP] Unknown step type: '{t}'"

        try:
            result = handler(step, params)
            logger.info(f"  [{label}]: {result}")
            return result
        except Exception as exc:
            msg = f"[ERROR] {label}: {exc}"
            logger.error(msg)
            return msg

    # ─────────────────────────────────────────────────────────────────────────
    #  HELPER: fill {param} placeholders
    # ─────────────────────────────────────────────────────────────────────────

    def _fill(self, template: str, params: dict) -> str:
        for k, v in params.items():
            template = template.replace(f"{{{k}}}", str(v))
        return template

    def _enrich_params(self, params: dict) -> dict:
        """Add URL-encoded variants and timestamp to params."""
        enriched = dict(params)
        for k, v in list(params.items()):
            if isinstance(v, str):
                enriched[f"{k}_encoded"] = urllib.parse.quote_plus(v)
        enriched["timestamp"] = datetime.now().strftime("%Y%m%d_%H%M%S")
        return enriched

    # ─────────────────────────────────────────────────────────────────────────
    #  STEP HANDLERS
    # ─────────────────────────────────────────────────────────────────────────

    def _cmd(self, step: dict, params: dict) -> str:
        command = self._fill(step["command"], self._enrich_params(params))
        capture = step.get("capture_output", False)
        if capture:
            result = subprocess.run(
                command, shell=True, capture_output=True,
                text=True, timeout=30
            )
            out = (result.stdout or result.stderr or "").strip()
            return f"OK\n{out[:1000]}" if out else "OK (no output)"
        else:
            subprocess.Popen(command, shell=True)
            return f"Launched: {command[:80]}"

    def _delay(self, step: dict, _: dict) -> str:
        secs = float(step.get("seconds", 1.0))
        time.sleep(secs)
        return f"Waited {secs}s"

    def _type_clip(self, step: dict, params: dict) -> str:
        """
        THE CORRECT WAY to type on Windows.
        pyautogui.typewrite() drops characters, misses Unicode, fails on
        special chars. This method copies to clipboard and pastes — 100%
        accurate for any language or symbol.
        """
        if not pyautogui:
            return "pyautogui not available"
        text = self._fill(step["text"], self._enrich_params(params))
        if not text:
            return "Empty text — skipped"

        if _CLIP_OK:
            # Clipboard paste — perfect Unicode support
            pyperclip.copy(text)
            time.sleep(0.1)
            pyautogui.hotkey("ctrl", "v")
            preview = text[:60] + ("..." if len(text) > 60 else "")
            return f"Typed via clipboard: '{preview}'"
        else:
            # Fallback: typewrite (ASCII only)
            safe_text = text.encode("ascii", errors="replace").decode("ascii")
            pyautogui.typewrite(safe_text, interval=0.04)
            return f"Typed (ASCII fallback): '{safe_text[:60]}'"

    def _hotkey(self, step: dict, params: dict) -> str:
        if not pyautogui:
            return "pyautogui not available"
        keys = [self._fill(k, params) for k in step.get("keys", [])]
        pyautogui.hotkey(*keys)
        return f"Hotkey: {'+'.join(keys)}"

    def _press(self, step: dict, params: dict) -> str:
        if not pyautogui:
            return "pyautogui not available"
        key = self._fill(step.get("key", "enter"), params)
        count = int(step.get("count", 1))
        for _ in range(count):
            pyautogui.press(key)
        return f"Pressed: {key}" + (f" x{count}" if count > 1 else "")

    def _write_file(self, step: dict, params: dict) -> str:
        ep = self._enrich_params(params)
        path_str = self._fill(step["path"],    ep).replace("~", str(Path.home()))
        content  = self._fill(step.get("content", ""), ep)
        path = Path(path_str)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return f"File written: {path} ({len(content)} chars)"

    def _screenshot(self, step: dict, params: dict) -> str:
        if not _MSS_OK:
            return "mss / PIL not available"
        ep       = self._enrich_params(params)
        path_str = self._fill(step["path"], ep).replace("~", str(Path.home()))
        save     = Path(path_str)
        save.parent.mkdir(parents=True, exist_ok=True)
        with mss.MSS() as sct:
            monitor = sct.monitors[1]
            raw     = sct.grab(monitor)
            img     = Image.frombytes("RGB", raw.size, raw.bgra, "raw", "BGRX")
            img.save(str(save))
        return f"Screenshot saved: {save}"

    def _win_search(self, step: dict, params: dict) -> str:
        """
        Win+S → clipboard-type query → wait for results.
        THE most reliable way to open any app on Windows.
        Does NOT rely on finding icons on the desktop.
        """
        if not pyautogui:
            return "pyautogui not available"
        query = self._fill(step["query"], self._enrich_params(params))

        # Open Windows Search
        pyautogui.hotkey("win", "s")
        time.sleep(0.8)

        # Clear any existing text in search box
        pyautogui.hotkey("ctrl", "a")
        time.sleep(0.1)

        # Paste query via clipboard (handles app names with spaces/special chars)
        if _CLIP_OK:
            pyperclip.copy(query)
            time.sleep(0.1)
            pyautogui.hotkey("ctrl", "v")
        else:
            pyautogui.typewrite(query, interval=0.06)

        return f"Windows Search: '{query}' (waiting for results...)"

    def _click_pct(self, step: dict, params: dict) -> str:
        """
        Click at a PERCENTAGE of screen width/height.
        Example: coordinate_pct=[0.5, 0.95] clicks center-bottom taskbar area.
        Works identically on 1080p, 1440p, 4K, or any resolution.
        """
        if not pyautogui:
            return "pyautogui not available"
        pct = step.get("coordinate_pct", [0.5, 0.5])
        x   = int(SCREEN_W * pct[0])
        y   = int(SCREEN_H * pct[1])
        # Safety clamp
        x   = max(5, min(x, SCREEN_W - 5))
        y   = max(5, min(y, SCREEN_H - 5))
        duration = float(step.get("duration", 0.2))
        pyautogui.moveTo(x, y, duration=duration)
        time.sleep(0.1)
        pyautogui.click()
        return f"Clicked at {pct} → pixel ({x}, {y}) on {SCREEN_W}x{SCREEN_H} screen"

    def _right_click_pct(self, step: dict, params: dict) -> str:
        if not pyautogui:
            return "pyautogui not available"
        pct = step.get("coordinate_pct", [0.5, 0.5])
        x   = max(5, min(int(SCREEN_W * pct[0]), SCREEN_W - 5))
        y   = max(5, min(int(SCREEN_H * pct[1]), SCREEN_H - 5))
        pyautogui.rightClick(x, y)
        return f"Right-clicked at {pct} → pixel ({x}, {y})"

    def _double_click_pct(self, step: dict, params: dict) -> str:
        if not pyautogui:
            return "pyautogui not available"
        pct = step.get("coordinate_pct", [0.5, 0.5])
        x   = max(5, min(int(SCREEN_W * pct[0]), SCREEN_W - 5))
        y   = max(5, min(int(SCREEN_H * pct[1]), SCREEN_H - 5))
        pyautogui.doubleClick(x, y)
        return f"Double-clicked at {pct} → pixel ({x}, {y})"

    def _scroll_at(self, step: dict, params: dict) -> str:
        if not pyautogui:
            return "pyautogui not available"
        pct       = step.get("coordinate_pct", [0.5, 0.5])
        direction = step.get("direction", "down")
        clicks    = int(step.get("clicks", 3))
        x         = max(5, min(int(SCREEN_W * pct[0]), SCREEN_W - 5))
        y         = max(5, min(int(SCREEN_H * pct[1]), SCREEN_H - 5))
        amount    = -clicks if direction == "down" else clicks
        pyautogui.scroll(amount, x=x, y=y)
        return f"Scrolled {direction} {clicks}x at ({x},{y})"

    def _generate_content(self, step: dict, params: dict) -> str:
        """
        Call the local LLM to GENERATE text content (letters, emails, essays,
        reports, code, etc.) and store the result in params[param_name].

        The result is then available as {generated_content} (or whatever
        param_name is set to) in all subsequent steps.

        This makes the agent smart — it doesn't just TYPE what you say,
        it WRITES what you need using AI.
        """
        if not _OLLAMA_OK or not self._ollama_client:
            fallback = "[Content generation unavailable — Ollama not connected]"
            param_name = step.get("param_name", "generated_content")
            params[param_name] = fallback
            return fallback

        param_name     = step.get("param_name", "generated_content")
        prompt_tmpl    = step.get("prompt", "Write a short document.")
        max_tokens     = int(step.get("max_tokens", 2048))
        temperature    = float(step.get("temperature", 0.7))
        prompt         = self._fill(prompt_tmpl, params)

        system_prompt = (
            "You are a professional content writer and expert at writing formal documents.\n"
            "Generate exactly what is requested — output ONLY the content itself.\n"
            "Do NOT add any preamble like 'Here is the letter:' or 'Sure! Below is...'.\n"
            "Do NOT add any commentary after the content.\n"
            "Just the pure, ready-to-use document text, correctly formatted.\n"
            "Use proper formatting: blank lines between paragraphs, correct salutations, etc."
        )

        print(f"\n    [AI Writer] Generating content for: {prompt[:80]}...")

        for attempt in range(3):
            try:
                resp = self._ollama_client.chat(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user",   "content": prompt}
                    ],
                    options={
                        "temperature": temperature,
                        "num_predict": max_tokens,
                        "top_p": 0.95,
                    }
                )
                content = resp.message.content.strip()
                if content:
                    # Store in the shared params dict so subsequent steps see it
                    params[param_name] = content
                    params[f"{param_name}_encoded"] = urllib.parse.quote_plus(content)

                    preview = content[:120].replace("\n", " ")
                    logger.info(f"  AI generated {len(content)} chars: {preview}...")
                    print(f"    [AI Writer] Done — {len(content)} characters generated.")
                    return f"Generated {len(content)} chars of content (stored as '{param_name}')"
                else:
                    logger.warning(f"  AI content generation attempt {attempt+1}: empty response")
                    time.sleep(1.0)
            except Exception as exc:
                logger.warning(f"  AI content generation attempt {attempt+1} error: {exc}")
                time.sleep(1.0)

        fallback = "[AI generation failed — please check Ollama connection]"
        params[param_name] = fallback
        return f"FAILED: {fallback}"

    def _verify(self, step: dict, params: dict) -> str:
        """
        Take a screenshot and ask the LLM to verify the expected screen state.
        Returns VERIFIED or UNVERIFIED with reason.
        This is what makes GUI steps precise — we check the outcome, not just fire and forget.
        """
        if not _MSS_OK or not _OLLAMA_OK or not self._ollama_client:
            return "[SKIP] Verify unavailable (mss/ollama not ready)"

        expected = step.get("expected", "action completed successfully")

        try:
            # Capture screen
            with mss.MSS() as sct:
                monitor = sct.monitors[1]
                raw     = sct.grab(monitor)
                img     = Image.frombytes("RGB", raw.size, raw.bgra, "raw", "BGRX")

            # Downscale to 800px for quick verification
            if img.width > 800:
                ratio = 800 / img.width
                img   = img.resize((800, int(img.height * ratio)), Image.LANCZOS)

            buf = io.BytesIO()
            img.save(buf, format="JPEG", quality=65, optimize=True)
            b64 = base64.b64encode(buf.getvalue()).decode("utf-8")

            # Ask LLM to verify
            verify_prompt = (
                f"Look at this screenshot carefully.\n"
                f"Expected state: {expected}\n\n"
                f"Reply ONLY with a JSON object:\n"
                f'{{ "verified": true_or_false, "reason": "one sentence" }}'
            )

            resp = self._ollama_client.chat(
                model=self.model,
                messages=[{
                    "role": "user",
                    "content": verify_prompt,
                    "images": [b64]
                }],
                format="json",
                options={"temperature": 0.0, "num_predict": 128}
            )

            raw_txt = resp.message.content.strip()
            if raw_txt:
                # Extract JSON
                m = re.search(r"\{.*\}", raw_txt, re.DOTALL)
                if m:
                    result = json.loads(m.group())
                    verified = result.get("verified", False)
                    reason   = result.get("reason", "")
                    status   = "VERIFIED" if verified else "UNVERIFIED"
                    return f"[{status}] {reason}"

            return "[VERIFY] Model returned empty — assuming OK"

        except Exception as exc:
            return f"[VERIFY ERROR] {exc} — continuing"


# ══════════════════════════════════════════════════════════════════════════════
#  PLAYBOOK RUNNER
# ══════════════════════════════════════════════════════════════════════════════

class PlaybookRunner:
    """
    Executes a full playbook (list of steps) for a matched task.
    Uses StepExecutor for each step, fills params, returns results list.
    """

    def __init__(self, model: str = "gemma4:e2b", ollama_host: str = "http://localhost:11434") -> None:
        self.executor = StepExecutor(model=model, ollama_host=ollama_host)

    def run(self, playbook: dict, params: dict) -> list[str]:
        steps   = playbook.get("steps", [])
        results = []

        # Enrich params
        enriched = dict(params)
        for k, v in list(params.items()):
            if isinstance(v, str):
                enriched[f"{k}_encoded"] = urllib.parse.quote_plus(v)
        enriched["timestamp"] = datetime.now().strftime("%Y%m%d_%H%M%S")

        tier  = playbook.get("tier", "cmd")
        title = playbook.get("description", "")
        logger.info(f"Running [{tier.upper()}] playbook: {title}")
        logger.info(f"  Steps: {len(steps)} | Params: {list(params.keys())}")

        for i, step in enumerate(steps, 1):
            label = step.get("label", step.get("type", f"Step {i}"))
            label_filled = self.executor._fill(label, enriched)
            print(f"    [{i}/{len(steps)}] {label_filled}...")

            result = self.executor.run(step, enriched)
            results.append(f"[{label_filled}]: {result}")

        return results
