# Local Desktop Computer-Use Agent

A production-grade, 100% local, zero-cost Desktop Computer-Use Agent framework.
Mirrors Anthropic's Claude Computer-Use architecture but runs entirely offline via
**Ollama + gemma2:7b** (vision-capable), **pyautogui**, and **mss**.

---

## Architecture

```
Human Controller (Terminal)
        │
        ▼
AgentOrchestrator (State Machine Loop)
   ├── ScreenCaptureEngine   (mss → PIL downscale → base64 JPEG)
   ├── VisualMemoryPruner    (strips old images, keeps text transcript)
   ├── OllamaVisionBrain     (gemma2:7b, format=json, retry logic)
   ├── ToolExecutor          (pyautogui dispatcher + coord clamping)
   └── ConsoleDashboard      (ANSI status dashboard per iteration)
```

---

## Setup

### 1. Install Ollama
Download from https://ollama.com and run:
```bash
ollama serve
ollama pull gemma2:7b
```

### 2. Install Python dependencies
```bash
pip install -r requirements.txt
```

---

## Usage

```bash
# Basic usage
python agent.py --task "Open Notepad and type Hello World"

# Interactive mode (no task flag — prompts you)
python agent.py

# Use a lighter model
python agent.py --model gemma2:2b --task "Open the file manager"

# Custom settings
python agent.py \
  --task "Search Google for Python tutorials" \
  --max-iter 15 \
  --delay 2.0 \
  --width 800 \
  --log-level DEBUG
```

### All CLI flags

| Flag | Default | Description |
|------|---------|-------------|
| `--task` / `-t` | *(prompt)* | Task for the agent to perform |
| `--model` / `-m` | `gemma2:7b` | Ollama model name |
| `--max-iter` | `20` | Hard iteration cap for the session |
| `--stall` | `5` | Consecutive same-actions before human handoff |
| `--delay` | `1.5` | Seconds to wait after each action (UI settle) |
| `--width` | `1024` | Max screenshot width before downscale (px) |
| `--host` | `http://localhost:11434` | Ollama server URL |
| `--monitor` | `1` | Monitor index (1 = primary) |
| `--log-level` | `INFO` | Console log verbosity |

---

## JSON Action Schema

The model always responds with this strict JSON structure:

```json
{
  "thought": "Step-by-step reasoning about what I see",
  "action": "left_click",
  "coordinate": [540, 320],
  "text": null
}
```

### Available actions

| Action | Needs `coordinate` | Needs `text` | Description |
|--------|-------------------|--------------|-------------|
| `mouse_move` | ✅ | ❌ | Move cursor (no click) |
| `left_click` | ✅ | ❌ | Single left click |
| `right_click` | ✅ | ❌ | Single right click |
| `double_click` | ✅ | ❌ | Double left click |
| `type` | ❌ | ✅ | Type text at cursor |
| `hotkey` | ❌ | ✅ | Key combo (e.g. `ctrl+s`) |
| `scroll` | ✅ | `"up"`/`"down"` | Scroll at position |
| `wait` | ❌ | ❌ | Pause for UI animation |
| `done` | ❌ | ❌ | Signal task complete |

---

## Key Design Features

### Visual Memory Pruning
Local 7B models have tight context windows (~8k tokens). The `VisualMemoryPruner`
automatically strips image bytes from all messages except the most recent one.
Only text transcripts of older steps are retained, slashing token usage by ~95%.

### Coordinate Scaling
The model sees a downscaled 1024px-wide screenshot. The `ToolExecutor` automatically
maps those coordinates back to actual screen resolution before calling pyautogui.

### Human Handoff
The orchestrator pauses and prompts you in the terminal when:
- The model returns `"action": "done"` (task complete — what next?)
- The same action repeats `--stall` times consecutively (stuck — need guidance?)

### Safety
- PyAutoGUI fail-safe: move mouse to **top-left corner** to immediately abort
- `Ctrl+C` is caught gracefully with a session summary
- All coordinates are hard-clamped to screen bounds before execution

---

## Log Files

Detailed DEBUG logs are written to `logs/agent_YYYYMMDD_HHMMSS.log` automatically.

---

## Requirements

- Python 3.10+
- Ollama running locally (`ollama serve`)
- `gemma2:7b` pulled (`ollama pull gemma2:7b`)
- Windows / macOS / Linux desktop environment
