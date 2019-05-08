import sys
sys.path.append(r'C:\Users\aburz\OneDrive\Documents\Northwestern\Classes\MSiA 423\Project\MSiA-423-Project')

import logging.config
from config import config
import requests
import json
import os
import src.helpers.helpers as h

parentDir = config.PROJECT_ROOT_DIR
writeToDir = os.path.join(parentDir, 'data', 'historical')

logging.config.fileConfig(config.LOGGING_CONFIG_FILE, disable_existing_loggers=False)
logger = logging.getLogger(__name__)

def parseYearString(yearString):
    """ Parse the API returned string of years to a list of ints.
    Ex. Converts '2015-2017, 2019' to a list of [2015, 2016, 2017, 2019]
    """
    yearSet = set()
    if len(yearString) < 1:
        return yearSet

    splitString = yearString.split(', ')
    for stringPart in splitString:
        if stringPart.find('-') == -1:
            yearSet.add(int(stringPart))
        else:
            for year in range(int(stringPart[0:4]), int(stringPart[5:]) + 1):
                yearSet.add(year)

    return yearSet


def pullStatsHistory(baseURL, histType, playerYears, startYear, endYear):
    """ Receive statistical data from API calls based on a playerid and seasonid.

        Arguments:
            histType (str): Specifies the type of data to collect.
                Either 'hitting' or 'pitching'
            playerYear (dict): A dictionary with keys of a unique player id
                and values of a set of years that player was active
    """
    writeHeaders = True
    h.silentRemove(os.path.join(writeToDir, histType + 'Historical.csv'))

    with open(os.path.join(writeToDir, histType + 'Historical.csv'), 'a') as f:
        for player in playerYears.keys():
            for year in playerYears[player]:
                if year >= startYear and year <= endYear:
                    endpoint = 'sport_' + histType + '_tm'
                    hittingURL = '/json/named.' + endpoint + '.bam'
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

                    fullURL = baseURL + hittingURL + options + columns
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

def pullTeams(baseURL, startYear = 2019, endYear = 2020):
    """ Pull MLB team data for each season between startYear and endYear """
    writeHeaders = True
    h.silentRemove(os.path.join(writeToDir, 'teams.csv'))

    with open(os.path.join(writeToDir, 'teams.csv'), 'a') as f:
        for year in range(startYear, endYear):
            endpoint = 'team_all_season'
            teamURL = '/json/named.' + endpoint + '.bam'
            options = '?sport_code=%27mlb%27&all_star_sw=%27N%27'
            options += '&season=' + str(year)
            fullURL = baseURL + teamURL + options
            r = requests.get(fullURL)

            if writeHeaders:
                h.writeIterLine(json.loads(r.text)[endpoint]['queryResults']['row'][0].keys(), f)
                writeHeaders = False
            for row in json.loads(r.text)[endpoint]['queryResults']['row']:
                h.writeIterLine(row.values(), f)
    
    f.close()

def pullPlayers(baseURL, playerYears):
    """ Pull data about each player

        Use the playerYears dictionary to ensure that each player that
        has stats will also have related data
    """
    writeHeaders = True
    h.silentRemove(os.path.join(writeToDir, 'players.csv'))

    with open(os.path.join(writeToDir, 'players.csv'), 'a') as f:
        for player in playerYears.keys():
            endpoint = 'player_info'
            column1 = 'player_id'
            playerURL = '/json/named.' + endpoint + '.bam'
            options = '?sport_code=%27mlb%27'
            options += '&player_id=' + player
            fullURL = baseURL + playerURL + options
            r = requests.get(fullURL)

            if writeHeaders:
                h.writeIterLine(json.loads(r.text)[endpoint]['queryResults']['row'].keys(), f)
                writeHeaders = False
            h.writeIterLine(json.loads(r.text)[endpoint]['queryResults']['row'].values(), f)

    f.close()


if __name__ == '__main__':
    baseURL = 'http://lookup-service-prod.mlb.com'

    startYear = 1960
    endYear = 2018

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

            playerYears[record[column1]] = playerYears[record[column1]].union(parseYearString(record[column2]))

    logger.debug('Got data on ' + str(len(playerYears)) + ' players')

    # Get Team Data
    logger.info('Creating teams.csv file')
    pullTeams(baseURL, startYear, endYear)

    # Get Player Data
    logger.info('Creating players.csv file')
    pullPlayers(baseURL, playerYears)

    # Get historical hitting stats
    logger.info('Creating hittingHistorical.csv file')
    pullStatsHistory(baseURL, 'hitting', playerYears, startYear, endYear)

    # Get historical pitching stats
    logger.info('Creating pitchingHistorical.csv file')
    pullStatsHistory(baseURL, 'pitching', playerYears, startYear, endYear)