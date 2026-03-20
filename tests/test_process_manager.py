import pytest
from unittest.mock import MagicMock, patch
from app.services.process_manager import ProcessManager
import subprocess

@pytest.fixture
def proc_mgr():
    return ProcessManager()

def test_is_running_no_process(proc_mgr):
    with patch('psutil.process_iter', return_value=[]):
        assert proc_mgr.is_running() is False

def test_check_version(proc_mgr):
    with patch('subprocess.run') as mock_run:
        mock_run.return_value = MagicMock(stdout="ngrok version 3.0.0")
        version = proc_mgr.check_version()
        assert "3.0.0" in version

@pytest.mark.asyncio
async def test_start_ngrok(proc_mgr):
    with patch('subprocess.Popen') as mock_popen:
        mock_popen.return_value = MagicMock(pid=1234)
        with patch.object(proc_mgr, 'is_running', return_value=False):
            success = await proc_mgr.start_ngrok("fake_config.yml")
            assert success is True
            assert proc_mgr.process is not None
            mock_popen.assert_called_once()

def test_stop_ngrok(proc_mgr):
    mock_proc = MagicMock()
    mock_proc.info = {'name': 'ngrok', 'pid': 1234}
    
    with patch('psutil.process_iter', return_value=[mock_proc]):
        with patch('os.kill') as mock_kill:
            success = proc_mgr.stop_ngrok()
            assert success is True
            mock_kill.assert_called_with(1234, 15) # SIGTERM is 15
