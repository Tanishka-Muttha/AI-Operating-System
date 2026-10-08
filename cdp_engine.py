"""Action engine: performs actions on a web page using the element ids from dom_snapshot."""

from dom_snapshot import snapshot, snapshot_text


class BrowserEngine:
    def __init__(self, page):
        self.page = page

    # ---- helpers ----------------------------------------------------
    def _el(self, agent_id: int):
        loc = self.page.locator(f'[data-agent-id="{agent_id}"]')
        if loc.count() == 0:
            raise ValueError(
                f"Element [{agent_id}] not found. The page changed, call observe() again."
            )
        return loc.first

    def find(self, text: str | None = None, tag: str | None = None, type: str | None = None):
        """Return the id of the first visible element matching all given filters, else None."""
        for e in snapshot(self.page):
            if tag and e["tag"] != tag:
                continue
            if type and e["type"] != type:
                continue
            if text and text.lower() not in e["text"].lower():
                continue
            return e["id"]
        return None

    # ---- actions ----------------------------------------------------
    def goto(self, url: str) -> str:
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        self.page.goto(url, wait_until="domcontentloaded")
        return f"opened {url}"

    def click(self, agent_id: int) -> str:
        self._el(agent_id).click(timeout=5000)
        self.page.wait_for_load_state("domcontentloaded")
        return f"clicked [{agent_id}]"

    def type_text(self, agent_id: int, text: str, submit: bool = False) -> str:
        el = self._el(agent_id)
        el.fill(text, timeout=5000)
        if submit:
            el.press("Enter")
            self.page.wait_for_load_state("domcontentloaded")
        return f"typed into [{agent_id}]" + (" and pressed Enter" if submit else "")

    def scroll(self, direction: str = "down", amount: int = 600) -> str:
        self.page.mouse.wheel(0, amount if direction == "down" else -amount)
        return f"scrolled {direction}"

    # ---- eyes -------------------------------------------------------
    def observe(self, limit: int = 60) -> str:
        """Fresh numbered list of what is on the page right now."""
        return snapshot_text(self.page, limit)