from unittest.mock import MagicMock, patch
from PIL import Image
import io
from src.tp3.utils.captcha import Captcha


def test_captcha_init():
    # Given
    url = "http://example.com/captcha"

    # When
    captcha = Captcha(url)

    # Then
    assert captcha.url == url
    assert captcha.image == ""
    assert captcha.value == ""


def test_solve():
    # Given
    captcha = Captcha("http://example.com/captcha")
    captcha.image = Image.new("RGB", (100, 30), color=(255, 255, 255))

    # When
    with patch("src.tp3.utils.captcha.pytesseract.image_to_string", return_value="652047\n"):
        captcha.solve()

    # Then
    assert captcha.value == "652047"


def test_capture():
    # Given
    captcha = Captcha("http://example.com/captcha")

    img = Image.new("RGB", (100, 30), color=(0, 0, 255))
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="PNG")
    img_bytes.seek(0)

    mock_session = MagicMock()
    mock_session.get.return_value = MagicMock(content=img_bytes.read())

    # When
    captcha.capture(session=mock_session)

    # Then
    assert isinstance(captcha.image, Image.Image)


def test_get_value():
    # Given
    captcha = Captcha("http://example.com/captcha")
    captcha.value = "TEST123"

    # When
    result = captcha.get_value()

    # Then
    assert result == "TEST123"