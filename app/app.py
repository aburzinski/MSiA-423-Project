import os
import sys
sys.path.append(os.environ.get('PYTHONPATH'))

import logging.config
from config import config
from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import traceback
import json
import pickle
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from models.mlb_database.create_database import Player, Team, CurrentStats, ProjectedStats, LastUpdate
import src.helpers.helpers as h
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

# Import models
with open(os.path.join(config.PROJECT_ROOT_DIR, 'data', 'model_files', 'mvp_lr.model'), 'rb') as f:
    mvp_model_lr = pickle.load(f)
f.close()

with open(os.path.join(config.PROJECT_ROOT_DIR, 'data', 'model_files', 'mvp_rf.model'), 'rb') as f:
    mvp_model_rf = pickle.load(f)
f.close()

with open(os.path.join(config.PROJECT_ROOT_DIR, 'data', 'model_files', 'cyYoung.model'), 'rb') as f:
    cyYoung_model_lr = pickle.load(f)
f.close()

@app.route('/')
def index():
    """Render and return the index template"""
    numPlayersToShow = 10

    try:
        # Get a list of the top players per league per award
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

        # Get a list of teams by division
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

        # Get a list of all players for a search box
        players = db.session.query(Player).join(ProjectedStats).order_by(Player.playerName).all()

        # Calculate the last updated date and the days left in the mlb season
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
    """Render and return the player template"""
    try:
        # Pull player from SQL
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

        # Calculate last update date
        lastUpdate = db.session.query(LastUpdate).first().lastUpdateDate
        lastUpdateLocal = lastUpdate - UTC_OFFSET_TIMEDELTA
        lastUpdateLocal = lastUpdateLocal.strftime('%b %d')

        # Format data to feed to d3 radar chart
        legend = ['End of Season Prediction', 'Current as of {}'.format(lastUpdateLocal)]
        colors = [teamColors[player.Team.teamName]['primary'], teamColors[player.Team.teamName]['secondary']]
        
        if player.Player.position == 'P':
            current = [
                {'axis': 'Innings Pitched', 'value': player.CurrentStats.inningsPitched},
                {'axis': 'Wins', 'value': player.CurrentStats.wins},
                {'axis': 'Saves', 'value': player.CurrentStats.saves},
                {'axis': 'Strikeouts', 'value': player.CurrentStats.strikeoutsPitching},
                {'axis': 'Earned Runs', 'value': player.CurrentStats.earnedRuns},
                {'axis': 'Hits', 'value': player.CurrentStats.hitsAllowed},
                {'axis': 'Walks', 'value': player.CurrentStats.walksAllowed}
            ]

            projected = [
                {'axis': 'Innings Pitched', 'value': player.ProjectedStats.inningsPitched},
                {'axis': 'Wins', 'value': player.ProjectedStats.wins},
                {'axis': 'Saves', 'value': player.ProjectedStats.saves},
                {'axis': 'Strikeouts', 'value': player.ProjectedStats.strikeoutsPitching},
                {'axis': 'Earned Runs', 'value': player.ProjectedStats.earnedRuns},
                {'axis': 'Hits', 'value': player.ProjectedStats.hitsAllowed},
                {'axis': 'Walks', 'value': player.ProjectedStats.walksAllowed}
            ]

            maxValues = db.session.query(func.max(ProjectedStats.inningsPitched), 
                func.max(ProjectedStats.wins),
                func.max(ProjectedStats.saves),
                func.max(ProjectedStats.strikeoutsPitching),
                func.max(ProjectedStats.earnedRuns),
                func.max(ProjectedStats.hitsAllowed),
                func.max(ProjectedStats.walksAllowed)).first()

            limits = [1.25 * maxValue for maxValue in maxValues]

            form = PitchingForm(request.form, inningsPitched=player.ProjectedStats.inningsPitched,
                wins=player.ProjectedStats.wins, saves=player.ProjectedStats.saves,
                strikeouts=player.ProjectedStats.strikeoutsPitching, earnedRuns=player.ProjectedStats.earnedRuns,
                hits=player.ProjectedStats.hitsAllowed, walks=player.ProjectedStats.walksAllowed)

            message = h.appendNumberEnding(player.ProjectedStats.cyYoungRank)
            award = 'Cy Young'

        else:
            current = [
                {'axis': 'At Bats', 'value': player.CurrentStats.atBats},
                {'axis': 'Hits', 'value': player.CurrentStats.hits},
                {'axis': 'Home Runs', 'value': player.CurrentStats.homeRuns},
                {'axis': 'RBIs', 'value': player.CurrentStats.runsBattedIn},
                {'axis': 'Strikeouts', 'value': player.CurrentStats.strikeoutsBatting},
                {'axis': 'Walks', 'value': player.CurrentStats.walks}
            ]

            projected = [
                {'axis': 'At Bats', 'value': player.ProjectedStats.atBats},
                {'axis': 'Hits', 'value': player.ProjectedStats.hits},
                {'axis': 'Home Runs', 'value': player.ProjectedStats.homeRuns},
                {'axis': 'RBIs', 'value': player.ProjectedStats.runsBattedIn},
                {'axis': 'Strikeouts', 'value': player.ProjectedStats.strikeoutsBatting},
                {'axis': 'Walks', 'value': player.ProjectedStats.walks}
            ]

            maxValues = db.session.query(func.max(ProjectedStats.atBats), 
                func.max(ProjectedStats.hits),
                func.max(ProjectedStats.homeRuns),
                func.max(ProjectedStats.runsBattedIn),
                func.max(ProjectedStats.strikeoutsBatting),
                func.max(ProjectedStats.walks)).first()

            limits = [1.25 * maxValue for maxValue in maxValues]


            form = BattingForm(request.form, atBats=player.ProjectedStats.atBats,
                hits=player.ProjectedStats.hits, homeRuns=player.ProjectedStats.homeRuns,
                rbis=player.ProjectedStats.runsBattedIn, strikeouts=player.ProjectedStats.strikeoutsBatting,
                walks=player.ProjectedStats.walks)

            message = h.appendNumberEnding(player.ProjectedStats.mvpRank)
            award = 'Most Valuable Player'

        stats = [projected, current]

        logger.debug('Player page accessed')
        return render_template('player.html', player=player,
            legend=legend, hometown=hometown, colors=colors,
            stats=stats, limits=limits, form=form, message=message,
            award=award)
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        logger.warning('Not able to display Player page')
        return render_template('error.html')

