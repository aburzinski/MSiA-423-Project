import logging.config
import os
import errno
from config import config

logging.config.fileConfig(config.LOGGING_CONFIG_FILE)
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


def writeIterLine(iter, f):
    """Take an iterator of strings and create one line of a csv from them
    Args:
        iter (An iterator of `str` objects): An iterator of string objects
            Created wither from dict keys or dict values
        f (file object): The file to write to
    """
    elems = []
    for elem in iter:
        elems.append(elem)
    f.write('"' + '","'.join(elems) + '"\n')