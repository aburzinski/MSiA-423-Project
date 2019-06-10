import os
import sys
sys.path.append(os.environ.get('PYTHONPATH'))

import logging.config
from config import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import src.helpers.helpers as h
import src.helpers.azureHelpers as ah
from data.auxiliary.teamMapping import teamMapping

parentDir = config.PROJECT_ROOT_DIR
logging.config.fileConfig(config.LOGGING_CONFIG_FILE, disable_existing_loggers=False)
logger = logging.getLogger(__name__)

from models.mlb_database.create_database import Base, Team

def ingestTeams(s3File, session, truncate=True):
    
    if truncate:
        session.query(Team).delete()

    columns = s3File.splitlines(False)[0]
    columns = columns[1:][:-1].split('","')

    # Column numbers are indexed from one
    teamSchema = {
        'id': columns.index('team_id'),
        'teamName': columns.index('name_display_long'),
        'venueName': columns.index('venue_name'),
        'city': columns.index('city'),
        'state': columns.index('state'),
        'league': columns.index('league'),
        'division': columns.index('division_abbrev'),
        'yearFounded': columns.index('first_year_of_play'),
        'season': columns.index('season')
    }

    teamCount = 0
    maxYear = 0

    for line in s3File.splitlines(False)[1:]:
        line = line[1:][:-1].split('","')
        if int(line[teamSchema['season'] - 1]) > maxYear:
            maxYear = int(line[teamSchema['season'] - 1])

    for line in s3File.splitlines(False)[1:]:
        line = line[1:][:-1].split('","')

        # Only pull most recent records
        if int(line[teamSchema['season'] - 1]) == maxYear:

            # Need to subtract one to index from zero
            teamId = int(line[teamSchema['id'] - 1])
            teamName = line[teamSchema['teamName'] - 1]
            venueName = line[teamSchema['venueName'] - 1]
            city = line[teamSchema['city'] - 1]
            state = line[teamSchema['state'] - 1]
            league = line[teamSchema['league'] - 1]
            division = line[teamSchema['division'] - 1]
            yearFounded = int(line[teamSchema['yearFounded'] - 1])
            teamAbbrev = teamMapping[teamName]
            
            new_team = Team(id=teamId,
                teamName=teamName,
                venueName=venueName,
                city=city,
                state=state,
                league=league,
                division=division,
                yearFounded=yearFounded,
                teamAbbrev=teamAbbrev
            )
            session.add(new_team)
            teamCount += 1

    session.commit()
    logging.info('Added {} teams to database successfully'.format(str(teamCount)))
