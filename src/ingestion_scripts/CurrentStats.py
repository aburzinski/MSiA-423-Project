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

    columns = s3File.splitlines(False)[0]
    columns = columns.split(',')

    # Column numbers are indexed from one
    currentStatsSchema = {
        'playerId': columns.index('player_id'),
        'hits': columns.index('h_x'),
        'homeRuns': columns.index('hr_x'),
        'runsBattedIn': columns.index('rbi'),
        'atBats': columns.index('ab'),
        'walks': columns.index('bb_x'),
        'strikeoutsBatting': columns.index('so_x'),
        'saves': columns.index('sv'),
        'strikeoutsPitching': columns.index('so_y'),
        'inningsPitched': columns.index('ip'),
        'wins': columns.index('w'),
        'walksAllowed': columns.index('bb_y'),
        'hitsAllowed': columns.index('h_y'),
        'earnedRuns': columns.index('er')
    }

    statsCount = 0

    for line in s3File.splitlines(False)[1:]:
        line = line.split(',')

        # Need to subtract one to index from zero
        playerId = int(line[currentStatsSchema['playerId']])
        hits = int(float(line[currentStatsSchema['hits']]))
        homeRuns = int(float(line[currentStatsSchema['homeRuns']]))
        runsBattedIn = int(float(line[currentStatsSchema['runsBattedIn']]))
        atBats = int(float(line[currentStatsSchema['atBats']]))
        walks = int(float(line[currentStatsSchema['walks']]))
        strikeoutsBatting = int(float(line[currentStatsSchema['strikeoutsBatting']]))
        saves = int(float(line[currentStatsSchema['saves']]))
        strikeoutsPitching = int(float(line[currentStatsSchema['strikeoutsPitching']]))
        inningsPitched = int(float(line[currentStatsSchema['inningsPitched']]))
        wins = int(float(line[currentStatsSchema['wins']]))
        walksAllowed = int(float(line[currentStatsSchema['walksAllowed']]))
        hitsAllowed = int(float(line[currentStatsSchema['hitsAllowed']]))
        earnedRuns = int(float(line[currentStatsSchema['earnedRuns']]))
        
        new_statistic = CurrentStats(playerId=playerId,
            hits=hits,
            homeRuns=homeRuns,
            runsBattedIn=runsBattedIn,
            atBats=atBats,
            walks=walks,
            strikeoutsBatting=strikeoutsBatting,
            saves=saves,
            strikeoutsPitching=strikeoutsPitching,
            inningsPitched=inningsPitched,
            wins=wins,
            walksAllowed=walksAllowed,
            hitsAllowed=hitsAllowed,
            earnedRuns=earnedRuns
        )
        session.add(new_statistic)
        statsCount += 1

    session.commit()
    logging.info('Added {} current statistics to database successfully'.format(str(statsCount)))
