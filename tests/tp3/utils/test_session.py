from unittest.mock import MagicMock, patch
from src.tp3.utils.session import Session, Session2


def test_session_init():
    # Given
    url = "http://example.com/captcha"

    # When
    session = Session(url)

    # Then
    assert session.url == url
    assert session.captcha_value == ""
    assert session.flag_value == 1000
    assert session.valid_flag == ""


def test_submit_request():
    # Given
    session = Session("http://example.com/captcha")
    session.captcha_value = "652047"
    session.http_session.post = MagicMock(return_value=MagicMock())

    # When
    session.submit_request()

    # Then
    session.http_session.post.assert_called_once_with(
        "http://example.com/captcha",
        data={"flag": "1000", "captcha": "652047", "submit": "Submit"},
    )


def test_process_response():
    # Given
    session = Session("http://example.com/captcha")
    session.response = MagicMock()
    session.response.text = "<html>Incorrect flag.</html>"

    # When
    result = session.process_response()

    # Then
    assert result is False


def test_get_flag():
    # Given
    session = Session("http://example.com/captcha")
    session.valid_flag = "FLAG123"

    # When
    result = session.get_flag()

    # Then
    assert result == "FLAG123"


def test_session2_process_response_warning():
    # Given
    session = Session2("http://example.com/captcha", flag_start=2000, flag_end=2000)
    session.response = MagicMock()
    session.response.text = "<html><b>Warning</b>: Undefined array key</html>"

    # When
    result = session.process_response()

    # Then
    assert result is False


def test_session2_process_response_flag_found():
    # Given
    session = Session2("http://example.com/captcha", flag_start=2000, flag_end=2000)
    session.response = MagicMock()
    session.response.text = "<html>...</html>\nuLNbF"

    # When
    result = session.process_response()

    # Then
    assert result is True
    assert session.valid_flag == "uLNbF"