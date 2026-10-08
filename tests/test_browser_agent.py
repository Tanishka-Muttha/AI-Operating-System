import json
import pytest
from playwright.sync_api import sync_playwright

from cdp_engine import BrowserEngine
from browser_agent import BrowserAgent, parse_action

PAGE = """
<input id="q" placeholder="Search">
<button onclick="out.innerText='Searched: ' + q.value">Go</button>
<button onclick="out.innerText='BOUGHT'">Buy now</button>
<div id="out"></div>
"""


@pytest.fixture
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        pg = browser.new_page()
        pg.set_content(PAGE)
        yield pg
        browser.close()


def scripted(replies):
    """Fake model: returns the given replies one by one."""
    it = iter(replies)
    return lambda goal, obs, hist: next(it) if isinstance(replies[0], str) else json.dumps(next(it))


def fake(*actions):
    it = iter(actions)
    return lambda goal, obs, hist: next(it) if isinstance(actions[0], str) else json.dumps(next(it))


def test_parse_action_handles_extra_text():
    raw = 'Sure! {"action": "click", "id": 2} hope that helps'
    assert parse_action(raw) == {"action": "click", "id": 2}


def test_parse_action_rejects_unknown_action():
    assert parse_action('{"action": "hack_pentagon"}') is None
    assert parse_action("not json at all") is None


def test_agent_types_clicks_and_finishes(page):
    decide = fake({"action": "type", "id": 0, "text": "python"},
                  {"action": "click", "id": 1},
                  {"action": "done", "summary": "searched"})
    result = BrowserAgent(BrowserEngine(page), decide).run("search python")
    assert result["status"] == "done"
    assert page.inner_text("#out") == "Searched: python"


def test_risky_click_is_blocked_when_user_says_no(page):
    decide = fake({"action": "click", "id": 2},
                  {"action": "done", "summary": "gave up"})
    agent = BrowserAgent(BrowserEngine(page), decide, confirm=lambda prompt: "n")
    result = agent.run("buy something")
    assert result["status"] == "done"
    assert page.inner_text("#out") != "BOUGHT"


def test_invalid_reply_is_retried(page):
    decide = fake("garbage", '{"action": "done", "summary": "ok"}')
    result = BrowserAgent(BrowserEngine(page), decide).run("anything")
    assert result["status"] == "done"


def test_stops_after_max_steps(page):
    decide = lambda goal, obs, hist: '{"action": "scroll", "direction": "down"}'
    result = BrowserAgent(BrowserEngine(page), decide, max_steps=3).run("loop forever")
    assert result["status"] == "max_steps"