import logging
import os
import errno

logging.basicConfig(level=logging.DEBUG,
    format='%(name)s - %(levelname)s - %(asctime)s - %(message)s'
) 

logger = logging.getLogger(__name__)

def silentRemove(fileName):
    """ Delete file if it exists, other don't do anything """
    try:
        os.remove(fileName)
        logger.debug('Removed file ' + fileName)
    except OSError as e:
        if e.errno != errno.ENOENT:  # File not found error
            raise
        else:
            logger.debug('File not deleted since it doesn\'t exist')


def silentCreateDir(dirName):
    """ Create directory if it doesn't already exist """
    if not os.path.exists(dirName):
        os.makedirs(dirName)
        logger.debug('Created directory ' + dirName)