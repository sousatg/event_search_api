from flask import Flask
from api.extemsions import cors


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    with app.app_context():
        cors.init_app(app, resources={r"*": {"origins": "*"}})

        register_blueprints(app)

    return app


def register_blueprints(app):
    from api.routes import bp

    app.register_blueprint(bp)
