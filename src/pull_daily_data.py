import os
import sys
sys.path.append(os.environ.get('PYTHONPATH'))

import logging.config
from config import config
import requests
import json
import src.helpers.helpers as h

parentDir = config.PROJECT_ROOT_DIR
writeToDir = os.path.join(parentDir, 'data', 'daily')

logging.config.fileConfig(config.LOGGING_CONFIG_FILE, disable_existing_loggers=False)
logger = logging.getLogger(__name__)


def pullStats(baseURL, statType, playerYears, currProj):
    """Receive statistical data from API calls based on a playerid and seasonid.

        Arguments:
            baseURL (`str`): The base URL of the API
            statType (`str`): Specifies the type of data to collect.
                Either 'hitting' or 'pitching'
            playerYear (`dict`): A dictionary with keys of a unique player id
                and values of a set of years that player was active.
            currProj (`str`): Get current or projected season stats.
                Either 'current' or 'projected'
    """
    writeHeaders = True
    fileName = statType + currProj.capitalize() + '.csv'
    h.silentRemove(os.path.join(writeToDir, fileName))

    with open(os.path.join(writeToDir, fileName), 'a') as f:
        for player in playerYears.keys():
            for year in playerYears[player]:
                if year >= config.CURRENT_SEASON and year <= config.CURRENT_SEASON:

                    if currProj == 'current':
                        endpoint = 'sport_' + statType + '_tm'
                    elif currProj == 'projected':
                        if statType == 'hitting':
                            statType = 'batting'
                        endpoint = 'proj_pecota_' + statType
                    else:
                        raise ValueError('Incorrent value of currProj parameter')


                    statsURL = '/json/named.' + endpoint + '.bam'

                    if currProj == 'current':
                        options = '?sport_code=%27mlb%27&game_type=%27R%27'
                        options += '&season=' + str(year)
                        options += '&player_id=' + player

                        columns = '&' +endpoint + '.col_ex=sport_code'
                        columns += '&' +endpoint + '.col_ex=team_full'
                        columns += '&' +endpoint + '.col_ex=league_full'
                        columns += '&' +endpoint + '.col_ex=team_abbrev'
                        columns += '&' +endpoint + '.col_ex=end_date'
                        columns += '&' +endpoint + '.col_ex=league_short'
                        columns += '&' +endpoint + '.col_ex=sport'
                        columns += '&' +endpoint + '.col_ex=team_short'

                    elif currProj == 'projected':
                        options = '?season=' + str(year)
                        options += '&player_id=' + player

                        columns = ''

                    fullURL = baseURL + statsURL + options + columns
                    r = requests.get(fullURL)
                    
                    if int(json.loads(r.text)[endpoint]['queryResults']['totalSize']) > 1:
                        if writeHeaders:
                            h.writeIterLine(json.loads(r.text)[endpoint]['queryResults']['row'][0].keys(), f)
                            writeHeaders = False
                        for row in json.loads(r.text)[endpoint]['queryResults']['row']:
                            h.writeIterLine(row.values(), f)
                    
                    if int(json.loads(r.text)[endpoint]['queryResults']['totalSize']) == 1:
                        if writeHeaders:
                            h.writeIterLine(json.loads(r.text)[endpoint]['queryResults']['row'].keys(), f)
                            writeHeaders = False
                        h.writeIterLine(json.loads(r.text)[endpoint]['queryResults']['row'].values(), f)
    
    f.close()


if __name__ == '__main__':

    baseURL = 'http://lookup-service-prod.mlb.com'

    startYear = config.CURRENT_SEASON
    endYear = config.CURRENT_SEASON

    h.silentCreateDir(writeToDir)
    logger.debug('Writing data to path ' + writeToDir)

    # Get Team Ids
    teamIds = {}

    for year in range(startYear, endYear + 1):
        endpoint = 'team_all_season'
        column = 'team_id'
        teamURL = '/json/named.' + endpoint + '.bam'
        options = '?sport_code=%27mlb%27&all_star_sw=%27N%27'
        options += '&season=' + str(year)
        columns = '&' +endpoint + '.col_in=' + column
        fullURL = baseURL + teamURL + options + columns
        r = requests.get(fullURL)
        for record in json.loads(r.text)[endpoint]['queryResults']['row']:
            if record[column] not in teamIds.keys():
                teamIds[record[column]] = [year, year]
            else:
                teamIds[record[column]][1] = year

    logger.debug('Got data on ' + str(len(teamIds)) + ' teams')

    # Get players by year

    playerYears = {}

    for teamId in teamIds.keys():
        endpoint = 'roster_team_alltime'
        column1 = 'player_id'
        column2 = 'stat_years'
        playerURL = '/json/named.' + endpoint + '.bam'
        options = '?start_season=' + str(teamIds[teamId][0]) + '&end_season=' + str(teamIds[teamId][1])
        options += '&team_id=' + teamId
        columns = '&' +endpoint + '.col_in=' + column1
        columns += '&' +endpoint + '.col_in=' + column2

        fullURL = baseURL + playerURL + options + columns
        r = requests.get(fullURL)

        for record in json.loads(r.text)[endpoint]['queryResults']['row']:
            if record[column1] not in playerYears.keys():
                playerYears[record[column1]] = set()

            playerYears[record[column1]] = playerYears[record[column1]].union({config.CURRENT_SEASON})

    logger.debug('Got data on ' + str(len(playerYears)) + ' players')

    # Get current hitting stats
    logger.info('Creating hittingCurrent.csv file')
    pullStats(baseURL, 'hitting', playerYears, 'current')

    # Get current pitching stats
    logger.info('Creating pitchingCurrent.csv file')
    pullStats(baseURL, 'pitching', playerYears, 'current')

    # Get current hitting stats
    logger.info('Creating hittingProjected.csv file')
    pullStats(baseURL, 'hitting', playerYears, 'projected')

    # Get current pitching stats
    logger.info('Creating pitchingProjected.csv file')
    pullStats(baseURL, 'pitching', playerYears, 'projected')

    logger.info('All files created successfully')