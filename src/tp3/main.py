import logging
from src.tp3.utils.session import Session, Session2

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TP3")


def main():
    logger.info("Starting TP3")

    ip = "31.220.95.27:9002"
    challenges = {
        "1": (f"http://{ip}/captcha1/", Session,  1000, 2000),
        "2": (f"http://{ip}/captcha2/", Session2, 2000, 2000),
    }

    for i, (url, SessionClass, flag_start, flag_end) in challenges.items():
        logger.info(f"Attaque du challenge {i} : {url}")

        session = SessionClass(url, flag_start=flag_start, flag_end=flag_end)
        session.prepare_request()
        session.submit_request()

        while not session.process_response():
            logger.info(f"Retry... captcha={session.captcha_value}")
            session.prepare_request()
            session.submit_request()

        logger.info("Terminé !")
        logger.info(f"Flag pour {url} : {session.get_flag()}")


if __name__ == "__main__":
    main()