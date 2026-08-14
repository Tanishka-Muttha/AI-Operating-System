"""
Simulate: "open word and write a letter to principal of my college about her resignation"
Tests the full routing → param extraction → AI content generation → GUI steps pipeline
WITHOUT actually running pyautogui (dry run mode).
"""
import json, sys
sys.path.insert(0, ".")

print("=" * 65)
print("  DRY RUN TEST — AI Letter Writing Pipeline")
print("=" * 65)

# ── Step 1: Test the router classifies correctly ─────────────────────
print("\n[1] Testing router classification...")
from router import TaskRouter

USER_TASK = "open word and write a letter to principal of my college about her resignation"
print(f"    Task: {USER_TASK!r}")

router = TaskRouter(model="gemma4:e2b")
result = router.route(USER_TASK)

print(f"\n    task_id    : {result.get('task_id')}")
print(f"    tier       : {result.get('tier')}")
print(f"    confidence : {result.get('confidence')}")
print(f"    reason     : {result.get('reason')}")
print(f"\n    PARAMS:")
for k, v in result.get("params", {}).items():
    print(f"      {k} = {str(v)[:120]}")

# ── Step 2: Confirm playbook lookup ──────────────────────────────────
print("\n[2] Looking up playbook...")
from gui_playbooks import GUI_PLAYBOOKS
from playbooks import ALL_PLAYBOOKS

task_id = result.get("task_id", "unknown")
playbook = GUI_PLAYBOOKS.get(task_id) or ALL_PLAYBOOKS.get(task_id)

if playbook:
    steps = playbook.get("steps", [])
    print(f"    Found: {task_id}  ({len(steps)} steps)")
    print(f"    Desc : {playbook.get('description')}")
    print(f"\n    Steps:")
    for i, s in enumerate(steps, 1):
        stype = s.get("type", "?")
        label = s.get("label", "")
        if stype == "generate_content":
            prompt_preview = s.get("prompt", "")[:60]
            print(f"      [{i}] {stype:20s} -> AI prompt: {prompt_preview!r}  [param_name={s.get('param_name')}]")
        elif stype == "type_clip":
            print(f"      [{i}] {stype:20s} -> text: {s.get('text', '')!r}")
        else:
            print(f"      [{i}] {stype:20s} -> {label}")
else:
    print(f"    No playbook found for: {task_id!r}")

# ── Step 3: Test AI content generation ───────────────────────────────
params = result.get("params", {})
content_request = params.get("content_request", "")

if content_request:
    print(f"\n[3] Testing AI content generation...")
    print(f"    Prompt being sent to LLM:")
    print(f"    {content_request[:200]}")
    print(f"\n    (Calling Ollama to generate letter...)")

    import ollama
    client = ollama.Client(host="http://localhost:11434")
    resp = client.chat(
        model="gemma4:e2b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a professional content writer. Generate exactly what is requested.\n"
                    "Output ONLY the content itself. No preamble like 'Here is the letter:'.\n"
                    "Just the pure, ready-to-use document text, correctly formatted.\n"
                    "Use proper formatting: blank lines between paragraphs, correct salutations."
                )
            },
            {"role": "user", "content": content_request}
        ],
        options={"temperature": 0.7, "num_predict": 2048, "top_p": 0.95}
    )
    generated = resp.message.content.strip()

    print(f"\n    Generated {len(generated)} characters of content:")
    print("-" * 65)
    print(generated[:1500])
    if len(generated) > 1500:
        print(f"\n    ... [{len(generated) - 1500} more characters]")
    print("-" * 65)

    print(f"\n[4] Summary:")
    print(f"    task_id    : {task_id}")
    print(f"    filename   : {params.get('filename', 'NOT SET')}")
    print(f"    content_len: {len(generated)} chars")
    print(f"\n  PIPELINE WORKS. In real run:")
    print(f"  -> Word opens -> Ctrl+N -> content pasted -> Ctrl+S -> saved as {params.get('filename', '?')}")
else:
    print(f"\n[3] WARN: No content_request in params. Router may need tuning.")
    print(f"    Params received: {params}")

print("\n" + "=" * 65)
print("  TEST COMPLETE")
print("=" * 65)
