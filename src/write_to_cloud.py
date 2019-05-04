import logging.config
import os

currentDir = os.path.dirname(__file__)
parentDir = os.path.split(currentDir)[0]
readFromDir = os.path.join(parentDir, 'data', 'historical')

logging.config.fileConfig(os.path.join(parentDir, 'config', 'logging', 'local.conf'))
logger = logging.getLogger(__name__)