from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import orm
from views import service_blueprint


def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)
    orm.init_app(app)
    app.register_blueprint(service_blueprint, url_prefix='/service')
    migrate = Migrate(app, orm)
    return app


app = create_app('config')
