import pytest
from fastapi.testclient import TestClient

def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome to Ngrok Local Control Panel API" in response.json()["message"]

def test_get_status(client):
    response = client.get("/api/v1/status")
    assert response.status_code == 200
    data = response.json()
    assert "ngrok_version" in data
    assert "is_running" in data

def test_update_authtoken(client):
    response = client.post("/api/v1/authtoken", json={"token": "new_test_token"})
    assert response.status_code == 200
    assert response.json()["message"] == "Auth token updated"

def test_create_and_list_tunnel(client):
    tunnel_data = {
        "name": "api_test_tunnel",
        "proto": "http",
        "addr": "8000",
        "extra_config": {"domain": "test.ngrok.io"}
    }
    # Create
    response = client.post("/api/v1/tunnels", json=tunnel_data)
    assert response.status_code == 200
    
    # List
    response = client.get("/api/v1/tunnels")
    assert response.status_code == 200
    assert "api_test_tunnel" in response.json()

def test_delete_tunnel(client):
    # Ensure it exists
    client.post("/api/v1/tunnels", json={"name": "del_me", "proto": "http", "addr": "80"})
    
    # Delete
    response = client.delete("/api/v1/tunnels/del_me")
    assert response.status_code == 200
    
    # Verify deleted
    response = client.get("/api/v1/tunnels")
    assert "del_me" not in response.json()

def test_delete_nonexistent_tunnel(client):
    response = client.delete("/api/v1/tunnels/nonexistent_xyz")
    assert response.status_code == 404
