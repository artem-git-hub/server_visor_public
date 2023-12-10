import logging

import sqlite3
from sqlalchemy import create_engine, Column, DateTime, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from config import config


logger = logging.getLogger(__name__)

# Create a base class for declarative models
Base = declarative_base()

class TimedModel(Base):
    __abstract__ = True

    created_at = Column(DateTime(True), server_default=func.now())
    updated_at = Column(
        DateTime(True),
        default=func.now(),
        onupdate=func.now(),
        server_default=func.now(),
    )


def request(func):
    def good_interaction(*args, **kwargs):
        try:
            # Начало явной транзакции
            config.db.session.begin()

            # Операции с базой данных
            result = func(session=config.db.session, *args, **kwargs)

            # Закрыть сессию
            config.db.session.close()


            return result

        except Exception as e:
            # Откат транзакции в случае ошибки
            config.db.session.rollback()
            logger.error(f"Transaction error: {e}")
            raise
    return good_interaction



def on_startapp():
    try:
        # Create an SQLite database (you can replace this with a file path)
        engine = create_engine('sqlite:///services/db/database.sqlite', echo=True)

        #Create class Session
        Session = sessionmaker(bind=engine)

        #Write Session to config
        config.db.session = Session()

        logger.info("Successful connection to SQLite")
    except sqlite3.OperationalError as e:
        logger.error("Failed to establish connection with SQLite.")
        logger.error(str(e))
        exit(1)



    #drop and create all tables
    if config.db.debug:
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)



def on_shutdown():
    # Close the session
    config.db.session.close()