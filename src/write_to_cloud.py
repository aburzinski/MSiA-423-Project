import sys
sys.path.append(r'C:\Users\aburz\OneDrive\Documents\Northwestern\Classes\MSiA 423\Project\MSiA-423-Project')

import argparse
import logging.config
import os
from config import config
import src.helpers.azure as ah
import boto3

parser = argparse.ArgumentParser(description='Write files to AWS s3.')
parser.add_argument('directory', metavar='directory', type=str,
    help='historical or daily')
args = parser.parse_args()

if args.directory not in ['historical', 'daily']:
    raise ValueError('The directory argument must be either "historical" or "daily"')

parentDir = config.PROJECT_ROOT_DIR
readFromDir = os.path.join(parentDir, 'data', args.directory)

logging.config.fileConfig(config.LOGGING_CONFIG_FILE, disable_existing_loggers=False)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    session  = boto3.Session(
        aws_access_key_id=config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY
    )

    bucketName = config.AWS_S3_BUCKET_NAME
    bucketPath = 'data/{}/'.format(args.directory)

    s3 = session.client('s3')
    logger.debug('Connected to s3 successfully')
    
    logger.info('Writing to the s3 bucket ' + bucketName)
    ah.writeDirToS3(readFromDir, s3, bucketName, bucketPath)