from unittest.mock import patch
from src.tp1.utils.lib import hello_world, choose_interface


def test_when_hello_world_then_return_hello_world():
    string = "hello world"

    result = hello_world()

    assert result == string


def test_when_choose_interface_then_return_empty_string():
    with (
        patch("src.tp1.utils.lib.get_if_list", return_value=["eth0", "wlan0"]),
        patch("builtins.input", return_value="1"),
    ):
        result = choose_interface()

    assert result == "eth0"