@app.route('/team/<id>')
def team(id):
    """Render and return the team template"""
    numPlayersToShow = 12

    try:
        team = db.session.query(Team).filter(Team.id == id).first()

        division = divisionMapping[team.division]
        location = '{}, {}'.format(team.city, team.state)

        # Rank players on team
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

@app.route('/predict/<id>', methods=['GET', 'POST'])
def predict(id):
    """ Receive a POST request with user input statistics,
        predict a new rank based on those statistics,
        and return the rank as a JSON oject
    """
    try:
        # Get data about current player
        currentPlayer = db.session.query(Team, Player).\
            join(Player, Player.currentTeamId == Team.id).\
            filter(Player.id == id).first()

        # Determine new rank of player
        if currentPlayer.Player.position == 'P':
            
            data = json.loads(request.data)
            for key, value in data.items():
                data[key] = float(value)
            predictData = pd.DataFrame(data, index=[0])
            cols = ['h', 'bb', 'so', 'er', 'sv', 'w', 'ip']
            predictData = predictData[cols]
            
            likelihood = cyYoung_model_lr.predict_proba(predictData)[:,1]

            newRank = db.session.query(Team, Player, ProjectedStats).\
                join(Player, Player.currentTeamId == Team.id).\
                join(ProjectedStats, ProjectedStats.playerId == Player.id).\
                filter(ProjectedStats.playerId != id).\
                filter(Team.league == currentPlayer.Team.league).\
                filter(ProjectedStats.cyYoungLikelihood > likelihood).count() + 1

            message = h.appendNumberEnding(newRank)
            print(predictData)
            print(message)
        
        else:
            
            data = json.loads(request.data)
            for key, value in data.items():
                data[key] = float(value)
            predictData = pd.DataFrame(data, index=[0])
            cols = ['h_x', 'bb_x', 'so_x', 'er', 'sv', 'w', 'ip', 'h_y', 'hr_y', 'rbi', 'bb_y', 'so_y', 'ab_y']
            predictData = predictData[cols]

            avgProbs = np.multiply(mvp_model_lr.predict_proba(predictData)[:,1],
                mvp_model_rf.predict_proba(predictData)[:,1]+.001)

            newRank = db.session.query(Team, Player, ProjectedStats).\
                join(Player, Player.currentTeamId == Team.id).\
                join(ProjectedStats, ProjectedStats.playerId == Player.id).\
                filter(ProjectedStats.playerId != id).\
                filter(Team.league == currentPlayer.Team.league).\
                filter(ProjectedStats.mvpLikelihood > avgProbs).count() + 1

            message = h.appendNumberEnding(newRank)

        # Return json object
        return json.dumps({'message': message})
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        logger.warning('Not able to display Updated Statistics page')
        return json.dumps({'message': 'Error!'})

if __name__ == '__main__':
    app.run(host=app.config['HOST'], port=app.config['PORT'])