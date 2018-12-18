import pytest
from app import create_app
from models import orm
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from views import service_blueprint


@pytest.fixture
def application():
    # Beggining of Setup code
    app = create_app('test_config')
    with app.app_context():   
        orm.create_all()
        # End of Setup code
        # The test will start running here
        yield app
        # The test finished running here
        # Beginning of Teardown code
        orm.session.remove()
        orm.drop_all()
        # End of Teardown code


@pytest.fixture
def client(application):
    return application.test_client()
