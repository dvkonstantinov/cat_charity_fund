import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s, %(levelname)s, %(message)s'
)
handler = RotatingFileHandler('logs.log', maxBytes=50000000, backupCount=5)
handler.setFormatter(formatter)
logger.addHandler(handler)
