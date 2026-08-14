"""
╔══════════════════════════════════════════════════════════════════════════════╗
║         LOCAL DESKTOP COMPUTER-USE AGENT — Production Framework             ║
║         Architecture: Anthropic Claude Computer-Use (Local Variant)         ║
║         Brain: Ollama / gemma4:e2b (Vision) |  OS: pyautogui + mss          ║
╚══════════════════════════════════════════════════════════════════════════════╝

Execution Flow:
  User Task  ->  TaskRouter (fast text-only LLM)
                   |-- known task  -->  PlaybookExecutor (CMD/subprocess)
                   `-- unknown     -->  Vision Agent Loop (screenshot + LLM)

Usage:
    python agent.py --task "Open Notepad and type Hello World"
    python agent.py --task "Search Google for Python tutorials" --max-iter 10
    python agent.py --model gemma3:1b --task "Take a screenshot and describe it"

Dependencies:
    pip install ollama pyautogui mss pillow
    # Ollama must be running locally: ollama serve
    # Pull model: ollama pull gemma4:e2b
"""

from __future__ import annotations

import argparse
import base64
import io
import json
import logging
import os
import signal
import sys
import time
import textwrap
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Literal, Optional

# ── Third-party imports ────────────────────────────────────────────────────────
try:
    import pyautogui
except ImportError:
    sys.exit("[FATAL] pyautogui not installed. Run: pip install pyautogui")

try:
    import mss
    import mss.tools
except ImportError:
    sys.exit("[FATAL] mss not installed. Run: pip install mss")

try:
    from PIL import Image
except ImportError:
    sys.exit("[FATAL] Pillow not installed. Run: pip install pillow")

try:
    import ollama
except ImportError:
    sys.exit("[FATAL] ollama not installed. Run: pip install ollama")


# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 1 — CONFIGURATION & TYPING
# ══════════════════════════════════════════════════════════════════════════════

ActionType = Literal["mouse_move", "left_click", "right_click", "double_click",
                     "type", "hotkey", "scroll", "wait", "done"]

@dataclass
class AgentConfig:
    """Centralised, strongly-typed agent configuration."""
    # Model
    model: str = "gemma4:e2b"
    ollama_host: str = "http://localhost:11434"
    temperature: float = 0.1            # Low temp -> deterministic JSON output
    # Screen
    max_image_width: int = 1024         # Max px width before downscale
    jpeg_quality: int = 75             # Lower = smaller payload
    monitor_index: int = 1             # mss monitor (1 = primary)
    # Execution
    max_iterations: int = 20           # Hard cap: full session
    stall_threshold: int = 5           # Iterations before human handoff
    post_action_delay: float = 1.5     # Seconds after pyautogui call (UI settle)
    screenshot_delay: float = 0.3      # Seconds before screenshot capture
    type_interval: float = 0.04        # pyautogui typing speed (seconds/char)
    # Logging
    log_dir: Path = field(default_factory=lambda: Path("logs"))
    log_level: int = logging.DEBUG


@dataclass
class AgentAction:
    """Parsed, validated action from model JSON response."""
    thought: str
    action: ActionType
    coordinate: Optional[list[int]] = None
    text: Optional[str] = None
    raw: dict = field(default_factory=dict)


@dataclass
class IterationState:
    """Tracks per-iteration metadata for the state machine."""
    iteration: int = 0
    stall_count: int = 0
    last_action: Optional[ActionType] = None
    last_thought: str = ""
    task_history: list[str] = field(default_factory=list)
    start_time: float = field(default_factory=time.time)


# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 2 — SYSTEM PROMPT CONTRACT
# ══════════════════════════════════════════════════════════════════════════════

