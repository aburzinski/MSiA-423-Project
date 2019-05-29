import os
import sys
sys.path.append(os.environ.get('PYTHONPATH'))

import logging.config
from config import config
import pandas as pd
import pickle

logging.config.fileConfig(config.LOGGING_CONFIG_FILE, disable_existing_loggers=False)
logger = logging.getLogger(__name__)

def makePredictions(modelData, model):
    """Make predictions based on the input data, and rank them

    Returns:
        A dataframe with the player_id, prediction, and rank
    """
    predictData = modelData
    predictData = predictData.loc[:, predictData.columns != 'player_id']

    modelData['prediction'] = model.predict_proba(predictData)[:,1]

    modelData['rank'] = modelData['prediction'].rank(method='dense', ascending=False).astype(int)
    modelData = modelData[['player_id', 'prediction', 'rank']]

    return modelData

if __name__ == '__main__':
    with open(os.path.join(config.PROJECT_ROOT_DIR, 'data', 'model_files', 'mvp.model'), 'rb') as f:
        model = pickle.load(f)
    f.close()

    modelData = pd.read_csv(os.path.join(config.PROJECT_ROOT_DIR, 'data', 'features', 'mvpFeaturesProjected.csv'))

    modelData = makePredictions(modelData, model)
    
    modelData.to_csv(os.path.join(config.PROJECT_ROOT_DIR, 'data', 'projected', 'mvpPredictions.csv'), index=False)
    logger.info('{} predictions made'.format(modelData.shape[0]))