import os
import logging.config
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, MetaData
from sqlalchemy.orm import sessionmaker
import sqlalchemy as sql

currentDir = os.path.dirname(__file__)
parentDir = os.path.split(currentDir)[0]
parentDir = os.path.split(parentDir)[0]
logging.config.fileConfig(os.path.join(parentDir, 'config', 'logging', 'local.conf'))
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
    engine_string = 'sqlite:///mlb.db'
    engine = sql.create_engine(engine_string)

    Base.metadata.create_all(engine)
    logger.info('MLB database created successfully')