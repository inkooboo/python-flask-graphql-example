from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker


def make_database_meta(app: Flask):
    '''Create database metadata class and open db session'''
    engine = create_engine('sqlite:///database.sqlite3', convert_unicode=True)
    session = scoped_session(sessionmaker(autocommit=False,
                                          autoflush=False,
                                          bind=engine))

    @app.teardown_appcontext
    def close_db(exception=None):
        session.remove()

    DbMeta = declarative_base()
    DbMeta.session = session
    DbMeta.query = session.query_property()

    return DbMeta
