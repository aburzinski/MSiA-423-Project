import sys
sys.path.append(r'C:\Users\aburz\OneDrive\Documents\Northwestern\Classes\MSiA 423\Project\MSiA-423-Project')

def test_createDatabaseURI():
    """Test the createDatabaseURI method"""
    import src.helpers.configHelpers as base
    # Test for incorrect dbtype
    dbtype = 'postgresql'
    dbname = 'test'
    host = '127.0.0.1'
    port = '5432'
    username = 'user'
    password = 'pw'

    try:
        base.createDatabaseURI(dbtype, host, dbname)
        assert False
    except ValueError:
        assert True

    # Test sqlite connection string
    dbtype = 'sqlite'
    dbname = 'test'
    host = '127.0.0.1'
    port = '5432'
    username = 'user'
    password = 'pw'

    expectedOutput = 'sqlite:///127.0.0.1/test.db'
    assert(base.createDatabaseURI(dbtype, host, dbname) == expectedOutput)

    # Test mysql connection string
    dbtype = 'mysql'
    dbname = 'test'
    host = '127.0.0.1'
    port = '5432'
    username = 'user'
    password = 'pw'

    expectedOutput = 'mysql+pymysql://user:pw@host:port/dbname'
    assert(base.createDatabaseURI(dbtype, host, dbname,
        port=port, username=username, password=password))
    
