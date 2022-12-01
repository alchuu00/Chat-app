import os
import pytest

os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from main import app, db


@pytest.fixture
def client():
    client = app.test_client()

    cleanup()  # clean up before every test

    db.create_all()

    yield client


def cleanup():
    # clean up/delete the DB (drop all tables in the database)
    db.drop_all()


# all test functions must start with test keyword
def test_index_not_logged_in(client):
    response = client.get("/")
    assert b"Enter your name" in response.data


def test_index_logged_in(client):
    # post request test
    client.post('/login',
                data={"user-name": "Test User", "user-email": "test@user.com"},
                follow_redirects=True)

    response = client.get('/')
    assert b"Enter your message" in response.data


def test_index_add_message(client):
    test_user = "Test User"
    client.post("/login",
                data={"user-name": test_user, "user-email": "testuser@test.com"},
                follow_redirects=True)

    test_message = b"This is a test message"
    response = client.post('/add-message',
                           data={"text": test_message},
                           follow_redirects=True)

    assert test_message in response.data
