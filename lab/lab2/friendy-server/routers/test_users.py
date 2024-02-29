import mariadb
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

# Test flow:
# Create user -> Get user -> Update user status -> Delete user

def test_create_user():
    response = client.post("/api/v1/user",
                           headers={"X-Token": "testonly"},
                           json={"username": "Arial", "password": "Arial"}
                            )
    assert response.status_code == 200
    assert response.json() == {
        "id": 2,
        "name": "Arial",
        "password": "Arial",
        "level": 0,
        "room": 0
    }

def test_create_user_nopasswd():
    response = client.post("/api/v1/user",
                           headers={"X-Token": "testonly"},
                           json={"username": "Arial", "password": ""}
                            )
    assert response.status_code == 400

def test_get_user():
    response = client.get("/api/v1/user/2",
                          headers={"X-Token": "testonly"}
                          )
    assert response.status_code == 200
    assert response.json() == {
        "id": 2,
        "name": "Arial",
        "password": "*",
        "level": 0,
        "room": 0
    }

def test_get_nonexist_user():
    try:
        response = client.get("/api/v1/user/3",
                          headers={"X-Token": "testonly"}
                          )
    except KeyError:
        assert True
        
def test_update_user_status():
    response = client.put("/api/v1/user/2",
                          headers={"X-Token": "testonly"},
                          json={"level": 0, "room": 1, "roomAdmin": 1}
                          )
    assert response.status_code == 200
    
def test_update_nonexist_user_status():
    response = client.put("/api/v1/user/3",
                          headers={"X-Token": "testonly"},
                          json={"level": 0, "room": 1, "roomAdmin": 1}
                          )
    assert response.status_code == 400