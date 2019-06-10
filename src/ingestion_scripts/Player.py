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

    columns = s3File.splitlines(False)[0]
    columns = columns[1:][:-1].split('","')

    # Column numbers are indexed from one
    playerSchema = {
        'id': columns.index('player_id'),
        'playerName': columns.index('name_display_first_last'),
        'birthCity': columns.index('birth_city'),
        'birthState': columns.index('birth_state'),
        'birthCountry': columns.index('birth_country'),
        'age': columns.index('age'),
        'heightInches': columns.index('height_index'),
        'heightFeet': columns.index('height_feet'),
        'weight': columns.index('weight'),
        'debutDate': columns.index('pro_debut_date'),
        'position': columns.index('primary_position_txt'),
        'currentTeamId': columns.index('team_id')
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
