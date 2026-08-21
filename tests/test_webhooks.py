import pytest
from unittest.mock import patch, AsyncMock
from app.services.webhook_service import webhook_service
from app.core.config import settings

@pytest.mark.asyncio
async def test_send_discord_notification():
    settings.DISCORD_WEBHOOK_URL = "http://fake-discord.com"
    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        await webhook_service.send_discord_notification("test message")
        mock_post.assert_called_once()
    settings.DISCORD_WEBHOOK_URL = None

@pytest.mark.asyncio
async def test_send_telegram_notification():
    settings.TELEGRAM_BOT_TOKEN = "fake_token"
    settings.TELEGRAM_CHAT_ID = "fake_id"
    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        await webhook_service.send_telegram_notification("test message")
        mock_post.assert_called_once()
    settings.TELEGRAM_BOT_TOKEN = None
    settings.TELEGRAM_CHAT_ID = None

@pytest.mark.asyncio
async def test_notify_tunnel_event():
    with patch.object(webhook_service, "send_discord_notification", new_callable=AsyncMock) as mock_discord:
        with patch.object(webhook_service, "send_telegram_notification", new_callable=AsyncMock) as mock_telegram:
            await webhook_service.notify_tunnel_event("TEST", "tunnel1", "details")
            mock_discord.assert_called_once()
            mock_telegram.assert_called_once()
            assert "TEST" in mock_discord.call_args[0][0]
            assert "tunnel1" in mock_discord.call_args[0][0]
