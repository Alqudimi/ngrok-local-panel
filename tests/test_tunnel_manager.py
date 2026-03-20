import pytest
import os
import yaml
from app.services.tunnel_manager import TunnelManager
from app.core.config import settings

@pytest.fixture
def tunnel_mgr():
    # Ensure we use the test data directory
    mgr = TunnelManager()
    return mgr

def test_ensure_config_exists(tunnel_mgr):
    assert os.path.exists(tunnel_mgr.config_file)
    with open(tunnel_mgr.config_file, 'r') as f:
        config = yaml.safe_load(f)
        assert config["version"] == "2"
        assert "tunnels" in config

def test_set_authtoken(tunnel_mgr):
    token = "test_token_123"
    tunnel_mgr.set_authtoken(token)
    with open(tunnel_mgr.config_file, 'r') as f:
        config = yaml.safe_load(f)
        assert config["authtoken"] == token

def test_add_tunnel(tunnel_mgr):
    name = "test_tunnel"
    proto = "http"
    addr = "8080"
    tunnel_mgr.add_tunnel(name, proto, addr, domain="example.com")
    
    tunnels = tunnel_mgr.list_tunnels()
    assert name in tunnels
    assert tunnels[name]["proto"] == proto
    assert tunnels[name]["addr"] == addr
    assert tunnels[name]["domain"] == "example.com"

def test_remove_tunnel(tunnel_mgr):
    name = "to_be_deleted"
    tunnel_mgr.add_tunnel(name, "http", "9000")
    assert name in tunnel_mgr.list_tunnels()
    
    success = tunnel_mgr.remove_tunnel(name)
    assert success is True
    assert name not in tunnel_mgr.list_tunnels()

def test_remove_nonexistent_tunnel(tunnel_mgr):
    success = tunnel_mgr.remove_tunnel("nonexistent")
    assert success is False
