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
        'hits': 15,
        'homeRuns': 16,
        'runsBattedIn': 17,
        'onBasePct': 21,
        'slugPct': 20,
        'atBats': 22,
        'earnedRunAverage': 13,
        'whip': 14,
        'saves': 8,
        'strikeouts': 6,
        'inningsPitched': 12,
        'wins': 10,
        'mvpLikelihood': 23,
        'mvpRank': 24,
        'cyYoungLikelihood': 25,
        'cyYoungRank': 26
    }

    statsCount = 0

    for line in s3File.splitlines(False)[1:]:
        line = line.split(',')

        # Need to subtract one to index from zero
        playerId = int(line[projectedStatsSchema['playerId'] - 1])
        hits = int(float(line[projectedStatsSchema['hits'] - 1]))
        homeRuns = int(float(line[projectedStatsSchema['homeRuns'] - 1]))
        runsBattedIn = int(float(line[projectedStatsSchema['runsBattedIn'] - 1]))
        onBasePlusSlug = float(line[projectedStatsSchema['onBasePct'] - 1]) + float(line[projectedStatsSchema['slugPct'] - 1])
        atBats = int(float(line[projectedStatsSchema['atBats'] - 1]))
        earnedRunAverage = float(line[projectedStatsSchema['earnedRunAverage'] - 1])
        whip = float(line[projectedStatsSchema['whip'] - 1])
        saves = int(float(line[projectedStatsSchema['saves'] - 1]))
        strikeouts = int(float(line[projectedStatsSchema['strikeouts'] - 1]))
        inningsPitched = int(float(line[projectedStatsSchema['inningsPitched'] - 1]))
        wins = int(float(line[projectedStatsSchema['wins'] - 1]))
        mvpLikelihood = float(line[projectedStatsSchema['mvpLikelihood'] - 1])
        mvpRank = int(float(line[projectedStatsSchema['mvpRank'] - 1]))
        cyYoungLikelihood = float(line[projectedStatsSchema['cyYoungLikelihood'] - 1])
        cyYoungRank = int(float(line[projectedStatsSchema['cyYoungRank'] - 1]))
        
        new_statistic = ProjectedStats(playerId=playerId,
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
            wins=wins,
            mvpLikelihood=mvpLikelihood,
            mvpRank=mvpRank,
            cyYoungLikelihood=cyYoungLikelihood,
            cyYoungRank=cyYoungRank
        )
        session.add(new_statistic)
        statsCount += 1

    session.commit()
    logging.info('Added {} projected statistics to database successfully'.format(str(statsCount)))
