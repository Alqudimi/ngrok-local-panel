from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List

class TunnelCreate(BaseModel):
    name: str = Field(..., json_schema_extra={"example": "web-app"})
    proto: str = Field(default="http", json_schema_extra={"example": "http"})
    addr: str = Field(..., json_schema_extra={"example": "8000"})
    extra_config: Optional[Dict[str, Any]] = Field(default_factory=dict)

class TunnelResponse(BaseModel):
    name: str
    proto: str
    addr: str
    public_url: Optional[str] = None

class AuthTokenUpdate(BaseModel):
    token: str

class SystemStatus(BaseModel):
    ngrok_version: str
    is_running: bool
    process_info: Dict[str, Any]
    active_tunnels_count: int