SYSTEM_PROMPT = textwrap.dedent("""
You are a Desktop Computer-Use Agent. Your job is to analyse a screenshot of
the user's desktop and determine the single best next action to achieve the
given task.

--- OUTPUT FORMAT: STRICT JSON ONLY ---
You MUST respond with ONLY a valid raw JSON object. No markdown, no code
fences, no explanatory text -- just the JSON object itself.

Required schema:
{
  "thought": "<step-by-step internal reasoning about current screen state>",
  "action": "<one of: mouse_move | left_click | right_click | double_click | type | hotkey | scroll | wait | done>",
  "coordinate": [X, Y],
  "text": "<text to type, or key combination like ctrl+c>"
}

Field rules:
- "thought"    : REQUIRED. Your detailed reasoning about what you see and why.
- "action"     : REQUIRED. Exactly one action string from the allowed list.
- "coordinate" : REQUIRED for mouse_move, left_click, right_click,
                 double_click, scroll. Integer pixel [X, Y] on screen.
- "text"       : REQUIRED for type (text to type) and hotkey (key combo string
                 e.g. "ctrl+s", "alt+F4", "win+d"). Optional for others.

Action semantics:
- mouse_move   : Move mouse cursor to coordinate (no click).
- left_click   : Single left click at coordinate.
- right_click  : Single right click at coordinate.
- double_click : Double left click at coordinate (open files, apps).
- type         : Type the string in "text" at current cursor position.
- hotkey       : Press keyboard shortcut in "text" (e.g. "ctrl+v").
- scroll       : Scroll at coordinate; use text="up" or text="down".
- wait         : Pause execution (use when animations/loading in progress).
- done         : Signal task is fully complete. No further actions needed.

--- CONSTRAINTS ---
- Only one action per response.
- Coordinates must be within the visible screen area.
- Never guess coordinates blindly -- derive them from what you see.
- If a previous action did not produce expected results, reason differently.
- Respond with ONLY the JSON. Nothing before or after.
""").strip()


# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 3 — LOGGING SETUP
# ══════════════════════════════════════════════════════════════════════════════

def setup_logging(config: AgentConfig) -> logging.Logger:
    """Configure file + console dual-handler logging."""
    config.log_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = config.log_dir / f"agent_{timestamp}.log"

    logger = logging.getLogger("ComputerUseAgent")
    logger.setLevel(config.log_level)

    # File handler -- verbose DEBUG
    fh = logging.FileHandler(log_file, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%H:%M:%S"
    ))

    # Console handler -- INFO only (keeps terminal clean)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    ch.setFormatter(logging.Formatter("%(message)s"))

    logger.addHandler(fh)
    logger.addHandler(ch)

    logger.info(f"Log file: {log_file.resolve()}")
    return logger


# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 4 — SCREEN CAPTURE ENGINE
# ══════════════════════════════════════════════════════════════════════════════

class ScreenCaptureEngine:
    """
    Ultra-fast multi-monitor safe screen capture using mss.
    Downscales images to max_width and returns base64-encoded JPEG bytes
    to minimise Ollama multimodal token payload size.
    """

    def __init__(self, config: AgentConfig, logger: logging.Logger) -> None:
        self.config = config
        self.logger = logger
        self._sct: Optional[mss.mss] = None

    def __enter__(self) -> "ScreenCaptureEngine":
        self._sct = mss.MSS()
        return self

    def __exit__(self, *_: Any) -> None:
        if self._sct:
            self._sct.close()

    def get_screen_size(self) -> tuple[int, int]:
        """Return (width, height) of the configured monitor."""
        if not self._sct:
            raise RuntimeError("ScreenCaptureEngine not initialised via context manager.")
        monitor = self._sct.monitors[self.config.monitor_index]
        return monitor["width"], monitor["height"]

    def capture(self) -> tuple[str, tuple[int, int]]:
        """
        Capture the screen and return:
          - base64-encoded JPEG string (for Ollama image payload)
          - (original_width, original_height) tuple for coordinate mapping
        """
        if not self._sct:
            raise RuntimeError("ScreenCaptureEngine not initialised via context manager.")

        monitor = self._sct.monitors[self.config.monitor_index]
        original_size = (monitor["width"], monitor["height"])

        # Grab raw screenshot
        raw_screenshot = self._sct.grab(monitor)

        # Convert to PIL Image (mss returns BGRA, PIL expects RGB)
        img = Image.frombytes("RGB", raw_screenshot.size, raw_screenshot.bgra, "raw", "BGRX")

        # Downscale to max_image_width if needed
        if img.width > self.config.max_image_width:
            scale_ratio = self.config.max_image_width / img.width
            new_height = int(img.height * scale_ratio)
            img = img.resize(
                (self.config.max_image_width, new_height),
                Image.LANCZOS
            )
            self.logger.debug(
                f"Image downscaled: {original_size} -> ({img.width}x{img.height})"
            )

        # Encode to JPEG byte stream
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=self.config.jpeg_quality, optimize=True)
        jpeg_bytes = buffer.getvalue()

        # Base64 encode for Ollama multimodal payload
        b64_str = base64.b64encode(jpeg_bytes).decode("utf-8")

        self.logger.debug(
            f"Screenshot captured: {len(jpeg_bytes) / 1024:.1f} KB JPEG -> "
            f"{len(b64_str) / 1024:.1f} KB base64"
        )
        return b64_str, original_size


# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 5 — VISUAL MEMORY PRUNER
# ══════════════════════════════════════════════════════════════════════════════

