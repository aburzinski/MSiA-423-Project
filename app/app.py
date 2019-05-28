import os
import sys
sys.path.append(os.environ.get('PYTHONPATH'))

import logging.config
from config import config
from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy

from models.mlb_database.create_database import Player

logging.config.fileConfig(config.LOGGING_CONFIG_FILE, disable_existing_loggers=False)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_pyfile(os.path.join(config.PROJECT_ROOT_DIR, 'config', 'config.py'))

db = SQLAlchemy(app)

@app.route('/')
def index():
    try:
        players = db.session.query(Player).limit(app.config['MAX_ROWS_SHOW']).all()
        logger.debug('Index page accessed')
        return render_template('index.html', players=players)
    except:
        logger.warning('Not able to display index')
        return render_template('error.html')

@app.route('/player')
def player():
    try:
        logger.debug('Player page accessed')
        return render_template('player.html')   
    except:
        logger.warning('Not able to display Player page')
        return render_template('error.html')

if __name__ == '__main__':
    app.run(host=app.config['HOST'])