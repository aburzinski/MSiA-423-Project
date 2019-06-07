import sys
import os
sys.path.append(os.environ.get('PYTHONPATH'))

import os
import src.pull_historical_data as base

def test_parseYearString():
    """Test the parseYearString function for different input cases"""
    # Test empty string
    testInput = ''
    expectedOutput = set()
    assert(base.parseYearString(testInput) == expectedOutput)

    # Test one year
    testInput = '2017'
    expectedOutput = {2017}
    assert(base.parseYearString(testInput) == expectedOutput)

    # Test comma spearation
    testInput = '2017, 2019'
    expectedOutput = {2017, 2019}
    assert(base.parseYearString(testInput) == expectedOutput)

    # Test hyphen spearation
    testInput = '2017-2019'
    expectedOutput = {2017, 2018, 2019}
    assert(base.parseYearString(testInput) == expectedOutput)

    # Test comma and hyphen spearation
    testInput = '2015, 2017-2019'
    expectedOutput = {2015, 2017, 2018, 2019}
    assert(base.parseYearString(testInput) == expectedOutput)

    # Test complex scenario
    testInput = '2009, 2011-2012, 2014, 2015, 2017-2019'
    expectedOutput = {2009, 2011, 2012, 2014, 2015, 2017, 2018, 2019}
    assert(base.parseYearString(testInput) == expectedOutput)
