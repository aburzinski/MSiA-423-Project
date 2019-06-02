import os
import sys
sys.path.append(os.environ.get('PYTHONPATH'))

import logging.config
from config import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

parentDir = config.PROJECT_ROOT_DIR
logging.config.fileConfig(config.LOGGING_CONFIG_FILE, disable_existing_loggers=False)
logger = logging.getLogger(__name__)

from models.mlb_database.create_database import Base, LastUpdate

def ingestLastUpdate(session, truncate=True):
    
    if truncate:
        session.query(LastUpdate).delete()

        
    update = LastUpdate(lastUpdateDate=datetime.now())
    session.add(update)
    session.commit()
    logging.info('Added current time to database successfully')
