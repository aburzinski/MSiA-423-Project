import sys
import os
sys.path.append(os.environ.get('PYTHONPATH'))
from config import config

def nineInningNormalize(df, statColumn, inningsPitchedColumn = 'ip'):
    """Return a statistic normalized to nine innings.
        To be used on pitching statistics such as home runs per 9 innings

        Args:
            df(`DataFrame`): The data frame with the column to normalize
            statColumn(`str`): The name of the column to normalize
            inningsPitchedColumn(`str`): The name of the column with the number of innings pitched
    """
    return df[statColumn] * 9/(df[inningsPitchedColumn] % 1 * 10 / 3 + df[inningsPitchedColumn].round())

def atBatNormalize(df, statColumn, atBatColumn):
    """Return a statistic normalized by the number of at bats.
        To be used on hitting statistics such as home runs per at bat

        Args:
            df(`DataFrame`): The data frame with the column to normalize
            statColumn(`str`): The name of the column to normalize
            atBatColumn(`str`): The name of the column with the number of at bats
    """
    return df[statColumn] / df[atBatColumn]