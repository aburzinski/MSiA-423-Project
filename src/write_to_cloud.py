import logging.config
import os
import configparser
import boto3

currentDir = os.path.dirname(__file__)
parentDir = os.path.split(currentDir)[0]
readFromDir = os.path.join(parentDir, 'data', 'historical')

config = configparser.ConfigParser()
config.read(os.path.join(parentDir, 'azureConfig.ini'))

logging.config.fileConfig(os.path.join(parentDir, 'config', 'logging', 'local.conf'))
logger = logging.getLogger(__name__)

session = boto3.Session(
    aws_access_key_id=config['DEFAULT']['aws_access_key_id'],
    aws_secret_access_key=config['DEFAULT']['aws_secret_access_key']
)

bucketName = 'nw-alexburzinski'
bucketPath = 'data/historical/'

s3 = session.resource('s3')
bucket = s3.Bucket(bucketName)
logger.debug('Writing to the s3 bucket ' + bucketName)

files = [f for f in os.listdir(readFromDir)
    if os.path.isfile(os.path.join(readFromDir, f))]

logger.debug('Writing the following files to s3: ' + files)

for f in files:
    with open(os.path.join(readFromDir, f), 'rb') as data:
        bucket.put_object(Key=bucketPath + f, Body=data)
    data.close()
    logger.debug('Wrote {} to s3 successfully'.format(f))