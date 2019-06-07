import logging.config
import os
import errno
from config import config

logging.config.fileConfig(config.LOGGING_CONFIG_FILE)
logger = logging.getLogger(__name__)

def silentRemove(fileName):
    """ Delete file if it exists, other don't do anything """
    try:
        os.remove(fileName)
        logger.debug('Removed file ' + fileName)
    except OSError as e:
        if e.errno != errno.ENOENT:  # File not found error
            raise
        else:
            logger.debug('File not deleted since it doesn\'t exist')


def silentCreateDir(dirName):
    """ Create directory if it doesn't already exist """
    if not os.path.exists(dirName):
        os.makedirs(dirName)
        logger.debug('Created directory ' + dirName)


def writeIterLine(iter, f):
    """Take an iterator of strings and create one line of a csv from them
    Args:
        iter (An iterator of `str` objects): An iterator of string objects
            Created wither from dict keys or dict values
        f (file object): The file to write to
    """
    elems = []
    for elem in iter:
        elems.append(elem)
    f.write(('"' + '","'.join(elems) + '"\n').encode('latin-1'))

def textParseDate(origDate):
    """Take a date of the format YYYY-MM-DDTHH:MM:SS and parse
        it to YYYY/MM/DD
    """
    if len(origDate) == 0:
        return ''
    else:
        year = origDate[0:4]
        month = origDate[5:7]
        day = origDate[8:10]

        try:
            yearInt = int(year)
            monthInt = int(month)
            dayInt = int(day)
        except ValueError:
            raise ValueError('Input date not in the correct formate')
        
        return year + '/' + month + '/' + day


def appendNumberEnding(number):
    """This function appends the ending of a number to be human readable
        For example, this will changed 4 to 4th and 21 to 21st

        Args:
            number (`int`): The number to be converted to human readable string
        Returns:
            (`str`): The human readable number representation
    """
    if not isinstance(number, int):
        raise ValueError('Please enter an integer value')

    if number % 100 == 11 or number % 100 == 12 or number % 100 == 13:
        return str(number) + 'th'
    elif number % 10 == 1:
        return str(number) + 'st'
    elif number % 10 == 2:
        return str(number) + 'nd'
    elif number % 10 == 3:
        return str(number) + 'rd'
    else:
        return str(number) + 'th'