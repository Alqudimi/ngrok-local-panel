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

from unittest.mock import patch

def test_start_ngrok_failure(client):
    with patch("app.services.process_manager.process_manager.start_ngrok", return_value=False):
        response = client.post("/api/v1/start")
        assert response.status_code == 500
        assert response.json()["detail"] == "Failed to start ngrok"

def test_stop_ngrok_success(client):
    with patch("app.services.process_manager.process_manager.stop_ngrok", return_value=True):
        response = client.post("/api/v1/stop")
        assert response.status_code == 200
        assert response.json()["success"] is True

def test_get_active_tunnels(client):
    with patch("app.services.tunnel_manager.tunnel_manager.get_active_tunnels_info", return_value=[]):
        response = client.get("/api/v1/active-tunnels")
        assert response.status_code == 200
        assert response.json() == []

