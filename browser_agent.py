"""Browser agent: observe -> ask the model for ONE action -> act -> repeat."""

import json
import re

from dom_snapshot import snapshot

ALLOWED = {"goto", "click", "type", "scroll", "done", "fail"}

# If the element we are about to click/type into contains one of these, ask the user first.
RISKY_WORDS = ("buy", "pay", "purchase", "delete", "remove", "sign out",
               "log out", "place order", "confirm order")

SYSTEM_PROMPT = """You control a web browser to reach a goal.
Each turn you see the current page as a numbered list of elements.
Reply with exactly ONE JSON action:
{"action": "goto", "url": "example.com"}
{"action": "click", "id": 3}
{"action": "type", "id": 5, "text": "hello", "submit": true}
{"action": "scroll", "direction": "down"}
{"action": "done", "summary": "what you did or found"}
{"action": "fail", "reason": "why it is impossible"}
Use only ids that appear in the list. Reply with JSON only."""


def ollama_decider(model: str, host: str = "http://localhost:11434"):
    """The ONLY place that talks to the LLM. Tests replace this with a fake."""
    import ollama
    client = ollama.Client(host=host)

    def decide(goal: str, observation: str, history: list[str]) -> str:
        recent = "\n".join(history[-5:]) or "none"
        user = (f"Goal: {goal}\n\nRecent actions:\n{recent}\n\n"
                f"Current page:\n{observation}\n\nNext action as JSON:")
        resp = client.chat(
            model=model,
            format="json",
            options={"temperature": 0},
            messages=[{"role": "system", "content": SYSTEM_PROMPT},
                      {"role": "user", "content": user}],
        )
        return resp["message"]["content"]

    return decide


def parse_action(raw: str):
    """Turn the model's reply into an action dict, or None if it is unusable."""
    try:
        data = json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        m = re.search(r"\{.*\}", str(raw), re.S)  # model added extra text around the JSON
        if not m:
            return None
        try:
            data = json.loads(m.group(0))
        except json.JSONDecodeError:
            return None
    if not isinstance(data, dict) or data.get("action") not in ALLOWED:
        return None
    return data


class BrowserAgent:
    def __init__(self, engine, decide, max_steps: int = 8, confirm=input):
        self.engine = engine
        self.decide = decide        # function(goal, observation, history) -> raw reply string
        self.max_steps = max_steps
        self.confirm = confirm      # function(prompt) -> answer string

    def _label(self, element_id) -> str:
        for e in snapshot(self.engine.page):
            if e["id"] == element_id:
                return e["text"].lower()
        return ""

    def _is_risky(self, a: dict) -> bool:
        if a["action"] not in ("click", "type"):
            return False
        try:
            label = self._label(int(a["id"]))
        except (KeyError, ValueError, TypeError):
            return False
        return any(w in label for w in RISKY_WORDS)

    def _execute(self, a: dict) -> str:
        act = a["action"]
        if act == "goto":
            return self.engine.goto(str(a["url"]))
        if act == "click":
            return self.engine.click(int(a["id"]))
        if act == "type":
            return self.engine.type_text(int(a["id"]), str(a["text"]),
                                         bool(a.get("submit", False)))
        return self.engine.scroll(a.get("direction", "down"))

    def run(self, goal: str) -> dict:
        history: list[str] = []
        for step in range(1, self.max_steps + 1):
            observation = self.engine.observe()
            action = parse_action(self.decide(goal, observation, history))

            if action is None:
                history.append("Your last reply was not a valid action. Reply with one JSON action.")
                continue
            if action["action"] == "done":
                return {"status": "done", "summary": action.get("summary", ""), "steps": step}
            if action["action"] == "fail":
                return {"status": "failed", "reason": action.get("reason", ""), "steps": step}

            if self._is_risky(action):
                answer = self.confirm(f"Agent wants to do {action}. Allow? (y/n): ")
                if not str(answer).lower().startswith("y"):
                    history.append(f"User refused {action}. Choose a different action.")
                    continue

            try:
                history.append(f"{action} -> {self._execute(action)}")
            except Exception as exc:  # bad id, timeout, etc. Tell the model and let it retry
                history.append(f"{action} FAILED: {exc}")

        return {"status": "max_steps", "steps": self.max_steps}