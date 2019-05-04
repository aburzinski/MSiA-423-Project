DEBUG = True
LOGGING_CONFIG = "logging/local.conf"
PORT = 8000
APP_NAME = "penny-lane"
SQLALCHEMY_DATABASE_URI = 'sqlite:///../data/tracks.db'
HOST = "127.0.0.1"
SQLALCHEMY_ECHO = False  # If true, SQL for queries made will be printed
MAX_ROWS_SHOW = 100