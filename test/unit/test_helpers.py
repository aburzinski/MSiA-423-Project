import sys
sys.path.append(r'C:\Users\aburz\OneDrive\Documents\Northwestern\Classes\MSiA 423\Project\MSiA-423-Project')

import os
import src.helpers.helpers as base

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

