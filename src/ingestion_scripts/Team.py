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

    # Column numbers are indexed from zero
    # No longer need to subtract one
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
        if int(line[teamSchema['season']]) > maxYear:
            maxYear = int(line[teamSchema['season']])

    for line in s3File.splitlines(False)[1:]:
        line = line[1:][:-1].split('","')

        # Only pull most recent records
        if int(line[teamSchema['season'] - 1]) == maxYear:

            # No longer need to subtract one to index from zero
            teamId = int(line[teamSchema['id']])
            teamName = line[teamSchema['teamName']]
            venueName = line[teamSchema['venueName']]
            city = line[teamSchema['city']]
            state = line[teamSchema['state']]
            league = line[teamSchema['league']]
            division = line[teamSchema['division']]
            yearFounded = int(line[teamSchema['yearFounded']])
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
