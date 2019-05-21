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

# Specify columns to later check for missing values
pitching = pd.read_csv(os.path.join(config.PROJECT_ROOT_DIR, 'data', args.featureType, 'pitching{}.csv'.format(args.featureType)),
    encoding = 'latin', dtype = {'ppa': str, 'obp': str, 'era': str, 'whip': str})
hitting = pd.read_csv(os.path.join(config.PROJECT_ROOT_DIR, 'data', args.featureType, 'hitting{}.csv'.format(args.featureType)),
    encoding = 'latin', dtype = {'slg': str, 'obp': str})
players = pd.read_csv(os.path.join(config.PROJECT_ROOT_DIR, 'data', 'historical', 'players.csv'), encoding = 'latin')
mvp = pd.read_csv(os.path.join(config.PROJECT_ROOT_DIR, 'data', 'auxiliary', 'mvpWinners.csv'), encoding = 'latin')

merged = players.merge(mvp, how='left', left_on='name_display_first_last', right_on='Winner')
if args.featureType == 'projected':
    merged['season'] = config.CURRENT_SEASON
    pitching['season'] = config.CURRENT_SEASON
    hitting['season'] = config.CURRENT_SEASON

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
merged = stats.merge(merged, how = 'left', left_on=['player_id','season'], right_on=['player_id', 'Year'])

minimumInningsPitched = 10
minimumAtBats = 10
merged = merged[(merged['ip'] > minimumInningsPitched) | (merged['ab_y'] > minimumAtBats)]

merged['sv_pct'] = merged['sv']/merged['svo']
merged['win_pct'] = merged['w']/(merged['w'] + merged['l'])
merged['hits_9'] = mh.nineInningNormalize(merged, 'h_x')
merged['hrs_9'] = mh.nineInningNormalize(merged, 'hr_x')
merged['bbs_9'] = mh.nineInningNormalize(merged, 'bb_x')
merged['ks_9'] = mh.nineInningNormalize(merged, 'so_x')
merged['ers_9'] = mh.nineInningNormalize(merged, 'er')

merged['hit_ab'] = mh.atBatNormalize(merged, 'h_y', 'ab_y')
merged['hr_ab'] = mh.atBatNormalize(merged, 'hr_y', 'ab_y')
merged['rbi_ab'] = mh.atBatNormalize(merged, 'rbi', 'ab_y')
merged['bb_ab'] = mh.atBatNormalize(merged, 'bb_y', 'ab_y')
merged['k_ab'] = mh.atBatNormalize(merged, 'so_y', 'ab_y')

if args.featureType == 'historical':
    merged['is_winner'] = merged['Winner'].apply(lambda x: 0 if isinstance(x, float) else 1)
    modelData = merged[['hits_9', 'hrs_9', 'bbs_9', 'ks_9', 'ers_9', 'sv_pct', 'win_pct', 'era', 'whip', 'hit_ab', 'hr_ab', 'rbi_ab', 'bb_ab', 'k_ab', 'slg_y', 'obp_y', 'is_winner']]
elif args.featureType == 'projected':
    modelData = merged[['player_id', 'hits_9', 'hrs_9', 'bbs_9', 'ks_9', 'ers_9', 'sv_pct', 'win_pct', 'era', 'whip', 'hit_ab', 'hr_ab', 'rbi_ab', 'bb_ab', 'k_ab', 'slg_y', 'obp_y']]

modelData.is_copy = False

modelData.loc[modelData['era'] == '-.--', 'era'] = 0.0
modelData.loc[modelData['era'] == '*.**', 'era'] = 0.0
modelData.loc[modelData['whip'] == '-.--', 'whip'] = 0.0
modelData.loc[modelData['whip'] == '*.**', 'whip'] = 0.0

modelData.loc[modelData['slg_y'] == '.---', 'slg_y'] = 0.0
modelData.loc[modelData['obp_y'] == '.---', 'obp_y'] = 0.0

modelData = modelData.replace([np.inf, -np.inf], np.nan).fillna(0)

writeToDir = os.path.join(config.PROJECT_ROOT_DIR, 'data', 'features')
h.silentCreateDir(writeToDir)
modelData.to_csv(os.path.join(writeToDir, 'mvpFeatures{}.csv'.format(args.featureType)), index=False)

logger.info('A file with {} rows and {} columns was created'.format(modelData.shape[0], modelData.shape[1]))
