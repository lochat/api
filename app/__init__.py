from flask import Flask
from flask.ext.mongoengine import MongoEngine
from flask.ext.mail import Mail
from config import config

db = MongoEngine()
mail = Mail()


def create_app(config_name):
    """TODO: Settings config and app
    :returns: app object

    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    mail.init_app(app)

    from .api_1_0 import api as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')

    return app
