import os

basedir = os.path.abspath(os.path.dirname(__file__))


class ApiConfig:
    DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'my-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('API_SQLALCHEMY_DATABASE_URI') \
        or 'postgresql+psycopg2://dev:dev@localhost:5432/events'
