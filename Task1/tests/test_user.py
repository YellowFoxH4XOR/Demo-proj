from starlette.testclient import TestClient
import sys
import os
sys.path.append(os.getcwd())

from main import app

client = TestClient(app)


def test_wrong_auth_details():
    response = client.get("/user/logged-user-details", headers={"Authorization": "wrong token"})
    assert response.status_code == 401

def test_correct_auth_details():
    response = client.post("/user/add-user", json={"email": "test", "password": "test"})
    token = client.post('/token/', data={"username": "test", "password": "test"})
    token = token.json()
    response = client.get("/user/logged-user-details", headers={"Authorization": "Bearer " + token.get('access_token')})
    assert response.status_code == 200