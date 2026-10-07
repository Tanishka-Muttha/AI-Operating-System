import pytest
from router import classify_by_rules


def task(text):
    return classify_by_rules(text)[0]


@pytest.mark.parametrize("text, expected", [
    ("open notepad", "open_notepad"),
    ("show my ip address", "show_ip_address"),
    ("calculate 42 * 7", "calculator_compute"),
    ("mute the volume", "mute_volume"),
    ("increase volume", "volume_up"),
    ("take a screenshot", "take_screenshot"),
    ("search python tutorials on google", "google_search"),
    ("write a letter to my teacher", "write_document_word"),
    ("ping google.com", "ping_host"),
    ("I need a minute to think", "unknown"),
])
def test_commands_that_already_work(text, expected):
    assert task(text) == expected


def test_shopping_is_not_ping():
    assert task("add milk to my shopping list") != "ping_host"


def test_shutdown_the_computer():
    assert task("shutdown the computer") == "shutdown_computer"


def test_restart_the_computer():
    assert task("restart the computer") == "restart_computer"


def test_question_about_shutdown_is_not_an_order():
    assert task("how to shutdown a pc properly") != "shutdown_computer"