import os
import sys
sys.path.append(os.environ.get('PYTHONPATH'))

import logging.config
from config import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import src.helpers.helpers as h
import src.helpers.azureHelpers as ah

parentDir = config.PROJECT_ROOT_DIR
logging.config.fileConfig(config.LOGGING_CONFIG_FILE, disable_existing_loggers=False)
logger = logging.getLogger(__name__)

from models.mlb_database.create_database import Base, Player

def ingestPlayers(s3File, session, truncate=True):
    
    if truncate:
        session.query(Player).delete()

    # Column numbers are indexed from one
    playerSchema = {
        'id': 24,
        'playerName': 3,
        'birthCity': 40,
        'birthState': 30,
        'birthCountry': 1,
        'age': 7,
        'heightInches': 5,
        'heightFeet': 10,
        'weight': 31,
        'debutDate': 11,
        'position': 20,
        'currentTeamId': 27
    }

    playerCount = 0

    for line in s3File.splitlines(False)[1:]:
        line = line[1:][:-1].split('","')

        # Need to subtract one to index from zero
        playerId = int(line[playerSchema['id'] - 1])
        playerName = line[playerSchema['playerName'] - 1]
        birthCity = line[playerSchema['birthCity'] - 1]
        birthState = line[playerSchema['birthState'] - 1]
        birthCountry = line[playerSchema['birthCountry'] - 1]
        age = int(line[playerSchema['age'] - 1])
        height = line[playerSchema['heightFeet'] - 1] + '\'' + line[playerSchema['heightInches'] - 1] + '"'
        weight = int(line[playerSchema['weight'] - 1])
        debutDate = h.textParseDate(line[playerSchema['debutDate'] - 1])
        position = line[playerSchema['position'] - 1]
        currentTeamId = int(line[playerSchema['currentTeamId'] - 1])
        
        new_player = Player(id=playerId,
            playerName=playerName,
            birthCity=birthCity,
            birthState=birthState,
            birthCountry=birthCountry,
            age=age,
            height=height,
            weight=weight,
            debutDate=debutDate,
            position=position,
            currentTeamId=currentTeamId
        )
        session.add(new_player)
        playerCount += 1

    session.commit()
    logging.info('Added {} players to database successfully'.format(str(playerCount)))
