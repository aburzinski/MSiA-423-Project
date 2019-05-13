import logging.config
from config import config

logging.config.fileConfig(config.LOGGING_CONFIG_FILE)
logger = logging.getLogger(__name__)

def createDatabaseURI(dbtype, host, dbname, dialect='pymysql',
    port='', username='', password=''):
    """Return a properly formatted database URI base on the inputs
        Args:
            dbtype(`str`): Should be either sqlite or mysql for this project
            dialect(`pymysql`): Not used for sqlite databases
            host(`str`): Database connection endpoint
            port(`str`): Not used for sqlite databases
            username(`str`): Not used for sqlite databases
            password(`str`): Not used for sqlite databases
            dbname(`str`): Name of the database to connect to
        Returns:
            A correctly formatted database connection string
    """
    if dbtype == 'mysql':
        return '{}+{}://{}:{}@{}:{}/{}'.format(dbtype, dialect,
            username, password, host, port, dbname)
    elif dbtype == 'sqlite':
        return '{}:///{}/{}.db'.format(dbtype, host, dbname)
    else:
        raise ValueError('This project only supports sqlite and mysql databases')