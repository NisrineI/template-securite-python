from src.tp1.utils.lib import hello_world, choose_interface
from unittest.mock import patch


def test_when_hello_world_then_return_hello_world():
    # Given
    string = "hello world"

    # When
    result = hello_world()

    # Then
    assert result == string


def test_when_choose_interface_then_return_empty_string():
    # When
    with (
        patch("scapy.arch.get_if_list", return_value=["eth0", "wlan0"]),
        patch("builtins.input", return_value="1"),
    ):
        result = choose_interface()

    # Then
    assert result == "eth0"
