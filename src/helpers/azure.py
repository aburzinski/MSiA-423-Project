import sys
sys.path.append(r'C:\Users\aburz\OneDrive\Documents\Northwestern\Classes\MSiA 423\Project\MSiA-423-Project')

import logging
import os
from config import config

logging.config.fileConfig(config.LOGGING_CONFIG_FILE, disable_existing_loggers=False)
logger = logging.getLogger(__name__)

def writeFileToS3(fileName, filePath, bucket, bucketPath):

    fullPath = os.path.join(fileName, filePath)

    logger.info('Writing the following files to s3: ' + str(fullPath))

    with open(fullPath, 'rb') as data:
        bucket.put_object(Key=bucketPath + fileName, Body=data)
    data.close()
    logger.debug('Wrote {} to s3 successfully'.format(fullPath))


def writeDirToS3(dirPath, client, bucketName, bucketPath):
    files = [f for f in os.listdir(dirPath)
        if os.path.isfile(os.path.join(dirPath, f))]

    logger.info('Writing the following files to s3: ' + str(files))

    for f in files:
        with open(os.path.join(dirPath, f), 'rb') as data:
            client.put_object(Bucket=bucketName, Key=bucketPath + f, Body=data)
        data.close()
        logger.debug('Wrote {} to s3 successfully'.format(f))