import sys
sys.path.append(r'C:\Users\aburz\OneDrive\Documents\Northwestern\Classes\MSiA 423\Project\MSiA-423-Project')

import os
import logging.config
from config import config
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, MetaData
from sqlalchemy.orm import sessionmaker
import sqlalchemy as sql
import src.helpers.helpers as h

logging.config.fileConfig(config.LOGGING_CONFIG_FILE, disable_existing_loggers=False)
logger = logging.getLogger(__name__)

Base = declarative_base()

class Player(Base):
    """Create a table to hold player data"""
    __tablename__ = 'player'
    id = Column(Integer, primary_key=True)
    playerName = Column(String(100), unique=False, nullable=False)

    def __repr__(self):
        return '<Player %r>' % self.playerName

class Team(Base):
    """Create a table to hold team data"""
    __tablename__ = 'team'
    id = Column(Integer, primary_key=True)
    teamName = Column(String(100), unique=False, nullable=False)

    def __repr__(self):
        return '<Team %r>' % self.teamName

if __name__ == '__main__':

    if config.SQLALCHEMY_TYPE == 'sqlite':
        h.silentCreateDir(config.SQLALCHEMY_SQLITE_DIR)
    
    logger.debug('Creating database at {}'.format(config.SQLALCHEMY_SQLITE_DIR))

    engine_string = config.SQLALCHEMY_DATABASE_URI
    engine = sql.create_engine(engine_string)

    Base.metadata.create_all(engine)
    logger.info('MLB database created successfully')