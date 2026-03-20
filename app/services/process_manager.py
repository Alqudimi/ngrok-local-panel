import subprocess
import psutil
import os
import signal
import time
import logging
import asyncio
from typing import Optional, Dict, Any
from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProcessManager:
    def __init__(self):
        self.process: Optional[subprocess.Popen] = None
        self.process_name = "ngrok"

    def is_running(self) -> bool:
        if self.process and self.process.poll() is None:
            return True
        
        # Check if any ngrok process is running on the system
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] == self.process_name:
                return True
        return False

    def get_status(self) -> Dict[str, Any]:
        running = self.is_running()
        status = {
            "running": running,
            "pid": None,
            "cpu_percent": 0.0,
            "memory_info": {},
            "uptime": 0
        }
        
        if running:
            for proc in psutil.process_iter(['pid', 'name', 'create_time', 'cpu_percent', 'memory_info']):
                if proc.info['name'] == self.process_name:
                    status["pid"] = proc.info['pid']
                    status["cpu_percent"] = proc.info['cpu_percent']
                    status["memory_info"] = proc.info['memory_info']._asdict()
                    status["uptime"] = time.time() - proc.info['create_time']
                    break
        return status

    async def start_ngrok(self, config_path: str) -> bool:
        if self.is_running():
            logger.info("ngrok is already running")
            return True

        try:
            cmd = [settings.NGROK_PATH, "start", "--all", "--config", config_path]
            # Start ngrok in background
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                preexec_fn=os.setsid
            )
            logger.info(f"Started ngrok with PID: {self.process.pid}")
            return True
        except Exception as e:
            logger.error(f"Failed to start ngrok: {e}")
            return False

    def stop_ngrok(self) -> bool:
        stopped = False
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == self.process_name:
                try:
                    os.kill(proc.info['pid'], signal.SIGTERM)
                    stopped = True
                except Exception as e:
                    logger.error(f"Error killing process {proc.info['pid']}: {e}")
        
        if self.process:
            self.process = None
        return stopped

    def restart_ngrok(self, config_path: str) -> bool:
        self.stop_ngrok()
        time.sleep(1)
        return asyncio.run(self.start_ngrok(config_path))

    def check_version(self) -> str:
        try:
            result = subprocess.run([settings.NGROK_PATH, "version"], capture_output=True, text=True)
            return result.stdout.strip()
        except Exception:
            return "Not Installed"

process_manager = ProcessManager()
