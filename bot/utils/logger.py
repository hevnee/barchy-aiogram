import os
import logging
from config import BotConfigs

file_name = BotConfigs.LOGGING_FILE

os.makedirs(os.path.dirname(file_name), exist_ok=True)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s %(levelname)s]: %(message)s', datefmt='%H:%M:%S')

file_handler = logging.FileHandler(file_name)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)