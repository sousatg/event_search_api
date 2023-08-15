from flask import Flask
from src.api.extensions import cors, db, ma, migrate


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    with app.app_context():
        cors.init_app(app, resources={r"*": {"origins": "*"}})
        db.init_app(app)
        migrate.init_app(app, db)
        ma.init_app(app)

        register_blueprints(app)

    return app


def register_blueprints(app):
    from api.routes import bp

    app.register_blueprint(bp)
