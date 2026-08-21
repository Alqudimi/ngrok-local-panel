from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from typing import List, Dict, Any
from app.schemas.tunnel import TunnelCreate, TunnelResponse, AuthTokenUpdate, SystemStatus
from app.services.tunnel_manager import tunnel_manager
from app.services.process_manager import process_manager
from app.core.config import settings
from app.core.security import get_api_key

router = APIRouter(dependencies=[Depends(get_api_key)])

@router.get("/status", response_model=SystemStatus)
async def get_status():
    active_tunnels = await tunnel_manager.get_active_tunnels_info()
    return {
        "ngrok_version": process_manager.check_version(),
        "is_running": process_manager.is_running(),
        "process_info": process_manager.get_status(),
        "active_tunnels_count": len(active_tunnels)
    }

@router.post("/start")
async def start_ngrok():
    success = await process_manager.start_ngrok(tunnel_manager.config_file)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to start ngrok")
    return {"message": "ngrok started successfully"}

@router.post("/stop")
async def stop_ngrok():
    success = process_manager.stop_ngrok()
    return {"message": "ngrok stopped", "success": success}

@router.post("/authtoken")
async def update_authtoken(data: AuthTokenUpdate):
    tunnel_manager.set_authtoken(data.token)
    return {"message": "Auth token updated"}

@router.get("/tunnels")
async def list_tunnels():
    return tunnel_manager.list_tunnels()

@router.post("/tunnels")
async def create_tunnel(tunnel: TunnelCreate):
    tunnel_manager.add_tunnel(
        name=tunnel.name,
        proto=tunnel.proto,
        addr=tunnel.addr,
        **tunnel.extra_config
    )
    return {"message": f"Tunnel {tunnel.name} created/updated"}

@router.delete("/tunnels/{name}")
async def delete_tunnel(name: str):
    success = tunnel_manager.remove_tunnel(name)
    if not success:
        raise HTTPException(status_code=404, detail="Tunnel not found")
    return {"message": f"Tunnel {name} deleted"}

@router.get("/active-tunnels")
async def get_active_tunnels():
    return await tunnel_manager.get_active_tunnels_info()
