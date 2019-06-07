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

    # Column numbers are indexed from one
    projectedStatsSchema = {
        'playerId': 1,
        'hits': 10,
        'homeRuns': 11,
        'runsBattedIn': 12,
        'atBats': 15,
        'walks': 13,
        'strikeoutsBatting': 14,
        'saves': 7,
        'strikeoutsPitching': 5,
        'inningsPitched': 9,
        'wins': 8,
        'walksAllowed': 4,
        'hitsAllowed': 3,
        'earnedRuns': 6,
        'mvpLikelihood': 16,
        'mvpRank': 17,
        'cyYoungLikelihood': 18,
        'cyYoungRank': 19
    }

    statsCount = 0

    for line in s3File.splitlines(False)[1:]:
        line = line.split(',')

        # Need to subtract one to index from zero
        playerId = int(line[projectedStatsSchema['playerId'] - 1])
        hits = int(float(line[projectedStatsSchema['hits'] - 1]))
        homeRuns = int(float(line[projectedStatsSchema['homeRuns'] - 1]))
        runsBattedIn = int(float(line[projectedStatsSchema['runsBattedIn'] - 1]))
        atBats = int(float(line[projectedStatsSchema['atBats'] - 1]))
        walks = int(float(line[projectedStatsSchema['walks'] - 1]))
        strikeoutsBatting = int(float(line[projectedStatsSchema['strikeoutsBatting'] - 1]))
        saves = int(float(line[projectedStatsSchema['saves'] - 1]))
        strikeoutsPitching = int(float(line[projectedStatsSchema['strikeoutsPitching'] - 1]))
        inningsPitched = int(float(line[projectedStatsSchema['inningsPitched'] - 1]))
        wins = int(float(line[projectedStatsSchema['wins'] - 1]))
        walksAllowed = int(float(line[projectedStatsSchema['walksAllowed'] - 1]))
        hitsAllowed = int(float(line[projectedStatsSchema['hitsAllowed'] - 1]))
        earnedRuns = int(float(line[projectedStatsSchema['earnedRuns'] - 1]))
        mvpLikelihood = float(line[projectedStatsSchema['mvpLikelihood'] - 1])
        mvpRank = int(float(line[projectedStatsSchema['mvpRank'] - 1]))
        cyYoungLikelihood = float(line[projectedStatsSchema['cyYoungLikelihood'] - 1])
        cyYoungRank = int(float(line[projectedStatsSchema['cyYoungRank'] - 1]))
        
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
