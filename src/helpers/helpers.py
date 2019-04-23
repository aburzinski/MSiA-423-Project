import logging
import os
import errno
 
logger = logging.getLogger(__name__)

def silentRemove(fileName):
    try:
        os.remove(fileName)
    except OSError as e:
        if e.errno != errno.ENOENT:  # File not found error
            raise
