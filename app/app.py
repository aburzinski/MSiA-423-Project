import os
import sys
sys.path.append(os.environ.get('PYTHONPATH'))

import logging.config
from config import config
from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import traceback
from datetime import datetime, timedelta

from models.mlb_database.create_database import Player, Team, CurrentStats, ProjectedStats, LastUpdate
from data.auxiliary.teamColors import teamColors
from data.auxiliary.divisionMapping import divisionMapping
from data.auxiliary.endOfSeason import endOfSeason
from static.forms import BattingForm, PitchingForm

logging.config.fileConfig(config.LOGGING_CONFIG_FILE, disable_existing_loggers=False)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_pyfile(os.path.join(config.PROJECT_ROOT_DIR, 'config', 'config.py'))

db = SQLAlchemy(app)

UTC_OFFSET_TIMEDELTA = datetime.utcnow() - datetime.now()

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

        players = db.session.query(Player).join(ProjectedStats).order_by(Player.playerName).all()
        print(players[0])

        lastUpdate = db.session.query(LastUpdate).first().lastUpdateDate
        lastUpdateLocal = lastUpdate - UTC_OFFSET_TIMEDELTA
        lastUpdateLocal = lastUpdateLocal.strftime('%b %d')

        daysLeftDelta = endOfSeason[config.CURRENT_SEASON] - datetime.now()
        daysLeft = daysLeftDelta.days

        logger.debug('Index page accessed')
        return render_template('index.html', daysLeft=daysLeft, lastUpdate=lastUpdateLocal,
            nlMvp=nlMvp, alMvp=alMvp, nlCyYoung=nlCyYoung, alCyYoung=alCyYoung,
            nlwTeams=nlwTeams, nlcTeams=nlcTeams, nleTeams=nleTeams,
            alwTeams=alwTeams, alcTeams=alcTeams, aleTeams=aleTeams,
            players=players)
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        logger.warning('Not able to display index page')
        return render_template('error.html')

