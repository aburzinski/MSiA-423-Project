import sys
sys.path.append(r'C:\Users\aburz\OneDrive\Documents\Northwestern\Classes\MSiA 423\Project\MSiA-423-Project')

import logging.config
import os
from config import config
import src.helpers.azure as ah
import boto3

parentDir = config.PROJECT_ROOT_DIR
readFromDir = os.path.join(parentDir, 'data', 'historical')

logging.config.fileConfig(config.LOGGING_CONFIG_FILE, disable_existing_loggers=False)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    session  = boto3.Session(
        aws_access_key_id=config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY
    )

    bucketName = config.AWS_S3_BUCKET_NAME
    bucketPath = 'data/historical/'

    s3 = session.resource('s3')
    logger.debug('Connected to s3 successfully')

    bucket = s3.Bucket(bucketName)
    logger.info('Writing to the s3 bucket ' + bucketName)

    ah.writeDirToS3(readFromDir, bucket, bucketPath)