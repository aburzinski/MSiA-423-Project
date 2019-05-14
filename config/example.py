import os.path as path

# DEBUG = True
# LOGGING_CONFIG = "logging/local.conf"
# PORT = 8000
# APP_NAME = "penny-lane"
# HOST = "127.0.0.1"
# SQLALCHEMY_ECHO = False  # If true, SQL for queries made will be printed
# MAX_ROWS_SHOW = 100

# Project
PROJECT_ROOT_DIR = path.join('Example', 'Project', 'Root')
CURRENT_SEASON = 2019

# S3
AWS_S3_BUCKET_NAME = 'bocket-name'
AWS_ACCESS_KEY_ID = 'id'
AWS_SECRET_ACCESS_KEY = 'secret-key'

# Logging
LOGGING_CONFIG_FILE = path.join(PROJECT_ROOT_DIR, 'config', 'logging', 'local.conf')

# SQL Alchemy
SQLALCHEMY_SQLITE_HOST = path.join(PROJECT_ROOT_DIR, 'data', 'database')

SQLALCHEMY_MYSQL_HOST = 'host'
SQLALCHEMY_MYSQL_PORT = 'port'
SQLALCHEMY_MYSQL_USERNAME = 'username'
SQLALCHEMY_MYSQL_PASSWORD = 'password'

SQLALCHEMY_HOST = SQLALCHEMY_SQLITE_HOST
SQLALCHEMY_TYPE = 'sqlite'  # Should be either 'sqlite' or 'mysql'
SQLALCHEMY_DATABASE_NAME = 'database'

import src.helpers.configHelpers as ch
SQLALCHEMY_DATABASE_URI = ch.createDatabaseURI(dbtype=SQLALCHEMY_TYPE,
    host=SQLALCHEMY_HOST, dbname=SQLALCHEMY_DATABASE_NAME,
    port=SQLALCHEMY_MYSQL_PORT, username=SQLALCHEMY_MYSQL_USERNAME,
    password=SQLALCHEMY_MYSQL_PASSWORD)