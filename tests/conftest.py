import pytest
from triton.factory import create_app


@pytest.fixture()
def app():
    app = create_app("config.yaml")
    app.config.update({
        "TESTING": True,
    })

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()