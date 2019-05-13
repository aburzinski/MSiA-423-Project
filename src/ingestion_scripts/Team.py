import sys
sys.path.append(r'C:\Users\aburz\OneDrive\Documents\Northwestern\Classes\MSiA 423\Project\MSiA-423-Project')

import logging.config
from config import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import src.helpers.helpers as h
import src.helpers.azure as ah

parentDir = config.PROJECT_ROOT_DIR
logging.config.fileConfig(config.LOGGING_CONFIG_FILE, disable_existing_loggers=False)
logger = logging.getLogger(__name__)

from models.mlb_database.create_database import Base, Team

def ingestTeams(s3File, session, truncate=True):
    
    if truncate:
        session.query(Team).delete()

    # Column numbers are indexed from one
    teamSchema = {
        'id': 37,
        'teamName': 8,
        'venueName': 2,
        'city': 7,
        'state': 40,
        'league': 23,
        'division': 43,
        'yearFounded': 48
    }

    teamCount = 0
    maxYear = 0

    for line in s3File.splitlines(False)[1:]:
        line = line[1:][:-1].split('","')
        if int(line[32]) > maxYear:
            maxYear = int(line[32])

    for line in s3File.splitlines(False)[1:]:
        line = line[1:][:-1].split('","')

        # Only pull most recent records
        if int(line[32]) == maxYear:

            # Need to subtract one to index from zero
            teamId = int(line[teamSchema['id'] - 1])
            teamName = line[teamSchema['teamName'] - 1]
            venueName = line[teamSchema['venueName'] - 1]
            city = line[teamSchema['city'] - 1]
            state = line[teamSchema['state'] - 1]
            league = line[teamSchema['league'] - 1]
            yearFounded = int(line[teamSchema['yearFounded'] - 1])
            
            new_team = Team(id=teamId,
                teamName=teamName,
                venueName=venueName,
                city=city,
                state=state,
                league=league,
                yearFounded=yearFounded
            )
            session.add(new_team)
            teamCount += 1

    session.commit()
    logging.info('Added {} teams to database successfully'.format(str(teamCount)))