import pytest
from fastapi.testclient import TestClient
from main import app
import os
import shutil
from app.core.config import settings

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    # Use a temporary data directory for tests
    original_data_dir = settings.NGROK_DATA_DIR
    settings.NGROK_DATA_DIR = "test_data"
    os.makedirs(settings.NGROK_DATA_DIR, exist_ok=True)
    
    yield
    
    # Cleanup after tests
    if os.path.exists(settings.NGROK_DATA_DIR):
        shutil.rmtree(settings.NGROK_DATA_DIR)
    settings.NGROK_DATA_DIR = original_data_dir

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c
