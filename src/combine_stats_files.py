import os
import sys
sys.path.append(os.environ.get('PYTHONPATH'))

import argparse
import logging.config
from config import config
import pandas as pd
import numpy as np

parser = argparse.ArgumentParser(description='Which type of files to combine')
parser.add_argument('type', metavar='type', type=str,
    help='"current" or "projected"')
args = parser.parse_args()

if args.type not in ['projected', 'current']:
    raise ValueError('The type argument must be either "projected" or "current"')


logging.config.fileConfig(config.LOGGING_CONFIG_FILE, disable_existing_loggers=False)
logger = logging.getLogger(__name__)

if __name__ == '__main__':

    if args.type == 'projected':

        df1 = pd.read_csv(os.path.join(config.PROJECT_ROOT_DIR, 'data', 'projected', 'mvpPredictions.csv'))
        df1.rename(columns={
            'prediction': 'mvpLikelihood',
            'rank': 'mvpRank'
        }, inplace=True)

        df2 = pd.read_csv(os.path.join(config.PROJECT_ROOT_DIR, 'data', 'projected', 'cyYoungPredictions.csv'))
        df2.rename(columns={
            'prediction': 'cyYoungLikelihood',
            'rank': 'cyYoungRank'
        }, inplace=True)

    elif args.type == 'current':

        df1 = pd.read_csv(os.path.join(config.PROJECT_ROOT_DIR, 'data', 'projected', 'hittingCurrent.csv'))
        df2 = pd.read_csv(os.path.join(config.PROJECT_ROOT_DIR, 'data', 'projected', 'pitchingCurrent.csv'))

    else:
        raise Exception('The type argument must be either "projected" or "current"')

    merged = df1.merge(df2, how='outer', on='player_id').drop_duplicates()
    logger.debug('Merging files of size {} and size {} to a file of size {} by {}'.format(df1.shape[0],
        df2.shape[0], merged.shape[0], merged.shape[1]))

    if args.type == 'projected':

        merged['cyYoungLikelihood'] = merged['cyYoungLikelihood'].fillna(0.0)
        merged['cyYoungRank'] = merged['cyYoungRank'].fillna(99999)

    elif args.type == 'current':
        
        merged.loc[merged['era'] == '-.--', 'era'] = 0.0
        merged.loc[merged['era'] == '*.**', 'era'] = 0.0
        merged.loc[merged['whip'] == '-.--', 'whip'] = 0.0
        merged.loc[merged['whip'] == '*.**', 'whip'] = 0.0

        merged.loc[merged['slg_x'] == '.---', 'slg_x'] = 0.0
        merged.loc[merged['obp_x'] == '.---', 'obp_x'] = 0.0

        merged = merged.replace([np.inf, -np.inf], np.nan).fillna(0)

    else:
        raise Exception('The type argument must be either "projected" or "current"')

    merged.to_csv(os.path.join(config.PROJECT_ROOT_DIR, 'data', 'projected', '{}Stats.csv'.format(args.type)), index=False)

    logger.info('Files merged successfully')