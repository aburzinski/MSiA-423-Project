import os
import sys
sys.path.append(os.environ.get('PYTHONPATH'))

from wtforms import Form, DecimalField, IntegerField, validators

class BattingForm(Form):

    atBats = IntegerField('At Bats:', validators=[validators.required()])
    hits = IntegerField('Hits:', validators=[validators.required()])
    homeRuns = IntegerField('Home Runs:', validators=[validators.required()])
    rbis = IntegerField('Runs Batted In:', validators=[validators.required()])
    strikeouts = IntegerField('Strikeouts:', validators=[validators.required()])
    walks = IntegerField('Walks:', validators=[validators.required()])

class PitchingForm(Form):

    inningsPitched = IntegerField('Innings Pitched:', validators=[validators.required()])
    wins = IntegerField('Wins:', validators=[validators.required()])
    saves = IntegerField('Saves:', validators=[validators.required()])
    strikeouts = IntegerField('Strikeouts:', validators=[validators.required()])
    era = IntegerField('Era:', validators=[validators.required()])
    whip = IntegerField('Whip:', validators=[validators.required()])