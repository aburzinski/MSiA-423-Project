import logging
import os
import errno

logging.basicConfig(level=logging.DEBUG,
    format='%(name)s - %(levelname)s - %(asctime)s - %(message)s'
) 

logger = logging.getLogger(__name__)

def silentRemove(fileName):
    try:
        os.remove(fileName)
	logger.debug('Removed file ' + filename)
    except OSError as e:
        if e.errno != errno.ENOENT:  # File not found error
            raise
	else:
	    logger.debug('File not deleted since it doesn't exist')
