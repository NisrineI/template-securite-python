import logging
import os

log_path = os.path.join(os.path.dirname(__file__), "tp2_app.log")
handlers = [logging.StreamHandler()]
try:
    handlers.insert(0, logging.FileHandler(log_path, mode="a"))
except PermissionError:
    pass

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=handlers,
)

logger = logging.getLogger("TP2")