class VisualMemoryPruner:
    """
    Implements the Visual Memory Pruning System to prevent context overflow
    in local 7B models with tight context windows.

    Strategy:
    - KEEP: System prompt (index 0) -- never pruned.
    - KEEP: The single most recent message (last in list) -- full image data.
    - STRIP: All older assistant/user messages -- images removed, text kept.
    """

    def __init__(self, logger: logging.Logger) -> None:
        self.logger = logger

    def prune(self, messages: list[dict]) -> list[dict]:
        """
        Return a pruned copy of the message list safe for Ollama submission.
        Modifies a copy, never mutates the source list.
        """
        if len(messages) <= 2:
            # System prompt + at most one message -- nothing to prune
            return messages

        pruned: list[dict] = []
        total_images_dropped = 0

        for i, msg in enumerate(messages):
            is_last = (i == len(messages) - 1)
            is_system = (msg.get("role") == "system")

            if is_system or is_last:
                # Preserve system prompt and latest message intact
                pruned.append(msg)
            else:
                # Strip images from older messages, keep text content
                cleaned_msg = dict(msg)
                if "images" in cleaned_msg:
                    dropped = len(cleaned_msg["images"])
                    total_images_dropped += dropped
                    del cleaned_msg["images"]
                    if isinstance(cleaned_msg.get("content"), str):
                        cleaned_msg["content"] = (
                            cleaned_msg["content"]
                            + f"\n[{dropped} screenshot(s) pruned for context efficiency]"
                        )
                pruned.append(cleaned_msg)

        if total_images_dropped > 0:
            self.logger.debug(
                f"VisualMemoryPruner: dropped {total_images_dropped} image(s) "
                f"from {len(messages) - 2} older message(s)."
            )

        return pruned


# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 6 — OLLAMA VISION BRAIN
# ══════════════════════════════════════════════════════════════════════════════