@app.route('/player/<id>', methods=['GET', 'POST'])
def player(id):
    try:
        player = db.session.query(Team, Player, CurrentStats, ProjectedStats).\
            join(Player, Team.id == Player.currentTeamId).\
            join(ProjectedStats, Player.id == ProjectedStats.playerId).\
            join(CurrentStats, Player.id == CurrentStats.playerId).\
            filter(Player.id == id).first()

        birthCity = player.Player.birthCity
        birthState = player.Player.birthState
        birthCountry = player.Player.birthCountry

        if len(birthState) > 0:
            hometown = '{}, {}, {}'.format(birthCity, birthState, birthCountry)
        else:
            hometown = '{}, {}'.format(birthCity, birthCountry)

        lastUpdate = db.session.query(LastUpdate).first().lastUpdateDate
        lastUpdateLocal = lastUpdate - UTC_OFFSET_TIMEDELTA
        lastUpdateLocal = lastUpdateLocal.strftime('%b %d')

        legend = ['End of Season Prediction', 'Current as of {}'.format(lastUpdateLocal)]
        colors = [teamColors[player.Team.teamName]['primary'], teamColors[player.Team.teamName]['secondary']]
        
        if player.Player.position == 'P':
            current = [
                {'axis': 'Innings Pitched', 'value': player.CurrentStats.inningsPitched},
                {'axis': 'Wins', 'value': player.CurrentStats.wins},
                {'axis': 'Saves', 'value': player.CurrentStats.saves},
                {'axis': 'Strikeouts', 'value': player.CurrentStats.strikeoutsPitching},
                {'axis': 'ERA', 'value': player.CurrentStats.earnedRunAverage},
                {'axis': 'WHIP', 'value': player.CurrentStats.whip}
            ]

            projected = [
                {'axis': 'Innings Pitched', 'value': player.ProjectedStats.inningsPitched},
                {'axis': 'Wins', 'value': player.ProjectedStats.wins},
                {'axis': 'Saves', 'value': player.ProjectedStats.saves},
                {'axis': 'Strikeouts', 'value': player.ProjectedStats.strikeoutsPitching},
                {'axis': 'ERA', 'value': player.ProjectedStats.earnedRunAverage},
                {'axis': 'WHIP', 'value': player.ProjectedStats.whip}
            ]

            maxValues = db.session.query(func.max(ProjectedStats.inningsPitched), 
                func.max(ProjectedStats.wins),
                func.max(ProjectedStats.saves),
                func.max(ProjectedStats.strikeoutsPitching),
                func.max(ProjectedStats.earnedRunAverage),
                func.max(ProjectedStats.whip)).first()

            limits = [1.25 * maxValue for maxValue in maxValues]

            form = PitchingForm(request.form, inningsPitched=player.ProjectedStats.inningsPitched,
                wins=player.ProjectedStats.wins, saves=player.ProjectedStats.saves,
                strikeouts=player.ProjectedStats.strikeoutsPitching, era=player.ProjectedStats.earnedRunAverage,
                whip=player.ProjectedStats.whip)

        else:
            current = [
                {'axis': 'At Bats', 'value': player.CurrentStats.atBats},
                {'axis': 'Hits', 'value': player.CurrentStats.hits},
                {'axis': 'Home Runs', 'value': player.CurrentStats.homeRuns},
                {'axis': 'RBIs', 'value': player.CurrentStats.runsBattedIn},
                # {'axis': 'OPS', 'value': player.CurrentStats.onBasePlusSlug},
                {'axis': 'Strikeouts', 'value': player.CurrentStats.strikeoutsBatting},
                {'axis': 'Walks', 'value': player.CurrentStats.walks}
            ]

            projected = [
                {'axis': 'At Bats', 'value': player.ProjectedStats.atBats},
                {'axis': 'Hits', 'value': player.ProjectedStats.hits},
                {'axis': 'Home Runs', 'value': player.ProjectedStats.homeRuns},
                {'axis': 'RBIs', 'value': player.ProjectedStats.runsBattedIn},
                # {'axis': 'OPS', 'value': player.ProjectedStats.onBasePlusSlug},
                {'axis': 'Strikeouts', 'value': player.ProjectedStats.strikeoutsBatting},
                {'axis': 'Walks', 'value': player.ProjectedStats.walks}
            ]

            maxValues = db.session.query(func.max(ProjectedStats.atBats), 
                func.max(ProjectedStats.hits),
                func.max(ProjectedStats.homeRuns),
                func.max(ProjectedStats.runsBattedIn),
                # func.max(ProjectedStats.onBasePlusSlug),
                func.max(ProjectedStats.strikeoutsBatting),
                func.max(ProjectedStats.walks)).first()

            limits = [1.25 * maxValue for maxValue in maxValues]


            form = BattingForm(request.form, atBats=player.ProjectedStats.atBats,
                hits=player.ProjectedStats.hits, homeRuns=player.ProjectedStats.homeRuns,
                rbis=player.ProjectedStats.runsBattedIn, strikeouts=player.ProjectedStats.strikeoutsBatting,
                walks=player.ProjectedStats.walks)

        stats = [projected, current]


        logger.debug('Player page accessed')
        return render_template('player.html', player=player,
            legend=legend, hometown=hometown, colors=colors,
            stats=stats, limits=limits, form=form)
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

