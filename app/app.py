import os
import sys
sys.path.append(os.environ.get('PYTHONPATH'))

import logging.config
from config import config
from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
import traceback
from datetime import datetime, timedelta

from models.mlb_database.create_database import Player, Team, CurrentStats, ProjectedStats, LastUpdate
from data.auxiliary.teamColors import teamColors
from data.auxiliary.divisionMapping import divisionMapping
from data.auxiliary.endOfSeason import endOfSeason

logging.config.fileConfig(config.LOGGING_CONFIG_FILE, disable_existing_loggers=False)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_pyfile(os.path.join(config.PROJECT_ROOT_DIR, 'config', 'config.py'))

db = SQLAlchemy(app)

@app.route('/')
def index():

    numPlayersToShow = 10

    try:
        nlMvp = db.session.query(Team, Player, ProjectedStats).\
            join(Player, Team.id == Player.currentTeamId).\
            join(ProjectedStats, Player.id == ProjectedStats.playerId).\
            filter(Team.league == 'NL').filter(ProjectedStats.mvpRank > 0).\
            order_by(ProjectedStats.mvpRank).limit(numPlayersToShow).all()

        alMvp = db.session.query(Team, Player, ProjectedStats).\
            join(Player, Team.id == Player.currentTeamId).\
            join(ProjectedStats, Player.id == ProjectedStats.playerId).\
            filter(Team.league == 'AL').filter(ProjectedStats.mvpRank > 0).\
            order_by(ProjectedStats.mvpRank).limit(numPlayersToShow).all()

        nlCyYoung = db.session.query(Team, Player, ProjectedStats).\
            join(Player, Team.id == Player.currentTeamId).\
            join(ProjectedStats, Player.id == ProjectedStats.playerId).\
            filter(Team.league == 'NL').filter(ProjectedStats.cyYoungRank > 0).\
            order_by(ProjectedStats.cyYoungRank).limit(numPlayersToShow).all()

        alCyYoung = db.session.query(Team, Player, ProjectedStats).\
            join(Player, Team.id == Player.currentTeamId).\
            join(ProjectedStats, Player.id == ProjectedStats.playerId).\
            filter(Team.league == 'AL').filter(ProjectedStats.cyYoungRank > 0).\
            order_by(ProjectedStats.cyYoungRank).limit(numPlayersToShow).all()

        nlwTeams = db.session.query(Team).filter(Team.division == 'NLW').\
            order_by(Team.teamName).all()

        nlcTeams = db.session.query(Team).filter(Team.division == 'NLC').\
            order_by(Team.teamName).all()

        nleTeams = db.session.query(Team).filter(Team.division == 'NLE').\
            order_by(Team.teamName).all()

        alwTeams = db.session.query(Team).filter(Team.division == 'ALW').\
            order_by(Team.teamName).all()

        alcTeams = db.session.query(Team).filter(Team.division == 'ALC').\
            order_by(Team.teamName).all()

        aleTeams = db.session.query(Team).filter(Team.division == 'ALE').\
            order_by(Team.teamName).all()

        lastUpdate = db.session.query(LastUpdate).first().lastUpdateDate
        lastUpdate = lastUpdate.strftime('%b %d')

        daysLeftDelta = endOfSeason[config.CURRENT_SEASON] - datetime.now()
        daysLeft = daysLeftDelta.days

        logger.debug('Index page accessed')
        return render_template('index.html', daysLeft=daysLeft, lastUpdate=lastUpdate,
            nlMvp=nlMvp, alMvp=alMvp, nlCyYoung=nlCyYoung, alCyYoung=alCyYoung,
            nlwTeams=nlwTeams, nlcTeams=nlcTeams, nleTeams=nleTeams,
            alwTeams=alwTeams, alcTeams=alcTeams, aleTeams=aleTeams)
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        logger.warning('Not able to display index page')
        return render_template('error.html')

