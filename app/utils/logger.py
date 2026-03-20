import logging
import os
from logging.handlers import RotatingFileHandler
from app.core.config import settings

def setup_logging(name: str, log_file: str, level=logging.INFO):
    """Function to setup as many loggers as you want"""
    log_path = os.path.join(settings.NGROK_LOG_DIR, log_file)
    
    handler = RotatingFileHandler(log_path, maxBytes=10*1024*1024, backupCount=5)
    handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

# Main application logger
app_logger = setup_logging('app', 'app.log')
# Tunnel specific logger
tunnel_logger = setup_logging('tunnels', 'tunnels.log')
