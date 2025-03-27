#flask imports
from flask import g, current_app
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = None
Session = None

def init_app(app):
    global engine, Session

    engine = create_engine(
            app.config['DATABASE_URI'],
            pool_size=app.config.get('SQLALCHEMY_POOL_SIZE', 5),
            pool_timeout=app.config.get('SQLALCHEMY_POOL_TIMEOUT', 30)
    )

    Session = scoped_session(sessionmaker(bind=engine))

    #executed before every request
    @app.before_request
    def before_request():
        g.db_session = Session()

    #runs after each request
    @app.teardown_request
    def teardown_request(exception=None):
        if hasattr(g, 'db_session'):
            g.db_session.close()


#connection managed by orm
def get_session():
    if not hasattr(g, 'db_session'):
        g.db_session = Session()
    return g.db_session

#Connection to use psycopg2
def get_raw_connection():
    session = get_session()
    return session.connection().connection
