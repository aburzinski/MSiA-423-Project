import os
import sys
sys.path.append(os.environ.get('PYTHONPATH'))

import logging.config
from config import config
import pandas as pd

logging.config.fileConfig(config.LOGGING_CONFIG_FILE, disable_existing_loggers=False)
logger = logging.getLogger(__name__)

if __name__ == '__main__':

    mvpStats = pd.read_csv(os.path.join(config.PROJECT_ROOT_DIR, 'data', 'projected', 'mvpPredictions.csv'))
    mvpStats.rename(columns={
        'prediction': 'mvpLikelihood',
        'rank': 'mvpRank'
    }, inplace=True)

    cyYoungStats = pd.read_csv(os.path.join(config.PROJECT_ROOT_DIR, 'data', 'projected', 'cyYoungPredictions.csv'))
    cyYoungStats.rename(columns={
        'prediciton': 'cyYoungLikelihood',
        'rank': 'cyYoungRank'
    }, inplace=True)

    merged = mvpStats.merge(cyYoungStats, how='left', on='player_id')
    logger.debug('Merging files of size {} and size {} to a file of size {} by {}'.format(mvpStats.shape[0],
        cyYoungStats.shape[0], merged.shape[0], merged.shape[1]))

    merged.to_csv(os.path.join(config.PROJECT_ROOT_DIR, 'data', 'projected', 'currentStats.csv'), index=False)

    logger.info('Files merged successfully')