class OllamaVisionBrain:
    """
    Manages communication with the local Ollama instance.
    Enforces structured JSON output via format="json" and
    robust retry logic for decode failures.
    """

    ALLOWED_ACTIONS = frozenset({
        "mouse_move", "left_click", "right_click", "double_click",
        "type", "hotkey", "scroll", "wait", "done"
    })

    def __init__(self, config: AgentConfig, logger: logging.Logger) -> None:
        self.config = config
        self.logger = logger
        self._client = ollama.Client(host=config.ollama_host)

    def ping(self) -> bool:
        """Verify Ollama server is reachable and model is available."""
        try:
            models = self._client.list()
            available = [m.model for m in models.models]
            self.logger.info(f"Ollama connected. Available models: {available}")
            if not any(self.config.model in m for m in available):
                self.logger.warning(
                    f"Model '{self.config.model}' not found locally. "
                    f"Run: ollama pull {self.config.model}"
                )
                return False
            return True
        except Exception as exc:
            self.logger.error(f"Cannot reach Ollama at {self.config.ollama_host}: {exc}")
            return False

    @staticmethod
    def _extract_json(raw: str) -> str:
        """
        Robustly extract a JSON object from a model response.
        Handles three cases:
          1. Pure JSON   : {"action": ...}
          2. Fenced JSON : ```json\n{...}\n```
          3. Mixed prose : ...some text... {"action": ...} ...more text...
        """
        if not raw:
            return ""

        # Case 1 — already clean JSON
        stripped = raw.strip()
        if stripped.startswith("{"):
            return stripped

        # Case 2 — markdown code fence (```json ... ``` or ``` ... ```)
        import re
        fence_match = re.search(r"```(?:json)?\s*({.*?})\s*```", stripped, re.DOTALL)
        if fence_match:
            return fence_match.group(1).strip()

        # Case 3 — JSON buried in prose, find first { ... } block
        brace_match = re.search(r"({.*})", stripped, re.DOTALL)
        if brace_match:
            return brace_match.group(1).strip()

        return stripped

    def think(
        self,
        messages: list[dict],
        retry_count: int = 3
    ) -> AgentAction:
        """
        Send the pruned message list to Ollama and parse the response
        into a validated AgentAction.

        Retry strategy (up to retry_count attempts):
          - Attempt 1-2 : use format='json' with correction prompt on failure
          - Attempt 3   : drop format='json', rely on prompt engineering only
          - Empty resp  : treated as a retryable failure (not just JSONDecodeError)
        """
        last_error: Optional[Exception] = None
        raw_text: str = ""
        current_messages = list(messages)

        for attempt in range(retry_count + 1):
            # On the last attempt, drop format="json" — some vision models
            # produce empty output when format + image are combined.
            use_format_json = attempt < retry_count

            try:
                self.logger.debug(
                    f"Sending {len(current_messages)} messages to Ollama "
                    f"(attempt {attempt + 1}/{retry_count + 1}, "
                    f"format_json={use_format_json})"
                )

                call_kwargs: dict = dict(
                    model=self.config.model,
                    messages=current_messages,
                    options={
                        "temperature": self.config.temperature,
                        "num_predict": 1024,   # Enough for vision + JSON
                        "top_p": 0.9,
                    }
                )
                if use_format_json:
                    call_kwargs["format"] = "json"

                response = self._client.chat(**call_kwargs)
                raw_text = response.message.content.strip()
                self.logger.debug(f"Raw model response ({len(raw_text)} chars):\n{raw_text[:400]}")

                # ── Empty response guard ───────────────────────────────────
                if not raw_text:
                    raise json.JSONDecodeError(
                        "Empty response from model", "", 0
                    )

                # ── Extract JSON (handles fences, prose wrapping) ──────────
                json_str = self._extract_json(raw_text)
                self.logger.debug(f"Extracted JSON string: {json_str[:200]}")

                parsed = json.loads(json_str)
                return self._validate(parsed)

            except json.JSONDecodeError as exc:
                last_error = exc
                self.logger.warning(
                    f"JSON decode failed (attempt {attempt + 1}/{retry_count + 1}): {exc}. "
                    f"Raw ({len(raw_text)} chars): {raw_text[:200]!r}"
                )
                if attempt < retry_count:
                    # Inject a strict correction message and try again
                    current_messages = current_messages + [{
                        "role": "user",
                        "content": (
                            "Your previous response was empty or not valid JSON. "
                            "You MUST respond with ONLY a raw JSON object. "
                            "No markdown, no code fences, no explanatory text. "
                            "Start your response directly with '{' and end with '}'. "
                            "Required keys: thought, action, coordinate, text."
                        )
                    }]
                    time.sleep(0.8)

            except Exception as exc:
                last_error = exc
                self.logger.error(f"Ollama API error (attempt {attempt + 1}): {exc}")
                if attempt < retry_count:
                    time.sleep(1.5)

        self.logger.error(f"All {retry_count + 1} attempts failed. Last error: {last_error}")
        return AgentAction(
            thought=f"Failed to get valid response after {retry_count + 1} attempts: {last_error}",
            action="wait",
            raw={}
        )

    def _validate(self, parsed: dict) -> AgentAction:
        """Validate parsed JSON against schema and return AgentAction."""
        thought = str(parsed.get("thought", "No thought provided"))

        action_raw = str(parsed.get("action", "wait")).lower().strip()
        if action_raw not in self.ALLOWED_ACTIONS:
            self.logger.warning(f"Unknown action '{action_raw}', defaulting to 'wait'")
            action_raw = "wait"
        action: ActionType = action_raw  # type: ignore[assignment]

        coordinate: Optional[list[int]] = None
        raw_coord = parsed.get("coordinate")
        if raw_coord is not None:
            try:
                coordinate = [int(raw_coord[0]), int(raw_coord[1])]
            except (TypeError, IndexError, ValueError) as exc:
                self.logger.warning(f"Invalid coordinate {raw_coord!r}: {exc}")

        text: Optional[str] = None
        if "text" in parsed and parsed["text"] is not None:
            text = str(parsed["text"])

        return AgentAction(
            thought=thought,
            action=action,
            coordinate=coordinate,
            text=text,
            raw=parsed
        )


# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 7 — TOOL EXECUTOR (pyautogui dispatcher)
# ══════════════════════════════════════════════════════════════════════════════

