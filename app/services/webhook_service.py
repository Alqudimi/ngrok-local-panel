import httpx
import logging
from typing import Optional
from app.core.config import settings

logger = logging.getLogger(__name__)

class WebhookService:
    async def send_discord_notification(self, message: str):
        if not settings.DISCORD_WEBHOOK_URL:
            return
        
        try:
            async with httpx.AsyncClient() as client:
                await client.post(settings.DISCORD_WEBHOOK_URL, json={"content": message})
        except Exception as e:
            logger.error(f"Failed to send Discord notification: {e}")

    async def send_telegram_notification(self, message: str):
        if not settings.TELEGRAM_BOT_TOKEN or not settings.TELEGRAM_CHAT_ID:
            return
        
        url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
        try:
            async with httpx.AsyncClient() as client:
                await client.post(url, json={
                    "chat_id": settings.TELEGRAM_CHAT_ID,
                    "text": message
                })
        except Exception as e:
            logger.error(f"Failed to send Telegram notification: {e}")

    async def notify_tunnel_event(self, event_type: str, tunnel_name: str, details: str = ""):
        message = f"🚀 **Ngrok Event**: {event_type}\nTunnel: {tunnel_name}\n{details}"
        await self.send_discord_notification(message)
        await self.send_telegram_notification(message)

webhook_service = WebhookService()
