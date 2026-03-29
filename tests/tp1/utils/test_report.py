from unittest.mock import patch, mock_open, MagicMock
from src.tp1.utils.report import Report


def test_report_init():
    capture = MagicMock()
    filename = "test.pdf"
    summary = "Test summary"

    report = Report(capture, filename, summary)

    assert report.capture == capture
    assert report.filename == filename
    assert "Capture" in report.title
    assert report.summary == summary
    assert report.array == ""
    assert report.graph == ""


def test_concat_report():
    report = Report(MagicMock(), "test.pdf", "Test summary")
    report.title = "Test Title"
    report.array = "Test Array"
    report.graph = "Test Graph"

    result = report.concat_report()

    assert result == "Test TitleTest summaryTest ArrayTest Graph"


def test_save():
    report = Report(MagicMock(), "test.pdf", "Test summary")
    report.title = "Test Title"

    with patch("builtins.open", mock_open()) as mock_file:
        report.save("test.pdf")
        mock_file.assert_called_once_with("test.pdf", "w")
        mock_file().write.assert_called_once_with("Test TitleTest summary")


def test_generate_graph():
    report = Report(MagicMock(), "test.pdf", "Test summary")
    report.capture.sort_network_protocols.return_value = [("TCP", 50), ("UDP", 30)]

    with patch("src.tp1.utils.report.pygal.Pie") as mock_pie:
        report.generate("graph")

    assert report.graph != ""


def test_generate_array():
    report = Report(MagicMock(), "test.pdf", "Test summary")
    report.capture.sort_network_protocols.return_value = [("TCP", 50), ("UDP", 50)]
    report.capture.packet_count = 100

    report.generate("array")

    assert "TCP" in report.array
    assert "50.0%" in report.array


def test_generate_invalid_param():
    report = Report(MagicMock(), "test.pdf", "Test summary")

    report.generate("invalid")

    assert report.graph == ""
    assert report.array == ""