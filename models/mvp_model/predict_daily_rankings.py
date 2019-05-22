import os
import sys
sys.path.append(os.environ.get('PYTHONPATH'))

import logging.config
from config import config
import pandas as pd
import pickle

logging.config.fileConfig(config.LOGGING_CONFIG_FILE, disable_existing_loggers=False)
logger = logging.getLogger(__name__)

pitching = pd.read_csv(os.path.join(config.PROJECT_ROOT_DIR, 'data', 'projected', 'pitchingProjected.csv'), encoding = 'latin')
hitting = pd.read_csv(os.path.join(config.PROJECT_ROOT_DIR, 'data', 'projected', 'hittingProjected.csv'), encoding = 'latin')
players = pd.read_csv(os.path.join(config.PROJECT_ROOT_DIR, 'data', 'historical', 'players.csv'), encoding = 'latin')

with open(os.path.join(config.PROJECT_ROOT_DIR, 'data', 'model_files', 'mvp.model'), 'rb') as f:
    lr = pickle.load(f)
f.close()

modelData = pd.read_csv(os.path.join(config.PROJECT_ROOT_DIR, 'data', 'features', 'mvpFeaturesProjected.csv'))

predictData = modelData
predictData = predictData.loc[:, predictData.columns != 'player_id']

modelData['prediction'] = lr.predict_proba(predictData)[:,1]
modelData['rank'] = modelData['prediction'].rank(method='dense', ascending=False)
modelData = modelData[['player_id', 'prediction', 'rank']]

modelData.to_csv(os.path.join(config.PROJECT_ROOT_DIR, 'data', 'projected', 'mvpPredictions.csv'), index=False)
logger.info('{} predictions made'.format(modelData.shape[0]))