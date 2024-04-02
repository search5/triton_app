import pytest
from triton.factory import create_app
from flask_login import FlaskLoginClient


@pytest.fixture()
def app():
    app = create_app("config.yaml")
    app.config.update({
        "TESTING": True,
    })
    app.test_client_class = FlaskLoginClient

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def client_user(app):
    from triton.models import db, Member

    with app.app_context():
        user = db.session.execute(db.select(Member).filter(Member.id == 'admin')).scalar_one()
        return app.test_client(user=user)
