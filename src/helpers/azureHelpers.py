import sys
import os
sys.path.append(os.environ.get('PYTHONPATH'))

import logging
import io
from config import config
import pandas as pd

logging.config.fileConfig(config.LOGGING_CONFIG_FILE, disable_existing_loggers=False)
logger = logging.getLogger(__name__)

def writeFileToS3(fileName, filePath, client, bucketName, bucketPath):

    fullPath = os.path.join(fileName, filePath)

    logger.info('Writing the following files to s3: ' + str(fullPath))

    with open(fullPath, 'rb') as data:
        client.put_object(Bucket=bucketName, Key=bucketPath + fileName, Body=data)
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


def readFileFromS3(fileName, client, bucketName, bucketPath):
    response = client.get_object(Bucket=bucketName, Key=bucketPath + fileName)
    return response['Body'].read().decode('utf-8')

def readDataframeFromS3(fileName, client, bucketName, bucketPath):
    response = client.get_object(Bucket=bucketName, Key=bucketPath + fileName)
    return pd.read_csv(io.BytesIO(response['Body'].read().decode('utf-8')))
