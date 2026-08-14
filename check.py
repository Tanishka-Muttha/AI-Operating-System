import sys
sys.path.insert(0, ".")

from playbooks     import CMD_PLAYBOOKS, KEYBOARD_PLAYBOOKS, ALL_PLAYBOOKS
from gui_playbooks import GUI_PLAYBOOKS

print("=" * 55)
print("  PLAYBOOK LIBRARY SUMMARY")
print("=" * 55)
print(f"  Tier 1 (cmd)      : {len(CMD_PLAYBOOKS):>3} tasks")
print(f"  Tier 2 (keyboard) : {len(KEYBOARD_PLAYBOOKS):>3} tasks")
print(f"  Tier 3 (gui)      : {len(GUI_PLAYBOOKS):>3} tasks")
print(f"  {'─'*35}")
print(f"  TOTAL             : {len(ALL_PLAYBOOKS) + len(GUI_PLAYBOOKS):>3} tasks")
print()

print("  Tier 1 — CMD tasks:")
for tid in CMD_PLAYBOOKS:
    print(f"    ⚙️  {tid}")

print()
print("  Tier 2 — KEYBOARD tasks:")
for tid in KEYBOARD_PLAYBOOKS:
    print(f"    ⌨️  {tid}")

print()
print("  Tier 3 — GUI tasks:")
for tid in GUI_PLAYBOOKS:
    print(f"    🖱️  {tid}")

print()
print("=" * 55)
print("  All playbooks imported successfully!")