class ToolExecutor:
    """
    Translates AgentAction into concrete pyautogui system calls.
    Includes:
    - Screen boundary coordinate clamping
    - Coordinate scaling from downscaled image back to real screen pixels
    - Execution timing delays for UI settle
    - Comprehensive error handling per action type
    """

    def __init__(self, config: AgentConfig, logger: logging.Logger) -> None:
        self.config = config
        self.logger = logger

        # Configure pyautogui safety
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.05

        self.screen_w, self.screen_h = pyautogui.size()
        self.logger.info(f"Screen resolution: {self.screen_w}x{self.screen_h}")

    def clamp_coordinate(self, x: int, y: int) -> tuple[int, int]:
        """Clamp coordinates to valid screen bounds with 5px margin."""
        margin = 5
        cx = max(margin, min(x, self.screen_w - margin))
        cy = max(margin, min(y, self.screen_h - margin))
        if cx != x or cy != y:
            self.logger.warning(f"Coordinate clamped: ({x},{y}) -> ({cx},{cy})")
        return cx, cy

    def scale_coordinate(
        self,
        coord: list[int],
        original_size: tuple[int, int],
        scaled_width: int
    ) -> tuple[int, int]:
        """
        Map model coordinates (from downscaled image) back to actual screen
        pixel coordinates using the captured original resolution.
        """
        orig_w, orig_h = original_size
        scale_x = orig_w / min(scaled_width, orig_w)
        scale_y = scale_x  # Uniform aspect ratio scaling

        actual_x = int(coord[0] * scale_x)
        actual_y = int(coord[1] * scale_y)

        return self.clamp_coordinate(actual_x, actual_y)

    def execute(
        self,
        action: AgentAction,
        original_screen_size: tuple[int, int]
    ) -> str:
        """
        Execute the action and return a human-readable execution log string.
        """
        act = action.action

        screen_x, screen_y = 0, 0
        if action.coordinate:
            screen_x, screen_y = self.scale_coordinate(
                action.coordinate,
                original_screen_size,
                self.config.max_image_width
            )

        try:
            if act == "mouse_move":
                pyautogui.moveTo(screen_x, screen_y, duration=0.3)
                result = f"Mouse moved -> ({screen_x}, {screen_y})"

            elif act == "left_click":
                pyautogui.click(screen_x, screen_y)
                result = f"Left click -> ({screen_x}, {screen_y})"

            elif act == "right_click":
                pyautogui.rightClick(screen_x, screen_y)
                result = f"Right click -> ({screen_x}, {screen_y})"

            elif act == "double_click":
                pyautogui.doubleClick(screen_x, screen_y)
                result = f"Double click -> ({screen_x}, {screen_y})"

            elif act == "type":
                if not action.text:
                    raise ValueError("'type' action requires 'text' field.")
                pyautogui.typewrite(action.text, interval=self.config.type_interval)
                preview = action.text[:40] + ("..." if len(action.text) > 40 else "")
                result = f"Typed: '{preview}'"

            elif act == "hotkey":
                if not action.text:
                    raise ValueError("'hotkey' action requires 'text' field.")
                keys = [k.strip() for k in action.text.lower().split("+")]
                pyautogui.hotkey(*keys)
                result = f"Hotkey pressed: {'+'.join(keys)}"

            elif act == "scroll":
                direction = (action.text or "down").lower()
                clicks = 3 if direction == "down" else -3
                pyautogui.scroll(clicks, x=screen_x, y=screen_y)
                result = f"Scrolled {direction} at ({screen_x}, {screen_y})"

            elif act == "wait":
                time.sleep(self.config.post_action_delay)
                result = f"Waited {self.config.post_action_delay}s"

            elif act == "done":
                result = "Task marked DONE by model."

            else:
                result = f"Unknown action '{act}' -- skipped."

        except pyautogui.FailSafeException:
            self.logger.critical("PyAutoGUI Fail-Safe triggered (mouse in corner). Aborting.")
            raise

        except Exception as exc:
            result = f"Execution error for '{act}': {exc}"
            self.logger.error(result)

        # Wait for UI to settle after action (except wait/done which handle their own timing)
        if act not in ("wait", "done"):
            time.sleep(self.config.post_action_delay)

        return result


# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 8 — CONSOLE UI / STATUS DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════

