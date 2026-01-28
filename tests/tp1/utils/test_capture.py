from unittest.mock import patch, MagicMock
from src.tp1.utils.capture import Capture
from scapy.layers.inet import IP, TCP, UDP, ICMP
from scapy.layers.l2 import Ether, ARP


def test_capture_init():
    # When
    with patch("src.tp1.utils.capture.choose_interface", return_value="eth0"):
        capture = Capture()

    # Then
    assert capture.interface == "eth0"
    assert capture.summary == ""
    assert capture.packet_count == 0
    assert capture.protocol_stats == {}


def test_capture_trafic():
    # Given
    with patch("src.tp1.utils.capture.choose_interface", return_value="eth0"):
        capture = Capture()

    # When
    with patch("src.tp1.utils.capture.sniff"):
        capture.capture_traffic(packet_count=10)

    # Then
    # This is a minimal test since the method doesn't do much yet
    assert capture.interface == "eth0"


def test_sort_network_protocols():
    # Given
    with patch("src.tp1.utils.capture.choose_interface", return_value="eth0"):
        capture = Capture()
    capture.protocol_stats = {"TCP": 50, "UDP": 30, "ARP": 20}

    # When
    result = capture.sort_network_protocols()

    # Then
    assert result == [("TCP", 50), ("UDP", 30), ("ARP", 20)]


def test_get_all_protocols():
    # Given
    with patch("src.tp1.utils.capture.choose_interface", return_value="eth0"):
        capture = Capture()
    capture.protocol_stats = {"TCP": 50, "UDP": 30}

    # When
    result = capture.get_all_protocols()

    # Then
    assert result == {"TCP": 50, "UDP": 30}
    #assert result is None  # Method currently returns None


def test_analyse():
    # Given
    with patch("src.tp1.utils.capture.choose_interface", return_value="eth0"):
        capture = Capture()

    # When
    with (
        patch.object(capture, "get_all_protocols") as mock_get_protocols,
        patch.object(capture, "sort_network_protocols") as mock_sort,
        patch.object(capture, "gen_summary") as mock_gen_summary,
    ):
        mock_gen_summary.return_value = "Test summary"
        capture.analyse("tcp")

    # Then
    mock_get_protocols.assert_called_once()
    mock_sort.assert_called_once()
    mock_gen_summary.assert_called_once()
    assert capture.summary == "Test summary"


def test_get_summary():
    # Given
    with patch("src.tp1.utils.capture.choose_interface", return_value="eth0"):
        capture = Capture()
    capture.summary = "Test summary"

    # When
    result = capture.get_summary()

    # Then
    assert result == "Test summary"


def test_gen_summary():
    # Given
    with patch("src.tp1.utils.capture.choose_interface", return_value="eth0"):
        capture = Capture()
    capture.interface = "eth0"
    capture.packet_count = 100
    capture.packets = [MagicMock()]
    capture.protocol_stats = {"TCP": 50, "UDP": 50}

    # When
    result = capture.gen_summary()

    # Then
    assert "Interface: eth0" in result
    #assert result == ""  # Method currently returns empty string
