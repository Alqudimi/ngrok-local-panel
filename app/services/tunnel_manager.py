import yaml
import os
import json
from typing import List, Dict, Any, Optional
from app.core.config import settings
from app.services.process_manager import process_manager

class TunnelManager:
    def __init__(self):
        self.config_file = os.path.join(settings.NGROK_DATA_DIR, "ngrok_config.yml")
        self._ensure_config_exists()

    def _ensure_config_exists(self):
        if not os.path.exists(settings.NGROK_DATA_DIR):
            os.makedirs(settings.NGROK_DATA_DIR)
        if not os.path.exists(self.config_file):
            initial_config = {
                "version": "2",
                "authtoken": "",
                "tunnels": {}
            }
            self._save_config(initial_config)

    def _load_config(self) -> Dict[str, Any]:
        with open(self.config_file, 'r') as f:
            return yaml.safe_load(f) or {}

    def _save_config(self, config: Dict[str, Any]):
        with open(self.config_file, 'w') as f:
            yaml.dump(config, f, default_flow_style=False)

    def set_authtoken(self, token: str):
        config = self._load_config()
        config["authtoken"] = token
        self._save_config(config)

    def add_tunnel(self, name: str, proto: str, addr: str, **kwargs):
        config = self._load_config()
        if "tunnels" not in config:
            config["tunnels"] = {}
        
        tunnel_config = {
            "proto": proto,
            "addr": addr
        }
        tunnel_config.update(kwargs)
        config["tunnels"][name] = tunnel_config
        self._save_config(config)

    def remove_tunnel(self, name: str):
        config = self._load_config()
        if "tunnels" in config and name in config["tunnels"]:
            del config["tunnels"][name]
            self._save_config(config)
            return True
        return False

    def list_tunnels(self) -> Dict[str, Any]:
        config = self._load_config()
        return config.get("tunnels", {})

    async def get_active_tunnels_info(self) -> List[Dict[str, Any]]:
        """Fetch active tunnels info from ngrok local API"""
        import httpx
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get("http://127.0.0.1:4040/api/tunnels")
                if response.status_code == 200:
                    return response.json().get("tunnels", [])
        except Exception:
            pass
        return []

tunnel_manager = TunnelManager()
