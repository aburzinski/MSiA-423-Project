import os
import sys
sys.path.append(os.environ.get('PYTHONPATH'))

import logging.config
from config import config
import pandas as pd
import numpy as np
import pickle

logging.config.fileConfig(config.LOGGING_CONFIG_FILE, disable_existing_loggers=False)
logger = logging.getLogger(__name__)

def makePredictions(modelData, models):
    """Make predictions based on the input data, and rank them

    Returns:
        A dataframe with the player_id, prediction, and rank
    """
    predictData = modelData
    predictData = predictData.loc[:, predictData.columns != 'player_id']
    predictData = predictData.loc[:, predictData.columns != 'league']

    probs = np.stack((models[0].predict_proba(predictData)[:,1], models[1].predict_proba(predictData)[:,1]))
    # avgProbs = np.mean(probs, axis=0)
    avgProbs = np.multiply(models[0].predict_proba(predictData)[:,1], models[1].predict_proba(predictData)[:,1]+.001)

    modelData['prediction'] = avgProbs

    modelData['rank'] = modelData.groupby('league')['prediction'].rank(method='dense', ascending=False).astype(int)
    # modelData = modelData[['player_id', 'prediction', 'rank']]

    return modelData.drop_duplicates()

if __name__ == '__main__':
    with open(os.path.join(config.PROJECT_ROOT_DIR, 'data', 'model_files', 'mvp_lr.model'), 'rb') as f:
        model_lr = pickle.load(f)
    f.close()

    with open(os.path.join(config.PROJECT_ROOT_DIR, 'data', 'model_files', 'mvp_rf.model'), 'rb') as f:
        model_rf = pickle.load(f)
    f.close()

    modelData = pd.read_csv(os.path.join(config.PROJECT_ROOT_DIR, 'data', 'features', 'mvpFeaturesProjected.csv'))

    modelData = makePredictions(modelData, (model_lr, model_rf))
    
    modelData.to_csv(os.path.join(config.PROJECT_ROOT_DIR, 'data', 'projected', 'mvpPredictions.csv'), index=False)
    logger.info('{} predictions made'.format(modelData.shape[0]))