import sys
sys.path.append(r'C:\Users\aburz\OneDrive\Documents\Northwestern\Classes\MSiA 423\Project\MSiA-423-Project')

import os
import src.helpers.helpers as base
import pytest

def test_silentRemove():
    """Test the silentRemove function"""
    # Ensure no error is thrown on incorrect file
    base.silentRemove('incorrectTestFIle')

    # Ensure file is deleted
    with open('myTestFile.txt', 'w') as f:
        f.write('This is a test file')
    f.close()

    base.silentRemove('myTestFile.txt')
    exists = os.path.isfile('myTestFile.txt')
    assert(not exists)

def test_silentCreateDir():
    """Test the silentCreateDir function"""
    # Ensure directory is created
    base.silentCreateDir('./myTestDir')
    exists = os.path.exists('./myTestDir')
    assert(exists)

    # Ensure there is no issue if directory already exists
    # Test directory exists from above code
    base.silentCreateDir('./myTestDir')
    exists = os.path.exists('./myTestDir')
    assert(exists)

    # Clean up test directory
    os.rmdir('./myTestDir')


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
            assert False
        except TypeError:
            assert(True)
    f.close()

    # Clean up test file
    os.remove(filename)


def test_textParseDate():
    """Test the textParseDate method"""
    # Test for empty string
    testValue = ''
    expectedValue = ''
    assert(base.textParseDate(testValue) == expectedValue)

    # Test correct format
    testValue = '1999-01-03T00:00:00'
    expectedValue = '1999/01/03'
    assert(base.textParseDate(testValue) == expectedValue)

    # Test incorrect format
    testValue = '01-03-1999'
    try:
        base.textParseDate(testValue)
        assert False
    except ValueError:
        assert(True)