@app.route('/player/<id>')
def player(id):
    try:
        player = db.session.query(Team, Player, CurrentStats, ProjectedStats).\
            join(Player, Team.id == Player.currentTeamId).\
            join(ProjectedStats, Player.id == ProjectedStats.playerId).\
            join(CurrentStats, Player.id == CurrentStats.playerId).\
            filter(Player.id == id).first()

        print(player)

        birthCity = player.Player.birthCity
        birthState = player.Player.birthState
        birthCountry = player.Player.birthCountry

        if len(birthState) > 0:
            hometown = '{}, {}, {}'.format(birthCity, birthState, birthCountry)
        else:
            hometown = '{}, {}'.format(birthCity, birthCountry)

        legend = ['Current as of XXX', 'End of Season Prediction']
        colors = [teamColors[player.Team.teamName]['primary'], teamColors[player.Team.teamName]['secondary']]
        
        if player.Player.position == 'P':
            current = [
                {'axis': 'Innings Pitched', 'value': player.CurrentStats.inningsPitched},
                {'axis': 'Wins', 'value': player.CurrentStats.wins},
                {'axis': 'Saves', 'value': player.CurrentStats.saves},
                {'axis': 'Strikeouts', 'value': player.CurrentStats.strikeouts},
                {'axis': 'ERA', 'value': player.CurrentStats.earnedRunAverage},
                {'axis': 'WHIP', 'value': player.CurrentStats.whip}
            ]

            projected = [
                {'axis': 'Innings Pitched', 'value': player.ProjectedStats.inningsPitched},
                {'axis': 'Wins', 'value': player.ProjectedStats.wins},
                {'axis': 'Saves', 'value': player.ProjectedStats.saves},
                {'axis': 'Strikeouts', 'value': player.ProjectedStats.strikeouts},
                {'axis': 'ERA', 'value': player.ProjectedStats.earnedRunAverage},
                {'axis': 'WHIP', 'value': player.ProjectedStats.whip}
            ]

            maxValue = [800, 40, 60, 400, 15, 5]

        else:
            current = [
                {'axis': 'At Bats', 'value': player.CurrentStats.atBats},
                {'axis': 'Hits', 'value': player.CurrentStats.hits},
                {'axis': 'Home Runs', 'value': player.CurrentStats.homeRuns},
                {'axis': 'RBIs', 'value': player.CurrentStats.runsBattedIn},
                {'axis': 'OPS', 'value': player.CurrentStats.onBasePlusSlug},
                {'axis': 'Runs', 'value': player.CurrentStats.homeRuns}
            ]

            projected = [
                {'axis': 'At Bats', 'value': player.ProjectedStats.atBats},
                {'axis': 'Hits', 'value': player.ProjectedStats.hits},
                {'axis': 'Home Runs', 'value': player.ProjectedStats.homeRuns},
                {'axis': 'RBIs', 'value': player.ProjectedStats.runsBattedIn},
                {'axis': 'OPS', 'value': player.ProjectedStats.onBasePlusSlug},
                {'axis': 'Runs', 'value': player.ProjectedStats.homeRuns}
            ]

            maxValue = [800, 300, 60, 200, 2, 60]

        stats = [current, projected]

        logger.debug('Player page accessed')
        return render_template('player.html', player=player,
            legend=legend, hometown=hometown, colors=colors,
            stats=stats, maxValue=maxValue)
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        logger.warning('Not able to display Player page')
        return render_template('error.html')

@app.route('/team/<id>')
def team(id):

    numPlayersToShow = 12

    try:
        team = db.session.query(Team).filter(Team.id == id).first()

        division = divisionMapping[team.division]
        location = '{}, {}'.format(team.city, team.state)

        mvpPlayers = db.session.query(Team, Player, ProjectedStats).\
            join(Player, Team.id == Player.currentTeamId).\
            join(ProjectedStats, Player.id == ProjectedStats.playerId).\
            filter(Team.id == id).filter(ProjectedStats.mvpRank > 0).\
            order_by(ProjectedStats.mvpRank).limit(numPlayersToShow).all()

        cyYoungPlayers = db.session.query(Team, Player, ProjectedStats).\
            join(Player, Team.id == Player.currentTeamId).\
            join(ProjectedStats, Player.id == ProjectedStats.playerId).\
            filter(Team.id == id).filter(ProjectedStats.cyYoungRank > 0).\
            order_by(ProjectedStats.cyYoungRank).limit(numPlayersToShow).all()

        logger.debug('Team page accessed')
        return render_template('team.html', team=team, division=division,
            location=location, mvpPlayers=mvpPlayers, cyYoungPlayers=cyYoungPlayers)

    except Exception as e:
        print(e)
        print(traceback.format_exc())
        logger.warning('Not able to display Team page')
        return render_template('error.html')

if __name__ == '__main__':
    app.run(host=app.config['HOST'], port=app.config['PORT'])