@app.route('/player/newStats/<id>', methods=['GET', 'POST'])
def newStats(id):
    try:
        print(request.form)

        player = db.session.query(Team, Player, CurrentStats, ProjectedStats).\
            join(Player, Team.id == Player.currentTeamId).\
            join(ProjectedStats, Player.id == ProjectedStats.playerId).\
            join(CurrentStats, Player.id == CurrentStats.playerId).\
            filter(Player.id == id).first()

        birthCity = player.Player.birthCity
        birthState = player.Player.birthState
        birthCountry = player.Player.birthCountry

        if len(birthState) > 0:
            hometown = '{}, {}, {}'.format(birthCity, birthState, birthCountry)
        else:
            hometown = '{}, {}'.format(birthCity, birthCountry)

        lastUpdate = db.session.query(LastUpdate).first().lastUpdateDate
        lastUpdateLocal = lastUpdate - UTC_OFFSET_TIMEDELTA
        lastUpdateLocal = lastUpdateLocal.strftime('%b %d')

        legend = ['End of Season Prediction', 'Current as of {}'.format(lastUpdateLocal)]
        colors = [teamColors[player.Team.teamName]['primary'], teamColors[player.Team.teamName]['secondary']]
        
        if player.Player.position == 'P':
            current = [
                {'axis': 'Innings Pitched', 'value': player.CurrentStats.inningsPitched},
                {'axis': 'Wins', 'value': player.CurrentStats.wins},
                {'axis': 'Saves', 'value': player.CurrentStats.saves},
                {'axis': 'Strikeouts', 'value': player.CurrentStats.strikeoutsPitching},
                {'axis': 'ERA', 'value': player.CurrentStats.earnedRunAverage},
                {'axis': 'WHIP', 'value': player.CurrentStats.whip}
            ]

            projected = [
                {'axis': 'Innings Pitched', 'value': request.form.get('inningsPitched')},
                {'axis': 'Wins', 'value': request.form.get('wins')},
                {'axis': 'Saves', 'value': request.form.get('saves')},
                {'axis': 'Strikeouts', 'value': request.form.get('strikeouts')},
                {'axis': 'ERA', 'value': request.form.get('era')},
                {'axis': 'WHIP', 'value': request.form.get('whip')}
            ]

            maxValues = db.session.query(func.max(ProjectedStats.inningsPitched), 
                func.max(ProjectedStats.wins),
                func.max(ProjectedStats.saves),
                func.max(ProjectedStats.strikeoutsPitching),
                func.max(ProjectedStats.earnedRunAverage),
                func.max(ProjectedStats.whip)).first()

            limits = [1.25 * maxValue for maxValue in maxValues]

            form = PitchingForm(request.form, inningsPitched=request.form.get('inningsPitched'),
                wins=request.form.get('wins'), saves=request.form.get('saves'),
                strikeouts=request.form.get('strikeouts'), era=request.form.get('era'),
                whip=request.form.get('whip'))

        else:
            current = [
                {'axis': 'At Bats', 'value': player.CurrentStats.atBats},
                {'axis': 'Hits', 'value': player.CurrentStats.hits},
                {'axis': 'Home Runs', 'value': player.CurrentStats.homeRuns},
                {'axis': 'RBIs', 'value': player.CurrentStats.runsBattedIn},
                # {'axis': 'OPS', 'value': player.CurrentStats.onBasePlusSlug},
                {'axis': 'Strikeouts', 'value': player.CurrentStats.strikeoutsBatting},
                {'axis': 'Walks', 'value': player.CurrentStats.walks}
            ]

            projected = [
                {'axis': 'At Bats', 'value': request.form.get('atBats')},
                {'axis': 'Hits', 'value': request.form.get('hits')},
                {'axis': 'Home Runs', 'value': request.form.get('homeRuns')},
                {'axis': 'RBIs', 'value': request.form.get('rbis')},
                # {'axis': 'OPS', 'value': player.ProjectedStats.onBasePlusSlug},
                {'axis': 'Strikeouts', 'value': request.form.get('strikeouts')},
                {'axis': 'Walks', 'value': request.form.get('walks')}
            ]

            maxValues = db.session.query(func.max(ProjectedStats.atBats), 
                func.max(ProjectedStats.hits),
                func.max(ProjectedStats.homeRuns),
                func.max(ProjectedStats.runsBattedIn),
                # func.max(ProjectedStats.onBasePlusSlug),
                func.max(ProjectedStats.strikeoutsBatting),
                func.max(ProjectedStats.walks)).first()

            limits = [1.25 * maxValue for maxValue in maxValues]


            form = BattingForm(request.form, atBats=request.form.get('atBats'),
                hits=request.form.get('hits'), homeRuns=request.form.get('homeRuns'),
                rbis=request.form.get('rbis'), strikeouts=request.form.get('strikeouts'),
                walks=request.form.get('walks'))

        stats = [projected, current]


        logger.debug('Player page accessed')
        return render_template('player.html', player=player,
            legend=legend, hometown=hometown, colors=colors,
            stats=stats, limits=limits, form=form)
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        logger.warning('Not able to display Updated Statistics page')
        return render_template('error.html')

if __name__ == '__main__':
    app.run(host=app.config['HOST'], port=app.config['PORT'])