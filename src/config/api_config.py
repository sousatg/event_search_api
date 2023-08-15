import os

basedir = os.path.abspath(os.path.dirname(__file__))


class ApiConfig:
    DEBUG = os.environ.get("DEBUG", "False").lower() == "true"
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://dev:dev@localhost:5432/events"