class ConsoleDashboard:
    """Renders a clean ANSI status dashboard to the terminal after each iteration."""

    COLORS = {
        "reset":   "\033[0m",
        "bold":    "\033[1m",
        "cyan":    "\033[96m",
        "green":   "\033[92m",
        "yellow":  "\033[93m",
        "red":     "\033[91m",
        "blue":    "\033[94m",
        "magenta": "\033[95m",
        "dim":     "\033[2m",
    }

    def c(self, color: str, text: str) -> str:
        """Apply ANSI color if terminal supports it."""
        if sys.stdout.isatty():
            return f"{self.COLORS.get(color, '')}{text}{self.COLORS['reset']}"
        return text

    def print_header(self, task: str) -> None:
        print()
        print(self.c("cyan",   "=" * 70))
        print(self.c("bold",   "  LOCAL COMPUTER-USE AGENT"))
        print(self.c("dim",    "  Brain: Ollama Vision | Controls: pyautogui + mss"))
        print(self.c("cyan",   "-" * 70))
        print(self.c("yellow", f"  Task: {task}"))
        print(self.c("cyan",   "=" * 70))
        print()

    def print_iteration(
        self,
        state: IterationState,
        action: AgentAction,
        execution_result: str,
        elapsed: float
    ) -> None:
        print()
        print(self.c("cyan", f"+-- Iteration {state.iteration} " + "-" * 48))
        print(self.c("dim",  f"|   Elapsed: {elapsed:.1f}s | Stall count: {state.stall_count}"))
        print()

        thought_lines = textwrap.wrap(action.thought, width=62)
        print(self.c("blue", "|   THOUGHT:"))
        for line in thought_lines:
            print(f"|     {line}")

        print()
        action_color = "green" if action.action == "done" else "yellow"
        print(self.c(action_color, f"|   ACTION:  {action.action.upper()}"))

        if action.coordinate:
            print(self.c("dim", f"|   COORD:   {action.coordinate}"))
        if action.text:
            preview = action.text[:50] + ("..." if len(action.text) > 50 else "")
            print(self.c("dim", f"|   TEXT:    '{preview}'"))

        print()
        print(self.c("magenta", f"|   RESULT:  {execution_result}"))
        print(self.c("cyan", "+" + "-" * 60))

    def print_handoff_prompt(self, state: IterationState, reason: str) -> str:
        """
        Print the human handoff banner and prompt for input.
        Returns the user's instruction or empty string to continue.
        """
        print()
        print(self.c("red", "+" + "=" * 68 + "+"))
        print(self.c("red", "|") + self.c("bold", "  HUMAN HANDOFF REQUIRED") + " " * 45 + self.c("red", "|"))
        print(self.c("red", "+" + "=" * 68 + "+"))
        reason_trunc = reason[:60]
        print(self.c("red", "|") + f"  Reason : {reason_trunc:<58}" + self.c("red", "|"))
        print(self.c("red", "|") + f"  Iter   : {state.iteration:<58}" + self.c("red", "|"))
        print(self.c("red", "|") + f"  Stalls : {state.stall_count:<58}" + self.c("red", "|"))
        print(self.c("red", "+" + "-" * 68 + "+"))
        print(self.c("red", "|") + "  Recent actions:" + " " * 52 + self.c("red", "|"))
        for entry in state.task_history[-5:]:
            truncated = entry[:64]
            print(self.c("red", "|") + f"    - {truncated:<64}" + self.c("red", "|"))
        print(self.c("red", "+" + "=" * 68 + "+"))
        print()

        try:
            user_input = input(
                self.c("yellow", "  Task state evaluated. What would you like me to do next?\n")
                + self.c("dim",   "  (Enter to continue | new instruction | 'quit' to exit)\n")
                + self.c("cyan",  "  > ")
            ).strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return "quit"

        return user_input

    def print_session_summary(self, state: IterationState, task: str) -> None:
        elapsed = time.time() - state.start_time
        print()
        print(self.c("green", "+" + "=" * 68 + "+"))
        print(self.c("green", "|") + self.c("bold", "  SESSION COMPLETE") + " " * 51 + self.c("green", "|"))
        print(self.c("green", "+" + "=" * 68 + "+"))
        task_trunc = task[:53]
        elapsed_str = f"{elapsed:.1f}s"
        print(self.c("green", "|") + f"  Task       : {task_trunc:<54}" + self.c("green", "|"))
        print(self.c("green", "|") + f"  Iterations : {state.iteration:<54}" + self.c("green", "|"))
        print(self.c("green", "|") + f"  Total Time : {elapsed_str:<54}" + self.c("green", "|"))
        print(self.c("green", "+" + "=" * 68 + "+"))
        print()


# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 9 — AGENT ORCHESTRATOR (Main State Machine)
# ══════════════════════════════════════════════════════════════════════════════

