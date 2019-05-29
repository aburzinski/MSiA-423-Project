import os
import sys
sys.path.append(os.environ.get('PYTHONPATH'))

import logging.config
from config import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import src.helpers.helpers as h
import src.helpers.azureHelpers as ah

parentDir = config.PROJECT_ROOT_DIR
logging.config.fileConfig(config.LOGGING_CONFIG_FILE, disable_existing_loggers=False)
logger = logging.getLogger(__name__)

from models.mlb_database.create_database import Base, CurrentStats

def ingestCurrentStats(s3File, session, truncate=True):
    
    if truncate:
        session.query(CurrentStats).delete()

    # Column numbers are indexed from one
    currentStatsSchema = {
        'playerId': 1,
        'mvpLikelihood': 2,
        'mvpRank': 3
    }

    statsCount = 0

    for line in s3File.splitlines(False)[1:]:
        line = line[1:][:-1].split(',')

        # Need to subtract one to index from zero
        playerId = int(line[currentStatsSchema['playerId'] - 1])
        mvpLikelihood = float(line[currentStatsSchema['mvpLikelihood'] - 1])
        mvpRank = int(line[currentStatsSchema['mvpRank'] - 1])
        
        new_statistic = CurrentStats(playerId=playerId,
            mvpLikelihood=mvpLikelihood,
            mvpRank=mvpRank
        )
        session.add(new_statistic)
        statsCount += 1

    session.commit()
    logging.info('Added {} player statistics to database successfully'.format(str(statsCount)))
