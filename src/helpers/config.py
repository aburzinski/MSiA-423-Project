import logging.config
from config import config

logging.config.fileConfig(config.LOGGING_CONFIG_FILE)
logger = logging.getLogger(__name__)