class AgentOrchestrator:
    """
    Central orchestration loop. Implements the full state machine:

    Capture Screen -> Prune Memory -> Think (Ollama) -> Execute (pyautogui) -> Evaluate State
         ^                                                                             |
         +-----------------------------------------------------------------------------+
                              (loop until done / stall / quit)
    """

    def __init__(self, config: AgentConfig) -> None:
        self.config = config
        self.logger = setup_logging(config)
        self.pruner = VisualMemoryPruner(self.logger)
        self.brain = OllamaVisionBrain(config, self.logger)
        self.dashboard = ConsoleDashboard()
        self._running = True

        signal.signal(signal.SIGINT, self._signal_handler)
        if hasattr(signal, "SIGTERM"):
            signal.signal(signal.SIGTERM, self._signal_handler)

    def _signal_handler(self, signum: int, frame: Any) -> None:
        self.logger.info("\nSignal received. Stopping gracefully...")
        self._running = False

    def _build_initial_messages(self, task: str) -> list[dict]:
        """Construct the initial message list with system prompt + task."""
        return [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": (
                    f"Your task is: {task}\n\n"
                    "I am sending you the current screenshot of the desktop. "
                    "Analyse it carefully and decide the next best single action."
                )
            }
        ]

    def _append_screenshot_message(
        self,
        messages: list[dict],
        b64_image: str,
        action_result: Optional[str] = None
    ) -> list[dict]:
        """
        Append a new user message with the latest screenshot.
        Optionally includes the result of the previous action.
        """
        if action_result:
            content = (
                f"Previous action result: {action_result}\n\n"
                "Here is the current state of the desktop. "
                "What is the next best action?"
            )
        else:
            content = (
                "Here is the current desktop screenshot. "
                "What is the next best action?"
            )

        return messages + [{
            "role": "user",
            "content": content,
            "images": [b64_image]
        }]

    def run(self, task: str) -> None:
        """Main execution entry point."""
        self.dashboard.print_header(task)

        if not self.brain.ping():
            self.logger.error(
                "Cannot proceed without Ollama connection. "
                f"Ensure 'ollama serve' is running and "
                f"'{self.config.model}' is pulled."
            )
            return

        state = IterationState()
        messages = self._build_initial_messages(task)
        last_execution_result: Optional[str] = None

        with ScreenCaptureEngine(self.config, self.logger) as capture:

            while self._running and state.iteration < self.config.max_iterations:
                state.iteration += 1
                iter_start = time.time()

                self.logger.info(
                    f"\n[Iteration {state.iteration}/{self.config.max_iterations}]"
                )

                # 1. Brief delay for UI to settle before screenshot
                time.sleep(self.config.screenshot_delay)

                # 2. Capture screenshot
                try:
                    b64_image, original_size = capture.capture()
                except Exception as exc:
                    self.logger.error(f"Screenshot failed: {exc}")
                    time.sleep(1.0)
                    continue

                # 3. Append screenshot message to thread
                messages = self._append_screenshot_message(
                    messages, b64_image, last_execution_result
                )

                # 4. Prune visual memory (context overflow protection)
                pruned_messages = self.pruner.prune(messages)

                # 5. Send to Ollama Vision Brain
                self.logger.info("Sending to Vision Brain...")
                action = self.brain.think(pruned_messages)

                # 6. Execute action
                executor = ToolExecutor(self.config, self.logger)
                execution_result = ""

                if action.action == "done":
                    execution_result = "Task marked DONE by model."
                    self.logger.info(execution_result)
                else:
                    try:
                        execution_result = executor.execute(action, original_size)
                        self.logger.info(f"Executed: {execution_result}")
                    except pyautogui.FailSafeException:
                        self._running = False
                        break
                    except Exception as exc:
                        execution_result = f"Execution error: {exc}"
                        self.logger.error(execution_result)

                last_execution_result = execution_result

                # 7. Append assistant response to history
                messages.append({
                    "role": "assistant",
                    "content": json.dumps(action.raw) if action.raw else action.thought
                })

                # 8. Update state tracking
                state.task_history.append(
                    f"[{state.iteration}] {action.action}: {execution_result[:80]}"
                )
                if action.action == state.last_action:
                    state.stall_count += 1
                else:
                    state.stall_count = 0
                state.last_action = action.action
                state.last_thought = action.thought

                # 9. Render status dashboard
                elapsed = time.time() - state.start_time
                self.dashboard.print_iteration(state, action, execution_result, elapsed)

                # 10. Evaluate state: done / stall / handoff
                if action.action == "done":
                    reason = "Model signalled task completion."
                    handoff_input = self.dashboard.print_handoff_prompt(state, reason)
                    if not handoff_input or handoff_input.lower() == "quit":
                        break
                    # User provided a follow-up task
                    messages = self._build_initial_messages(handoff_input)
                    last_execution_result = None
                    state.stall_count = 0
                    state.last_action = None

                elif state.stall_count >= self.config.stall_threshold:
                    reason = (
                        f"Stall detected: '{action.action}' "
                        f"repeated {state.stall_count}x consecutively."
                    )
                    self.logger.warning(reason)
                    handoff_input = self.dashboard.print_handoff_prompt(state, reason)
                    if not handoff_input or handoff_input.lower() == "quit":
                        break
                    if handoff_input:
                        messages.append({
                            "role": "user",
                            "content": (
                                f"Human guidance: {handoff_input}\n"
                                "Please adjust your approach accordingly."
                            )
                        })
                    state.stall_count = 0

                # Brief pause between iterations
                time.sleep(0.2)

        # Session complete
        self.dashboard.print_session_summary(state, task)
        self.logger.info("Agent session ended.")


# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 10 — CLI ENTRY POINT
# ══════════════════════════════════════════════════════════════════════════════

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="agent",
        description="Local Desktop Computer-Use Agent (Ollama + gemma2:7b)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""
        Examples:
          python agent.py --task "Open Notepad and type Hello World"
          python agent.py --task "Take a screenshot" --model gemma2:2b
          python agent.py --task "Search for Python docs" --max-iter 15
          python agent.py --task "Open calculator and compute 42 * 7" --delay 2.0
        """)
    )

    parser.add_argument(
        "--task", "-t",
        required=False,
        default=None,
        help="The task for the agent to perform on your desktop."
    )
    parser.add_argument(
        "--model", "-m",
        default="gemma4:e2b",
        help="Ollama model name (default: gemma4:e2b)"
    )
    parser.add_argument(
        "--max-iter",
        type=int,
        default=20,
        help="Maximum agent iterations before forced stop (default: 20)"
    )
    parser.add_argument(
        "--stall",
        type=int,
        default=5,
        help="Stall threshold: consecutive same-actions before handoff (default: 5)"
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=1.5,
        help="Post-action delay in seconds for UI settle (default: 1.5)"
    )
    parser.add_argument(
        "--width",
        type=int,
        default=1024,
        help="Max image width in pixels before downscaling (default: 1024)"
    )
    parser.add_argument(
        "--host",
        default="http://localhost:11434",
        help="Ollama server URL (default: http://localhost:11434)"
    )
    parser.add_argument(
        "--monitor",
        type=int,
        default=1,
        help="Monitor index to capture (1=primary, default: 1)"
    )
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Console logging level (default: INFO)"
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    config = AgentConfig(
        model=args.model,
        ollama_host=args.host,
        max_iterations=args.max_iter,
        stall_threshold=args.stall,
        post_action_delay=args.delay,
        max_image_width=args.width,
        monitor_index=args.monitor,
        log_level=getattr(logging, args.log_level),
    )

    task = args.task
    dashboard = ConsoleDashboard()

    if not task:
        print()
        print(dashboard.c("cyan",  "=" * 70))
        print(dashboard.c("bold",  "  LOCAL DESKTOP COMPUTER-USE AGENT"))
        print(dashboard.c("cyan",  "=" * 70))
        try:
            task = input(dashboard.c("yellow", "\n  Enter task: ")).strip()
        except (EOFError, KeyboardInterrupt):
            print("\nAborted.")
            sys.exit(0)

    if not task:
        print("No task provided. Exiting.")
        sys.exit(1)

    # -- Stage 1: Smart Router + Playbook Executor (4-tier) ------------------
    try:
        from router import SmartAgent
        smart = SmartAgent(
            model=config.model,
            ollama_host=config.ollama_host,
        )
        route_result = smart.run(task)
    except ImportError as exc:
        logging.warning(f"router.py not found ({exc}), skipping to vision loop.")
        route_result = {"mode": "vision_fallback"}

    tier_labels = {"cmd": "[Tier1 CMD]", "keyboard": "[Tier2 KB]", "gui": "[Tier3 GUI]"}

    # -- Stage 2: Playbook handled -- show results + continuous follow-up -----
    if route_result.get("mode") == "playbook":
        while True:
            tier       = route_result.get("tier", "cmd")
            task_id    = route_result.get("task_id", "?")
            tier_label = tier_labels.get(tier, "[Tier?]")

            print()
            print(dashboard.c("green", "=" * 60))
            print(dashboard.c("bold",  f"  DONE  {tier_label}  {task_id}"))
            print(dashboard.c("green", "=" * 60))
            for line in route_result.get("results", []):
                print(f"  {line}")
            print()

            try:
                follow_up = input(
                    dashboard.c("yellow", "  Task done! Enter another task (or blank to exit): ")
                ).strip()
            except (EOFError, KeyboardInterrupt):
                break

            if not follow_up:
                break

            route_result = smart.run(follow_up)
            if route_result.get("mode") != "playbook":
                print(dashboard.c("dim", "  (Falling back to vision agent loop)"))
                orchestrator = AgentOrchestrator(config)
                orchestrator.run(follow_up)
                break
        return

    # -- Stage 3: Vision fallback loop ----------------------------------------
    print(dashboard.c("dim", "  (Using vision agent loop for this task)"))
    orchestrator = AgentOrchestrator(config)
    orchestrator.run(task)


if __name__ == "__main__":
    main()
