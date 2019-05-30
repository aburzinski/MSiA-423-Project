import os
import sys
sys.path.append(os.environ.get('PYTHONPATH'))

teamColors = {
    'Arizona Diamondbacks': {
        'primary': '#A71930',
        'secondary': '#E3D4AD'
    },
    'Atlanta Braves': {
        'primary': '#13274F',
        'secondary': '#CE1141'
    },
    'Baltimore Orioles': {
        'primary': '#DF4601',
        'secondary': '#000000'
    },
    'Boston Red Sox': {
        'primary': '#BD3039',
        'secondary': '#0C2340'
    },
    'Chicago Cubs': {
        'primary': '#0E3386',
        'secondary': '#CC3433'
    },
    'Chicago White Sox': {
        'primary': '#27251F',
        'secondary': '#C4CED4'
    },
    'Cincinnati Reds': {
        'primary': '#C6011F',
        'secondary': '#000000'
    },
    'Cleveland Indians': {
        'primary': '#0C2340',
        'secondary': '#E31937'
    },
    'Colorado Rockies': {
        'primary': '#33006F',
        'secondary': '#C4CED4'
    },
    'Detroit Tigers': {
        'primary': '#0C2340',
        'secondary': '#FA4616'
    },
    'Houston Astros': {
        'primary': '#002D62',
        'secondary': '#EB6E1F'
    },
    'Kansas City Royals': {
        'primary': '#004687',
        'secondary': '#BD9B60'
    },
    'Los Angeles Angels': {
        'primary': '#BA0021',
        'secondary': '#003263'
    },
    'Los Angeles Dodgers': {
        'primary': '#005A9C',
        'secondary': '#A5ACAF'
    },
    'Miami Marlins': {
        'primary': '#000000',
        'secondary': '#00A3E0'
    },
    'Milwaukee Brewers': {
        'primary': '#0A2351',
        'secondary': '#B6922E'
    },
    'Minnesota Twins': {
        'primary': '#002B5C',
        'secondary': '#D31145'
    },
    'New York Mets': {
        'primary': '#002D72',
        'secondary': '#FF5910'
    },
    'New York Yankees': {
        'primary': '#0C2340',
        'secondary': '#C4CED3'
    },
    'Oakland Athletics': {
        'primary': '#003831',
        'secondary': '#EFB21E'
    },
    'Philadelphia Phillies': {
        'primary': '#E81828',
        'secondary': '#002D72'
    },
    'Pittsburgh Pirates': {
        'primary': '#FDB827',
        'secondary': '#27251F'
    },
    'San Diego Padres': {
        'primary': '#002D62',
        'secondary': '#A2AAAD'
    },
    'San Francisco Giants': {
        'primary': '#FD5A1E',
        'secondary': '#27251F'
    },
    'Seattle Mariners': {
        'primary': '#0C2C56',
        'secondary': '#005C5C'
    },
    'St. Louis Cardinals': {
        'primary': '#C41E3A',
        'secondary': '#0C2340'
    },
    'Tampa Bay Rays': {
        'primary': '#092C5C',
        'secondary': '#8FBCE6'
    },
    'Texas Rangers': {
        'primary': '#003278',
        'secondary': '#C0111F'
    },
    'Toronto Blue Jays': {
        'primary': '#134A8E',
        'secondary': '#E8291C'
    },
    'Washington Nationals': {
        'primary': '#E8291C',
        'secondary': '#14225A'
    }
}