from unittest.mock import patch, mock_open, MagicMock
import pytest
from src.tp1.utils.report import Report


def test_report_init():
    # Given
    capture = MagicMock()
    filename = "test.pdf"
    summary = "Test summary"

    # When
    report = Report(capture, filename, summary)

    # Then
    assert report.capture == capture
    assert report.filename == filename
    assert "Capture" in report.title
    assert report.summary == summary


def test_concat_report():
    # Given
    report = Report(MagicMock(), "test.pdf", "Test summary")
    report.title = "Test Title"
    report.array = "Test Array"
    report.graph = "Test Graph"

    # When
    result = report.concat_report()

    # Then
    assert result == "Test TitleTest summaryTest ArrayTest Graph"


def test_save():
    # Given
    report = Report(MagicMock(), "test.pdf", "Test summary")
    report.title = "Test Title"
    report.array = ""
    report.graph = ""

    # When/Then
    with patch("builtins.open", mock_open()) as mock_file:
        report.save("test.pdf")

        # Verify file was opened with correct name
        mock_file.assert_called_once_with("test.pdf", "w")

        # Verify write was called with the concatenated content
        mock_file().write.assert_called_once_with("Test TitleTest summary")


def test_generate_raises_attribute_error():
    # Given
    report = Report(MagicMock(), "test.pdf", "Test summary")

    # When / Then
    with pytest.raises(AttributeError):
        report.generate()
