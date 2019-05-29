import os
import sys
sys.path.append(os.environ.get('PYTHONPATH'))

import logging.config
from config import config
import pandas as pd
import pickle
import src.helpers.helpers as h
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import imblearn.over_sampling as SMOTE

logging.config.fileConfig(config.LOGGING_CONFIG_FILE, disable_existing_loggers=False)
logger = logging.getLogger(__name__)

def trainModel(modelData):
    """Train and fit the model based on the input data, then return it"""
    X = modelData.loc[:, modelData.columns != 'is_winner']
    y = modelData.loc[:, modelData.columns == 'is_winner']

    over_sample = SMOTE.SMOTE(random_state = 0)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
    columns = X_train.columns

    over_sample_X, over_sample_y = over_sample.fit_sample(X_train, y_train.values.ravel())
    over_sample_X = pd.DataFrame(data=over_sample_X,columns=columns )
    over_sample_y = pd.DataFrame(data=over_sample_y,columns=['is_winner'])

    model = LogisticRegression(random_state=0, solver='lbfgs', multi_class='ovr')
    model.fit(over_sample_X, over_sample_y.values.ravel())

    logger.debug('Model created and trained with {} rows of data'.format(over_sample_X.shape[0]))

    return model

if __name__ == '__main__':
    
    modelData = pd.read_csv(os.path.join(config.PROJECT_ROOT_DIR, 'data', 'features', 'mvpFeaturesHistorical.csv'))
    model = trainModel(modelData)
    
    writeToDir = os.path.join(config.PROJECT_ROOT_DIR, 'data', 'model_files')
    h.silentCreateDir(writeToDir)

    with open(os.path.join(writeToDir, 'mvp.model'), 'wb') as f:
        pickle.dump(model, f)
    f.close()

    logger.info('Model saved to {}'.format(os.path.join(writeToDir, 'mvp.model')))