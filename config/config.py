import sys
import os
sys.path.append(os.environ.get('PYTHONPATH'))

# Flask config
DEBUG = True
PORT = 8000
APP_NAME = 'whosinfirst'
HOST = '127.0.0.1'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Project
PROJECT_ROOT_DIR = os.environ.get('PYTHONPATH')
CURRENT_SEASON = 2019

# Yaml File Locations
MVP_YML = os.path.join(PROJECT_ROOT_DIR, 'config', 'models', 'mvp.yml')
CY_YOUNG_YML = os.path.join(PROJECT_ROOT_DIR, 'config', 'models', 'cyYoung.yml')

# Model Artifact Locations
FEATURES_DIR = os.path.join(PROJECT_ROOT_DIR, 'data', 'features')
MODEL_DIR = os.path.join(PROJECT_ROOT_DIR, 'data', 'model_files')

# S3
AWS_S3_BUCKET_NAME = os.environ.get('AWS_BUCKET_NAME')
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

# S3 Historical Data Download
# Note: This should never be changed
HISTORICAL_S3_BUCKET_NAME = '423-mlb-historical'

# Logging
LOGGING_CONFIG_FILE = os.path.join(PROJECT_ROOT_DIR, 'config', 'logging', 'local.conf')

# SQL Alchemy
SQLALCHEMY_SQLITE_HOST = os.path.join(PROJECT_ROOT_DIR, 'data', 'mlb_database')

SQLALCHEMY_MYSQL_HOST = os.environ.get('MYSQL_HOST')
SQLALCHEMY_MYSQL_PORT = '3306'
SQLALCHEMY_MYSQL_USERNAME = os.environ.get('MYSQL_USER')
SQLALCHEMY_MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD')

SQLALCHEMY_TYPE = 'sqlite'  # Should be either 'sqlite' or 'mysql'
if SQLALCHEMY_TYPE == 'sqlite':
    SQLALCHEMY_HOST = SQLALCHEMY_SQLITE_HOST
elif SQLALCHEMY_TYPE == 'mysql':
    SQLALCHEMY_HOST = SQLALCHEMY_MYSQL_HOST
else:
    raise ValueError('SQLALCHEMY_TYPE not set ccorrectly in config/config.py')
SQLALCHEMY_DATABASE_NAME = 'mlb'

import src.helpers.configHelpers as ch
SQLALCHEMY_DATABASE_URI = ch.createDatabaseURI(dbtype=SQLALCHEMY_TYPE,
    host=SQLALCHEMY_HOST, dbname=SQLALCHEMY_DATABASE_NAME,
    port=SQLALCHEMY_MYSQL_PORT, username=SQLALCHEMY_MYSQL_USERNAME,
    password=SQLALCHEMY_MYSQL_PASSWORD)
