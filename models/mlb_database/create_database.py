import sys
import os
sys.path.append(os.environ.get('PYTHONPATH'))

import logging.config
from config import config
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, MetaData
from sqlalchemy.orm import sessionmaker
import sqlalchemy as sql
import pymysql
from sqlalchemy_utils import create_database, database_exists
import src.helpers.helpers as h

logging.config.fileConfig(config.LOGGING_CONFIG_FILE, disable_existing_loggers=False)
logger = logging.getLogger(__name__)

Base = declarative_base()

class Player(Base):
    """Create a table to hold player data"""
    __tablename__ = 'player'
    id = Column(Integer, primary_key=True)
    playerName = Column(String(100), unique=False, nullable=False)
    birthCity = Column(String(100), unique=False, nullable=True)
    birthState = Column(String(10), unique=False, nullable=True)
    birthCountry = Column(String(100), unique=False, nullable=True)
    age = Column(Integer, unique=False, nullable=True)
    height = Column(String(10), unique=False, nullable=True)
    weight = Column(String(10), unique=False, nullable=True)
    debutDate = Column(String(20), unique=False, nullable=True)
    position = Column(String(20), unique=False, nullable=True)
    currentTeamId = Column(Integer, unique=False, nullable=True)

    def __repr__(self):
        return '<Player %r>' % self.playerName

class Team(Base):
    """Create a table to hold team data"""
    __tablename__ = 'team'
    id = Column(Integer, primary_key=True)
    teamName = Column(String(100), unique=False, nullable=False)
    venueName = Column(String(100), unique=False, nullable=True)
    city = Column(String(100), unique=False, nullable=True)
    state = Column(String(100), unique=False, nullable=True)
    league = Column(String(10), unique=False, nullable=True)
    division = Column(String(10), unique=False, nullable=True)
    yearFounded = Column(Integer, unique=False, nullable=True)

    def __repr__(self):
        return '<Team %r>' % self.teamName

class CurrentStats(Base):
    """Create a table to hold current stats and predictions"""
    __tablename__ = 'currentStats'
    playerId = Column(Integer, primary_key=True)
    teamId = Column(Integer, unique=False, nullable=False)
    isPitcher = Column(Integer, unique=False, nullable=False)
    homeRuns = Column(Integer, unique=False, nullable=True)
    runsBattedIn = Column(Integer, unique=False, nullable=True)
    onBasePlusSlug = Column(Float, unique=False, nullable=True)
    atBats = Column(Integer, unique=False, nullable=True)
    earnedRunAverage = Column(Float, unique=False, nullable=True)
    saves = Column(Integer, unique=False, nullable=True)
    strikeOuts = Column(Integer, unique=False, nullable=True)
    inningsPitched = Column(Float, unique=False, nullable=True)
    winPercentage = Column(Float, unique=False, nullable=True)
    mvpLikelihood = Column(Float, unique=False, nullable=True)
    mvpRank = Column(Integer, unique=False, nullable=True)
    cyYoungLikelihood = Column(Float, unique=False, nullable=True)
    cyYoungRank = Column(Integer, unique=False, nullable=True)

    def __repr__(self):
        return '<Player Stats %r>' % self.playerId

if __name__ == '__main__':

    if config.SQLALCHEMY_TYPE == 'sqlite':
        h.silentCreateDir(config.SQLALCHEMY_SQLITE_HOST)

    engine_string = config.SQLALCHEMY_DATABASE_URI
    engine = sql.create_engine(engine_string)

    # Create database only if it doesn't already exist
    if not database_exists(engine.url):
        logger.debug('Creating database at {}'.format(config.SQLALCHEMY_DATABASE_URI))
        create_database(engine.url)
        logger.info('MLB database created successfully')
    else:
        logger.info('Database already exists')

    # Drop all tables if they already exist
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    logger.info('Tables dropped and recreated successfully')