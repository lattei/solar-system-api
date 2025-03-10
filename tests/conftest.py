import pytest
from app import create_app
from app import db
from flask.signals import request_finished
from app.models.planet import Planet


@pytest.fixture
def app():
    app = create_app({"TESTING": True})

    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()

    with app.app_context():
        db.create_all()
        yield app

    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def two_saved_planets(app):
    
    venus_planet = Planet(id=1,name="Venus",description="hot enough to melt lead n ur heart </3", color="she lil' rusty :(")
    saturn_planet = Planet(id=2,name="Saturn",description="bling bling rings",
color="she cute pink :(")

    db.session.add(venus_planet)
    db.session.add(saturn_planet)
    db.session.commit()
