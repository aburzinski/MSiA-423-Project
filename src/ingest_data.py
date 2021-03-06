import os
import sys
sys.path.append(os.environ.get('PYTHONPATH'))

import logging.config
from config import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import boto3
import src.helpers.helpers as h
import src.helpers.azureHelpers as ah
from datetime import datetime

parentDir = config.PROJECT_ROOT_DIR
logging.config.fileConfig(config.LOGGING_CONFIG_FILE, disable_existing_loggers=False)
logger = logging.getLogger(__name__)

from models.mlb_database.create_database import Base
import src.ingestion_scripts.Player as player
import src.ingestion_scripts.Team as team
import src.ingestion_scripts.CurrentStats as currentStats
import src.ingestion_scripts.ProjectedStats as projectedStats
import src.ingestion_scripts.LastUpdateDate as lastUpdateDate

if __name__ == '__main__':
    engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
    Base.metadata.bind = engine

    DBSession = sessionmaker(bind=engine)
    dbsession = DBSession()

    s3session  = boto3.Session(
        aws_access_key_id=config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY
    )

    bucketName = config.AWS_S3_BUCKET_NAME
    bucketPath = 'data/{}/'.format('historical')

    s3 = s3session.client('s3')
    logger.debug('Connected to s3 successfully')

    # Ingest teams
    logger.info('Reading from the s3 bucket ' + bucketName)
    teamFile = ah.readFileFromS3('teams.csv', s3, bucketName, bucketPath)

    team.ingestTeams(teamFile, dbsession, truncate=True)

    # Ingest players
    logger.info('Reading from the s3 bucket ' + bucketName)
    playerFile = ah.readFileFromS3('players.csv', s3, bucketName, bucketPath)

    player.ingestPlayers(playerFile, dbsession, truncate=True)

    # Ingest projected statistics
    logger.info('Reading from the s3 bucket ' + bucketName)
    bucketPath = 'data/{}/'.format('projected')
    projectedStatsFile = ah.readFileFromS3('projectedStats.csv', s3, bucketName, bucketPath)

    projectedStats.ingestProjectedStats(projectedStatsFile, dbsession, truncate=True)

    # Ingest current statistics
    logger.info('Reading from the s3 bucket ' + bucketName)
    bucketPath = 'data/{}/'.format('projected')
    currentStatsFile = ah.readFileFromS3('currentStats.csv', s3, bucketName, bucketPath)

    currentStats.ingestCurrentStats(currentStatsFile, dbsession, truncate=True)


    # Update last updated table
    lastUpdateDate.ingestLastUpdate(dbsession, truncate=True)

    logger.info('Data ingestion conpleted')