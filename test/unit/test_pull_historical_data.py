import sys
sys.path.append(r'C:\Users\aburz\OneDrive\Documents\Northwestern\Classes\MSiA 423\Project\MSiA-423-Project')

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


def test_writeIterLine():
    """Test the writeIterLine function for different input cases"""
    
    filename = './myTestFile'
    # Test empty string
    expectedValue = '""\n'
    testValue = ''

    with open(filename, 'w') as f:
        base.writeIterLine({}.values(), f)
    f.close()

    with open(filename, 'r') as f:
        testValue = f.read()
    f.close()

    # Test one input
    expectedValue = '"testValue"\n'
    testValue = ''

    with open(filename, 'w') as f:
        base.writeIterLine({'testKey': 'testValue'}.values(), f)
    f.close()

    with open(filename, 'r') as f:
        testValue = f.read()
    f.close()

    assert(testValue == expectedValue)

    # Test two inputs
    expectedValue = '"testValue","test2Value"\n'
    testValue = ''

    with open(filename, 'w') as f:
        base.writeIterLine({'testKey': 'testValue', 'test2Key': 'test2Value'}.values(), f)
    f.close()

    with open(filename, 'r') as f:
        testValue = f.read()
    f.close()

    assert(testValue == expectedValue)

    # Test comma in iterator
    expectedValue = '"testValue","test2,test3"\n'
    testValue = ''

    with open(filename, 'w') as f:
        base.writeIterLine({'testKey': 'testValue', 'test2Key': 'test2,test3'}.values(), f)
    f.close()

    with open(filename, 'r') as f:
        testValue = f.read()
    f.close()

    assert(testValue == expectedValue)

    # Test incorrect type
    with open(filename, 'w') as f:
        try:
            base.writeIterLine({'testKey': 123}.values(), f)
        except TypeError:
            assert(True)
    f.close()

    # Clean up test file
    os.remove(filename)