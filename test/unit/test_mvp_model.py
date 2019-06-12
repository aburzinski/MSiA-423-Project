import sys
import os
sys.path.append(os.environ.get('PYTHONPATH'))

import os
import models.mvp_model.create_features as mvpBase
import pytest
from config import config

def test_createMvpFeatures():
    """Test the createMvpFeatures function"""

    # Test for correct shape for projected stats
    expectedShape = (4,15)

    testPitching = os.path.join(config.PROJECT_ROOT_DIR, 'data', 'sample', 'pitchingProjected.csv')
    testHitting = os.path.join(config.PROJECT_ROOT_DIR, 'data', 'sample', 'hittingProjected.csv')

    testShape = mvpBase.createMvpFeatures(testPitching, testHitting, 'projected')

    assert(testShape.shape == expectedShape)

    # Test for correct shape for historical stats
    expectedShape = (4,14)

    testPitching = os.path.join(config.PROJECT_ROOT_DIR, 'data', 'sample', 'pitchingHistorical.csv')
    testHitting = os.path.join(config.PROJECT_ROOT_DIR, 'data', 'sample', 'hittingHistorical.csv')

    testShape = mvpBase.createMvpFeatures(testPitching, testHitting, 'historical')

    assert(testShape.shape == expectedShape)

    # Test for incorrect file paths

    try:
        mvpBase.createMvpFeatures('badPath', 'anotherBadPath', 'historical')
        assert False
    except IOError:
        assert True

    # Test for incorrect arg being passed

    try:
        testPitching = os.path.join(config.PROJECT_ROOT_DIR, 'data', 'sample', 'pitchingHistorical.csv')
        testHitting = os.path.join(config.PROJECT_ROOT_DIR, 'data', 'sample', 'hittingHistorical.csv')

        mvpBase.createMvpFeatures(testPitching, testHitting, 'badArg')
        assert False
    except ValueError:
        assert True
