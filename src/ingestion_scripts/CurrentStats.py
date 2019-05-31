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
        'playerId': 37,
        'hits': 34,
        'homeRuns': 25,
        'runsBattedIn': 41,
        'onBasePct': 45,
        'slugPct': 43,
        'atBats': 2,
        'earnedRunAverage': 107,
        'whip': 63,
        'saves': 104,
        'strikeouts': 106,
        'inningsPitched': 51,
        'wins': 79
    }

    statsCount = 0

    for line in s3File.splitlines(False)[1:]:
        line = line.split(',')

        # Need to subtract one to index from zero
        playerId = int(line[currentStatsSchema['playerId'] - 1])
        hits = int(float(line[currentStatsSchema['hits'] - 1]))
        homeRuns = int(float(line[currentStatsSchema['homeRuns'] - 1]))
        runsBattedIn = int(float(line[currentStatsSchema['runsBattedIn'] - 1]))
        onBasePlusSlug = float(line[currentStatsSchema['onBasePct'] - 1]) + float(line[currentStatsSchema['slugPct'] - 1])
        atBats = int(float(line[currentStatsSchema['atBats'] - 1]))
        earnedRunAverage = float(line[currentStatsSchema['earnedRunAverage'] - 1])
        whip = float(line[currentStatsSchema['whip'] - 1])
        saves = int(float(line[currentStatsSchema['saves'] - 1]))
        strikeouts = int(float(line[currentStatsSchema['strikeouts'] - 1]))
        inningsPitched = int(float(line[currentStatsSchema['inningsPitched'] - 1]))
        wins = int(float(line[currentStatsSchema['wins'] - 1]))
        
        new_statistic = CurrentStats(playerId=playerId,
            hits=hits,
            homeRuns=homeRuns,
            runsBattedIn=runsBattedIn,
            onBasePlusSlug=onBasePlusSlug,
            atBats=atBats,
            earnedRunAverage=earnedRunAverage,
            whip=whip,
            saves=saves,
            strikeouts=strikeouts,
            inningsPitched=inningsPitched,
            wins=wins
        )
        session.add(new_statistic)
        statsCount += 1

    session.commit()
    logging.info('Added {} current statistics to database successfully'.format(str(statsCount)))
