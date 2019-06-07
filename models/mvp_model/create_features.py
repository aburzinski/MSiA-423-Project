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

parser = argparse.ArgumentParser(description='The set of features to create.')
parser.add_argument('featureType', metavar='featureType', type=str,
    help='historical or projected')
args = parser.parse_args()

if args.featureType not in ['historical', 'projected']:
    raise ValueError('The directory argument must be either "historical" or "projected"')

def readFeatures():
    """Read the raw data from local fs or S3, and format it correctly for creating features"""
    # Specify columns to later check for missing values
    pitching = pd.read_csv(os.path.join(config.PROJECT_ROOT_DIR, 'data', args.featureType, 'pitching{}.csv'.format(args.featureType.capitalize())),
        encoding = 'latin', dtype = {'ppa': str, 'obp': str, 'era': str, 'whip': str})
    hitting = pd.read_csv(os.path.join(config.PROJECT_ROOT_DIR, 'data', args.featureType, 'hitting{}.csv'.format(args.featureType.capitalize())),
        encoding = 'latin', dtype = {'slg': str, 'obp': str})
    players = pd.read_csv(os.path.join(config.PROJECT_ROOT_DIR, 'data', 'historical', 'players.csv'), encoding = 'latin')
    mvp = pd.read_csv(os.path.join(config.PROJECT_ROOT_DIR, 'data', 'auxiliary', 'mvpWinners.csv'), encoding = 'latin')
    teams = pd.read_csv(os.path.join(config.PROJECT_ROOT_DIR, 'data', 'historical', 'teams.csv'), encoding = 'latin')

    merged = players.merge(mvp, how='left', left_on='name_display_first_last', right_on='Winner')
    if args.featureType == 'projected':
        merged['season'] = config.CURRENT_SEASON
        pitching['season'] = config.CURRENT_SEASON
        hitting['season'] = config.CURRENT_SEASON

    merged['season'] = config.CURRENT_SEASON
    merged = merged.merge(teams, how = 'left', left_on=['team_id', 'season'], right_on=['team_id', 'season'])

    league = merged[['player_id', 'season', 'league']]

    # Need to rename the columns because the historical data will be rename
    # during the join, by projected data will not
    pitching.rename(columns={
        'h': 'h_x',
        'hr': 'hr_x',
        'bb': 'bb_x',
        'so': 'so_x'
    }, inplace=True)

    hitting.rename(columns={
        'h': 'h_y',
        'hr': 'hr_y',
        'bb': 'bb_y',
        'so': 'so_y',
        'ab': 'ab_y',
        'obp': 'obp_y',
        'slg': 'slg_y'
    }, inplace=True)

    stats = pitching.merge(hitting, how='outer', left_on=['player_id', 'season'], right_on=['player_id', 'season'])
    merged = stats.merge(merged, how='left', left_on=['player_id','season'], right_on=['player_id', 'Year'])
    merged = merged.merge(league, how='left', left_on=['player_id', 'season_x'], right_on=['player_id', 'season'])

    return merged

def cleanFeatures(merged):
    """Clean and normalize the feature data"""
    minimumInningsPitched = 10
    minimumAtBats = 10
    merged = merged[(merged['ip'] > minimumInningsPitched) | (merged['ab_y'] > minimumAtBats)]

    if args.featureType == 'historical':
        merged['is_winner'] = merged['Winner'].apply(lambda x: 0 if isinstance(x, float) else 1)
        modelData = merged[['h_x', 'bb_x', 'so_x', 'er', 'sv', 'w', 'ip', 'h_y', 'hr_y',
            'rbi', 'bb_y', 'so_y', 'ab_y', 'is_winner']]
    elif args.featureType == 'projected':
        modelData = merged[['player_id', 'league_y', 'h_x', 'bb_x', 'so_x', 'er', 'sv', 'w', 'ip', 'h_y', 'hr_y',
            'rbi', 'bb_y', 'so_y', 'ab_y']]
        modelData.rename(columns={
            'league_y': 'league'
        }, inplace=True)

    modelData.is_copy = False
    modelData = modelData.replace([np.inf, -np.inf], np.nan).fillna(0)

    return modelData.drop_duplicates()

if __name__ == '__main__':

    merged = readFeatures()
    modelData = cleanFeatures(merged)

    writeToDir = os.path.join(config.PROJECT_ROOT_DIR, 'data', 'features')
    h.silentCreateDir(writeToDir)
    modelData.to_csv(os.path.join(writeToDir, 'mvpFeatures{}.csv'.format(args.featureType.capitalize())), index=False)

    logger.info('A file with {} rows and {} columns was created'.format(modelData.shape[0], modelData.shape[1]))
