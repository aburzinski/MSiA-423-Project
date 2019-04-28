import logging
import requests
import json
import os
import helpers.helpers as h
 
logging.basicConfig(level=logging.DEBUG,
    format='%(name)s - %(levelname)s - %(asctime)s - %(message)s'
)

logger = logging.getLogger(__name__)

baseURL = 'http://lookup-service-prod.mlb.com'

startYear = 2017
endYear = 2018

currentDir = os.path.dirname(__file__)
parentDir = os.path.split(currentDir)[0]
writeToDir = os.path.join(parentDir, 'data', 'historical')

logger.debug('Writing data to path ' + writeToDir)

def parseYearString(yearString):
    yearList = set()
    splitString = yearString.split(', ')
    for string in splitString:
        if string.find('-') == -1:
            yearList.add(int(string))
        else:
            for year in range(int(string[0:4]), int(string[5:]) + 1):
                yearList.add(year)

    return yearList


def writeIterLine(iter, f):
    elems = []
    for elem in iter:
        elems.append(elem)
    f.write(','.join(elems) + '\n')


def pullStatsHistory(histType, playerYears):
    writeHeaders = True
    h.silentRemove(os.path.join(writeToDir, histType + 'Historical.csv'))

    with open(os.path.join(writeToDir, histType + 'Historical.csv'), 'a') as f:
        for player in playerYears.keys():
            for year in playerYears[player]:
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
                        writeIterLine(json.loads(r.text)[endpoint]['queryResults']['row'][0].keys(), f)
                        writeHeaders = False
                    for row in json.loads(r.text)[endpoint]['queryResults']['row']:
                        writeIterLine(row.values(), f)
                
                if int(json.loads(r.text)[endpoint]['queryResults']['totalSize']) == 1:
                    if writeHeaders:
                        writeIterLine(json.loads(r.text)[endpoint]['queryResults']['row'].keys(), f)
                        writeHeaders = False
                    writeIterLine(json.loads(r.text)[endpoint]['queryResults']['row'].values(), f)
    
    f.close()

# Get Team Ids
teamIds = set()

for year in range(startYear, endYear):
    endpoint = 'team_all_season'
    column = 'team_id'
    teamURL = '/json/named.' + endpoint + '.bam'
    options = '?sport_code=%27mlb%27&all_star_sw=%27N%27'
    options += '&season=' + str(year)
    columns = '&' +endpoint + '.col_in=' + column
    fullURL = baseURL + teamURL + options + columns
    r = requests.get(fullURL)
    for record in json.loads(r.text)[endpoint]['queryResults']['row']:
        teamIds.add(record[column])


# Get players by year

playerYears = {}

for teamId in teamIds:
    # if teamId == str(146):
    endpoint = 'roster_team_alltime'
    column1 = 'player_id'
    column2 = 'stat_years'
    playerURL = '/json/named.' + endpoint + '.bam'
    options = '?start_season=' + str(startYear) + '&end_season=' + str(endYear)
    options += '&team_id=' + teamId
    columns = '&' +endpoint + '.col_in=' + column1
    columns += '&' +endpoint + '.col_in=' + column2

    fullURL = baseURL + playerURL + options + columns
    r = requests.get(fullURL)

    for record in json.loads(r.text)[endpoint]['queryResults']['row']:
        if record[column1] not in playerYears.keys():
            playerYears[record[column1]] = set()

        playerYears[record[column1]] = playerYears[record[column1]].union(parseYearString(record[column2]))


# Get historical hitting stats
pullStatsHistory('hitting', playerYears)

# Get historical pitching stats
pullStatsHistory('pitching', playerYears)
