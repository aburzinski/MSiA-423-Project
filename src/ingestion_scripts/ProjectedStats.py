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

from models.mlb_database.create_database import Base, ProjectedStats

def ingestProjectedStats(s3File, session, truncate=True):
    
    if truncate:
        session.query(ProjectedStats).delete()

    columns = s3File.splitlines(False)[0]
    columns = columns[1:][:-1].split('","')

    # Column numbers are indexed from one
    projectedStatsSchema = {
        'playerId': columns.index('player_id'),
        'hits': columns.index('h_y'),
        'homeRuns': columns.index('hr_y'),
        'runsBattedIn': columns.index('rbi'),
        'atBats': columns.index('ab_y'),
        'walks': columns.index('bb_y'),
        'strikeoutsBatting': columns.index('so_y'),
        'saves': columns.index('sv'),
        'strikeoutsPitching': columns.index('so_x'),
        'inningsPitched': columns.index('ip'),
        'wins': columns.index('w'),
        'walksAllowed': columns.index('bb_x'),
        'hitsAllowed': columns.index('h_x'),
        'earnedRuns': columns.index('er'),
        'mvpLikelihood': columns.index('mvpLikelihood'),
        'mvpRank': columns.index('mvpRank'),
        'cyYoungLikelihood': columns.index('cyYoungLikelihood'),
        'cyYoungRank': columns.index('cyYoungRank')
    }

    statsCount = 0

    for line in s3File.splitlines(False)[1:]:
        line = line.split(',')

        # Need to subtract one to index from zero
        playerId = int(line[projectedStatsSchema['playerId']])
        hits = int(float(line[projectedStatsSchema['hits']]))
        homeRuns = int(float(line[projectedStatsSchema['homeRuns']]))
        runsBattedIn = int(float(line[projectedStatsSchema['runsBattedIn']]))
        atBats = int(float(line[projectedStatsSchema['atBats']]))
        walks = int(float(line[projectedStatsSchema['walks']]))
        strikeoutsBatting = int(float(line[projectedStatsSchema['strikeoutsBatting']]))
        saves = int(float(line[projectedStatsSchema['saves']]))
        strikeoutsPitching = int(float(line[projectedStatsSchema['strikeoutsPitching']]))
        inningsPitched = int(float(line[projectedStatsSchema['inningsPitched']]))
        wins = int(float(line[projectedStatsSchema['wins']]))
        walksAllowed = int(float(line[projectedStatsSchema['walksAllowed']]))
        hitsAllowed = int(float(line[projectedStatsSchema['hitsAllowed']]))
        earnedRuns = int(float(line[projectedStatsSchema['earnedRuns']]))
        mvpLikelihood = float(line[projectedStatsSchema['mvpLikelihood']])
        mvpRank = int(float(line[projectedStatsSchema['mvpRank']]))
        cyYoungLikelihood = float(line[projectedStatsSchema['cyYoungLikelihood']])
        cyYoungRank = int(float(line[projectedStatsSchema['cyYoungRank']]))
        
        new_statistic = ProjectedStats(playerId=playerId,
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
            earnedRuns=earnedRuns,
            mvpLikelihood=mvpLikelihood,
            mvpRank=mvpRank,
            cyYoungLikelihood=cyYoungLikelihood,
            cyYoungRank=cyYoungRank
        )
        session.add(new_statistic)
        statsCount += 1

    session.commit()
    logging.info('Added {} projected statistics to database successfully'.format(str(statsCount)))
