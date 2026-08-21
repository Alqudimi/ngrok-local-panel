import pytest
from fastapi.testclient import TestClient
from app.core.config import settings

def test_api_key_required(client):
    # Temporarily set an API key
    settings.API_KEY = "test-secret-key"
    
    response = client.get("/api/v1/status")
    assert response.status_code == 403
    assert response.json()["detail"] == "Could not validate API Key"
    
    # Reset API key
    settings.API_KEY = None

def test_api_key_success(client):
    # Temporarily set an API key
    settings.API_KEY = "test-secret-key"
    
    response = client.get(
        "/api/v1/status",
        headers={"X-API-Key": "test-secret-key"}
    )
    assert response.status_code == 200
    
    # Reset API key
    settings.API_KEY = None

def test_api_key_not_required(client):
    # Ensure no API key is set
    settings.API_KEY = None
    
    response = client.get("/api/v1/status")
    assert response.status_code == 200

from app.core.security import create_access_token, verify_password, get_password_hash
from datetime import timedelta

def test_password_hashing():
    password = "abc"
    hashed = get_password_hash(password)
    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("wrongpassword", hashed) is False

def test_create_access_token():
    token = create_access_token(subject="testuser")
    assert isinstance(token, str)
    
    token_with_delta = create_access_token(subject="testuser", expires_delta=timedelta(minutes=10))
    assert isinstance(token_with_delta, str)

