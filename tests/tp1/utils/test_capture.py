from unittest.mock import patch, MagicMock
from src.tp1.utils.capture import Capture


def test_capture_init():
    with patch("src.tp1.utils.capture.choose_interface", return_value="eth0"):
        capture = Capture()

    assert capture.interface == "eth0"
    assert capture.summary == ""


def test_capture_traffic():
    with patch("src.tp1.utils.capture.choose_interface", return_value="eth0"):
        capture = Capture()

    with patch("src.tp1.utils.capture.sniff"):
        capture.capture_traffic()

    assert capture.interface == "eth0"


def test_sort_network_protocols():
    with patch("src.tp1.utils.capture.choose_interface", return_value="eth0"):
        capture = Capture()
    capture.protocol_stats = {"TCP": 50, "UDP": 30, "ARP": 20}

    result = capture.sort_network_protocols()

    assert result == [("TCP", 50), ("UDP", 30), ("ARP", 20)]


def test_get_all_protocols():
    with patch("src.tp1.utils.capture.choose_interface", return_value="eth0"):
        capture = Capture()
    capture.protocol_stats = {"TCP": 50, "UDP": 30}

    result = capture.get_all_protocols()

    assert result == {"TCP": 50, "UDP": 30}


def test_analyse():
    with patch("src.tp1.utils.capture.choose_interface", return_value="eth0"):
        capture = Capture()

    with (
        patch.object(capture, "get_all_protocols") as mock_get_protocols,
        patch.object(capture, "sort_network_protocols") as mock_sort,
        patch.object(capture, "gen_summary") as mock_gen_summary,
    ):
        mock_gen_summary.return_value = "Test summary"
        capture.analyse("tcp")

    mock_get_protocols.assert_called_once()
    mock_sort.assert_called_once()
    mock_gen_summary.assert_called_once()
    assert capture.summary == "Test summary"


def test_get_summary():
    with patch("src.tp1.utils.capture.choose_interface", return_value="eth0"):
        capture = Capture()
    capture.summary = "Test summary"

    assert capture.get_summary() == "Test summary"


def test_gen_summary():
    with patch("src.tp1.utils.capture.choose_interface", return_value="eth0"):
        capture = Capture()
    capture.interface = "eth0"
    capture.packet_count = 100
    capture.protocol_stats = {"TCP": 50, "UDP": 50}

    result = capture.gen_summary()

    assert "Interface: eth0" in result
    assert "Total paquets: 100" in result
    assert "TCP" in result