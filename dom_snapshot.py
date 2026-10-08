"""DOM subagent: turns a web page into a short list of things the agent can act on."""

_JS = """
() => {
  const sel = 'a, button, input, textarea, select, [role="button"], [role="link"]';
  const out = [];
  let i = 0;
  document.querySelectorAll(sel).forEach(el => {
    const r = el.getBoundingClientRect();
    const s = getComputedStyle(el);
    if (r.width < 2 || r.height < 2 || s.visibility === 'hidden' || s.display === 'none') return;
    el.setAttribute('data-agent-id', i);
    out.push({
      id: i,
      tag: el.tagName.toLowerCase(),
      type: el.getAttribute('type') || '',
      text: (el.innerText || el.value || el.getAttribute('aria-label')
             || el.getAttribute('placeholder') || el.title || '').trim().slice(0, 80),
      href: el.getAttribute('href') || ''
    });
    i++;
  });
  return out;
}
"""


def snapshot(page) -> list[dict]:
    """Visible interactive elements. Each one is tagged data-agent-id so we can click it by number."""
    return page.evaluate(_JS)


def snapshot_text(page, limit: int = 60) -> str:
    """Compact text version, small enough to give to a small LLM."""
    lines = []
    for e in snapshot(page)[:limit]:
        kind = e["tag"] + (f"/{e['type']}" if e["type"] else "")
        link = f"  -> {e['href'][:60]}" if e["href"] else ""
        lines.append(f"[{e['id']}] {kind}: {e['text']}{link}")
    return "\n".join(lines)