import sys
import os
sys.path.append(os.environ.get('PYTHONPATH'))

import pandas as pd
import numpy as np
import argparse
import logging.config
from config import config
import src.helpers.helpers as h
import src.helpers.modelHelpers as mh

parentDir = config.PROJECT_ROOT_DIR
logging.config.fileConfig(config.LOGGING_CONFIG_FILE, disable_existing_loggers=False)
logger = logging.getLogger(__name__)

def readFeatures(pitchingPath, featureType):
    """Read the raw data from local fs or S3, and format it correctly for creating features"""
    # Specify columns to later check for missing values
    pitching = pd.read_csv(pitchingPath,
        encoding = 'latin', dtype = {'ppa': str, 'obp': str, 'era': str, 'whip': str})
    players = pd.read_csv(os.path.join(config.PROJECT_ROOT_DIR, 'data', 'historical', 'players.csv'), encoding = 'latin')
    cyYoung = pd.read_csv(os.path.join(config.PROJECT_ROOT_DIR, 'data', 'auxiliary', 'cyYoungWinners.csv'), encoding = 'latin')
    teams = pd.read_csv(os.path.join(config.PROJECT_ROOT_DIR, 'data', 'historical', 'teams.csv'), encoding = 'latin')

    merged = players.merge(cyYoung, how='left', left_on='name_display_first_last', right_on='Winner')
    if featureType == 'projected':
        merged['season'] = config.CURRENT_SEASON
        pitching['season'] = config.CURRENT_SEASON

    merged['season'] = config.CURRENT_SEASON
    merged = merged.merge(teams, how = 'left', left_on=['team_id', 'season'], right_on=['team_id', 'season'])

    league = merged[['player_id', 'season', 'league']]

    # Need to rename the columns because the historical data will be rename
    # during the join, by projected data will not

    merged = pitching.merge(merged, how = 'left', left_on=['player_id','season'], right_on=['player_id', 'Year'])
    merged = merged.merge(league, how='left', left_on=['player_id', 'season_x'], right_on=['player_id', 'season'])

    return merged

def cleanFeatures(merged, featureType):
    """Clean and normalize the feature data"""
    minimumInningsPitched = 10
    merged = merged[merged['ip'] > minimumInningsPitched]

    if featureType == 'historical':
        merged['is_winner'] = merged['Winner'].apply(lambda x: 0 if isinstance(x, float) else 1)
        modelData = merged[['h', 'bb', 'so', 'er', 'sv', 'w', 'ip', 'is_winner']].fillna(0)
    elif featureType == 'projected':
        modelData = merged[['player_id', 'league_y', 'h', 'bb', 'so', 'er', 'sv', 'w', 'ip']].fillna(0)
        modelData.rename(columns={
            'league_y': 'league'
        }, inplace=True)

    return modelData.drop_duplicates()

def createCyYoungFeatures(pitchingPath, featureType):
    """Run the two functions defined above to create features file"""
    if not os.path.exists(pitchingPath):
        raise IOError('The pitching file was not found')

    if featureType not in ['historical', 'projected']:
        raise ValueError('The directory argument must be either "historical" or "projected"')

    merged = readFeatures(pitchingPath, featureType)
    modelData = cleanFeatures(merged, featureType)

    return modelData

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='The set of features to create.')
    parser.add_argument('featureType', metavar='featureType', type=str,
        help='historical or projected')
    args = parser.parse_args()

    if args.featureType not in ['historical', 'projected']:
        raise ValueError('The directory argument must be either "historical" or "projected"')

    pitchingPath = os.path.join(config.PROJECT_ROOT_DIR, 'data', args.featureType, 'pitching{}.csv'.format(args.featureType.capitalize()))

    modelData = createCyYoungFeatures(pitchingPath, args.featureType)

    writeToDir = config.FEATURES_DIR
    h.silentCreateDir(writeToDir)
    modelData.to_csv(os.path.join(writeToDir, 'cyYoungFeatures{}.csv'.format(args.featureType.capitalize())), index=False)

    logger.info('A file with {} rows and {} columns was created'.format(modelData.shape[0], modelData.shape[1]))
