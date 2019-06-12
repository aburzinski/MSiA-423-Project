import sys
import os
sys.path.append(os.environ.get('PYTHONPATH'))

import os
import models.cy_young_model.create_features as cyYoungBase
import pytest
from config import config

def test_createCyYoungFeatures():
    """Test the createMvpFeatures function"""

    # Test for correct shape for projected stats
    expectedShape = (2,9)

    testPitching = os.path.join(config.PROJECT_ROOT_DIR, 'data', 'sample', 'pitchingProjected.csv')

    testShape = cyYoungBase.createCyYoungFeatures(testPitching, 'projected')

    assert(testShape.shape == expectedShape)

    # Test for correct shape for historical stats
    expectedShape = (2,8)

    testPitching = os.path.join(config.PROJECT_ROOT_DIR, 'data', 'sample', 'pitchingHistorical.csv')
    
    testShape = cyYoungBase.createCyYoungFeatures(testPitching, 'historical')

    assert(testShape.shape == expectedShape)

    # Test for incorrect file paths

    try:
        cyYoungBase.createCyYoungFeatures('badPath', 'historical')
        assert False
    except IOError:
        assert True

    # Test for incorrect arg being passed

    try:
        testPitching = os.path.join(config.PROJECT_ROOT_DIR, 'data', 'sample', 'pitchingHistorical.csv')

        cyYoungBase.createCyYoungFeatures(testPitching, 'badArg')
        assert False
    except ValueError:
        assert True
