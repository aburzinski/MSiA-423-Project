import logging
import os
import pandas as pd
 
logger = logging.getLogger(__name__)

currentDir = os.path.dirname(__file__)
parentDir = os.path.split(currentDir)[0]

cyYoungPath = os.path.join(parentDir, 'data', 'auxiliary')
cyYoung = pd.read_csv(os.path.join(cyYoungPath, 'cyYoungWinners.csv'), quotechar='"', encoding='latin-1')

playersPath = os.path.join(parentDir, 'data', 'historical')
players = pd.read_csv(os.path.join(playersPath, 'players.csv'), quotechar='"', encoding='latin-1')

merged = cyYoung.merge(players, how='left', left_on='Winner', right_on='name_display_first_last')

print(merged[merged['name_full'].isnull()])

