import os
import sys
sys.path.append(os.environ.get('PYTHONPATH'))

import logging.config
from config import config
from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy

from models.mlb_database.create_database import Player, Team, CurrentStats
from data.auxiliary.teamColors import teamColors

logging.config.fileConfig(config.LOGGING_CONFIG_FILE, disable_existing_loggers=False)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_pyfile(os.path.join(config.PROJECT_ROOT_DIR, 'config', 'config.py'))

db = SQLAlchemy(app)

@app.route('/')
def index():

    numPlayersToShow = 10

    try:
        nlMvp = db.session.query(Team, Player, CurrentStats).\
            join(Player, Team.id == Player.currentTeamId).\
            join(CurrentStats, Player.id == CurrentStats.playerId).\
            filter(Team.league == 'NL').\
            order_by(CurrentStats.mvpRank).limit(numPlayersToShow).all()

        alMvp = db.session.query(Team, Player, CurrentStats).\
            join(Player, Team.id == Player.currentTeamId).\
            join(CurrentStats, Player.id == CurrentStats.playerId).\
            filter(Team.league == 'AL').\
            order_by(CurrentStats.mvpRank).limit(numPlayersToShow).all()

        nlCyYoung = db.session.query(Team, Player, CurrentStats).\
            join(Player, Team.id == Player.currentTeamId).\
            join(CurrentStats, Player.id == CurrentStats.playerId).\
            filter(Team.league == 'NL').\
            order_by(CurrentStats.cyYoungRank).limit(numPlayersToShow).all()

        alCyYoung = db.session.query(Team, Player, CurrentStats).\
            join(Player, Team.id == Player.currentTeamId).\
            join(CurrentStats, Player.id == CurrentStats.playerId).\
            filter(Team.league == 'AL').\
            order_by(CurrentStats.cyYoungRank).limit(numPlayersToShow).all()


        logger.debug('Index page accessed')
        return render_template('index.html',
            nlMvp=nlMvp, alMvp=alMvp, nlCyYoung=nlCyYoung, alCyYoung=alCyYoung)
    except Exception as e:
        print(e)
        logger.warning('Not able to display index page')
        return render_template('error.html')

@app.route('/player/<id>')
def player(id):
    try:
        player = db.session.query(Team, Player).join(Player).filter(Player.id == id).first()

        birthCity = player.Player.birthCity
        birthState = player.Player.birthState
        birthCountry = player.Player.birthCountry

        if len(birthState) > 0:
            hometown = '{}, {}, {}'.format(birthCity, birthState, birthCountry)
        else:
            hometown = '{}, {}'.format(birthCity, birthCountry)

        colors = [teamColors[player.Team.teamName]['primary'], teamColors[player.Team.teamName]['secondary']]
        print(colors)

        logger.debug('Player page accessed')
        return render_template('player.html', player=player, hometown=hometown,
            test='qwerty', colors=colors)
    except Exception as e:
        print(e)
        logger.warning('Not able to display Player page')
        return render_template('error.html')

if __name__ == '__main__':
    app.run(host=app.config['HOST'], port=app.config['PORT'])