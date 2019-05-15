import os
import sys
sys.path.append(os.environ.get('PYTHONPATH'))

import logging.config
from config import config
import requests
import src.helpers.helpers as h
import src.helpers.azureHelpers as ah

parentDir = config.PROJECT_ROOT_DIR
logging.config.fileConfig(config.LOGGING_CONFIG_FILE, disable_existing_loggers=False)
logger = logging.getLogger(__name__)

if __name__ == '__main__':

    bucketName = config.HISTORICAL_S3_BUCKET_NAME
    bucketPath = 'data/'

    filesToDownload = ['hittingHistorical.csv',
        'pitchingHistorical.csv', 'players.csv', 'teams.csv']

    logger.info('Reading from the s3 bucket ' + bucketName)

    for file in filesToDownload:
        bucketURL = 'https://{}.s3.amazonaws.com/{}{}'.format(bucketName, bucketPath, file) 
        response = requests.get(bucketURL)

        fileName = os.path.join(parentDir, 'data', 'historical', file)
        h.silentCreateDir(os.path.join(parentDir, 'data', 'historical'))
        h.silentRemove(fileName)
        with open(fileName, 'wb') as f:
            f.write(response.content)
        f.close()
        logger.info('{} downloaded successfully'.format(file))