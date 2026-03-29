import requests
import pytesseract
from PIL import Image
from io import BytesIO

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


class Captcha:
    def __init__(self, url):
        self.url = url
        self.image = ""
        self.value = ""

    def capture(self, session=None):
        base = self.url.rstrip("/").rsplit("/", 1)[0]
        captcha_url = base + "/captcha.php"
        response = session.get(captcha_url) if session else requests.get(captcha_url)
        self.image = Image.open(BytesIO(response.content))

    def solve(self):
        if self.image == "":
            raise ValueError("Captcha image not captured yet. Call capture() first.")
        config = "--psm 7 -c tessedit_char_whitelist=0123456789"
        self.value = pytesseract.image_to_string(self.image, config=config).strip()

    def get_value(self):
        return self.value