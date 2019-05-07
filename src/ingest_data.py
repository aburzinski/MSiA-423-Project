import sys
sys.path.append(r'C:\Users\aburz\OneDrive\Documents\Northwestern\Classes\MSiA 423\Project\MSiA-423-Project')

import os
import logging.config
from config import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import src.helpers.helpers as h

parentDir = config.PROJECT_ROOT_DIR
logging.config.fileConfig(config.LOGGING_CONFIG_FILE)
logger = logging.getLogger(__name__)

from models.mlb_database.create_database import Base, Player, Team

# Don't need to check for dir, that is done on database creation
# if config.SQLALCHEMY_TYPE == 'sqlite':
#     h.silentCreateDir(config.SQLALCHEMY_SQLITE_DIR)

engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

new_player = Player(id=123, playerName='new player')
session.add(new_player)
session.commit()

logging.info('Added player to database successfully')
