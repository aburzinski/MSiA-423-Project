import sys
sys.path.append(r'C:\Users\aburz\OneDrive\Documents\Northwestern\Classes\MSiA 423\Project\MSiA-423-Project')

import logging.config
import os
from config import config
import boto3

currentDir = os.path.dirname(__file__)
parentDir = config.PROJECT_ROOT_DIR
readFromDir = os.path.join(parentDir, 'data', 'historical')

logging.config.fileConfig(config.LOGGING_CONFIG_FILE)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    session  = boto3.Session(
        aws_access_key_id=config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY
    )

    bucketName = config.AWS_S3_BUCKET_NAME
    bucketPath = 'data/historical/'

    s3 = session.resource('s3')
    bucket = s3.Bucket(bucketName)
    logger.info('Writing to the s3 bucket ' + bucketName)

    files = [f for f in os.listdir(readFromDir)
        if os.path.isfile(os.path.join(readFromDir, f))]

    logger.info('Writing the following files to s3: ' + str(files))

    for f in files:
        with open(os.path.join(readFromDir, f), 'rb') as data:
            bucket.put_object(Key=bucketPath + f, Body=data)
        data.close()
        logger.debug('Wrote {} to s3 successfully'.format(f))