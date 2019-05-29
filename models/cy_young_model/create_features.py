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
    players = pd.read_csv(os.path.join(config.PROJECT_ROOT_DIR, 'data', 'historical', 'players.csv'), encoding = 'latin')
    cyYoung = pd.read_csv(os.path.join(config.PROJECT_ROOT_DIR, 'data', 'auxiliary', 'cyYoungWinners.csv'), encoding = 'latin')

    merged = players.merge(cyYoung, how='left', left_on='name_display_first_last', right_on='Winner')
    if args.featureType == 'projected':
        merged['season'] = config.CURRENT_SEASON
        pitching['season'] = config.CURRENT_SEASON

    # Need to rename the columns because the historical data will be rename
    # during the join, by projected data will not

    merged = pitching.merge(merged, how = 'left', left_on=['player_id','season'], right_on=['player_id', 'Year'])

    return merged

def cleanFeatures(merged):
    """Clean and normalize the feature data"""
    minimumInningsPitched = 10
    merged = merged[merged['ip'] > minimumInningsPitched]

    # merged.loc[:, 'sv_pct'] = merged['sv']/merged['svo']
    # merged.loc[:, 'win_pct'] = merged['w']/(merged['w'] + merged['l'])
    # merged.loc[:, 'hits_9'] = mh.nineInningNormalize(merged, 'h')
    # merged.loc[:, 'hrs_9'] = mh.nineInningNormalize(merged, 'hr')
    # merged.loc[:, 'bbs_9'] = mh.nineInningNormalize(merged, 'bb')
    # merged.loc[:, 'ks_9'] = mh.nineInningNormalize(merged, 'so')
    # merged.loc[:, 'ers_9'] = mh.nineInningNormalize(merged, 'er')

    if args.featureType == 'historical':
        merged['is_winner'] = merged['Winner'].apply(lambda x: 0 if isinstance(x, float) else 1)
        modelData = merged[['h', 'hr', 'bb', 'so', 'er', 'sv', 'svo', 'w', 'l', 'era', 'whip', 'ip', 'is_winner']].fillna(0)
    elif args.featureType == 'projected':
        modelData = merged[['player_id', 'h', 'hr', 'bb', 'so', 'er', 'sv', 'svo', 'w', 'l', 'era', 'whip', 'ip']].fillna(0)

    return modelData

if __name__ == '__main__':

    merged = readFeatures()
    modelData = cleanFeatures(merged)

    writeToDir = os.path.join(config.PROJECT_ROOT_DIR, 'data', 'features')
    h.silentCreateDir(writeToDir)
    modelData.to_csv(os.path.join(writeToDir, 'cyYoungFeatures{}.csv'.format(args.featureType.capitalize())), index=False)

    logger.info('A file with {} rows and {} columns was created'.format(modelData.shape[0], modelData.shape[1]))
