"""
ProdSynth Agents — WebhookNotifier (Phase 3)
Sends notifications to Slack, Telegram, or custom URLs.
Triggered when product synthesis is complete.
"""

import os
import logging
from typing import Dict, List, Any, Optional
from pydantic import BaseModel

logger = logging.getLogger("prodsynth.agents.webhook")


class WebhookEvent(BaseModel):
    """Webhook event model."""
    event: str  # product.ready, product.failed
    project_id: str
    url: Optional[str] = None
    status: str  # completed, failed, deployed
    message: Optional[str] = None


class WebhookConfig(BaseModel):
    """Webhook configuration."""
    url: str  # https://hooks.slack.com/...
    events: List[str] = ["product.ready", "product.failed"]
    active: bool = True


class WebhookNotifier:
    """
    Agent for sending webhook notifications.
    Supports Slack, Telegram, custom URLs.
    """

    def __init__(self, graph_adapter=None):
        self.graph_adapter = graph_adapter
        self.webhooks: List[WebhookConfig] = self._load_webhooks()
        logger.info("🔔 WebhookNotifier initialized")

    def _load_webhooks(self) -> List[WebhookConfig]:
        """Load webhook configurations from env or DB."""
        # Placeholder: In real implementation, load from DB
        webhooks = []

        slack_url = os.getenv("SLACK_WEBHOOK_URL")
        if slack_url:
            webhooks.append(WebhookConfig(
                url=slack_url,
                events=["product.ready", "product.failed"]
            ))

        telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
        if telegram_token:
            webhooks.append(WebhookConfig(
                url=f"https://api.telegram.org/bot{telegram_token}/sendMessage",
                events=["product.ready"]
            ))

        logger.info(f"   Loaded {len(webhooks)} webhooks")
        return webhooks

    async def send_notification(self, event: WebhookEvent) -> Dict[str, Any]:
        """
        Send webhook notification.
        Phase 3: Basic implementation.
        """
        logger.info(f"🔔 Sending webhook notification: {event.event}")
        logger.info(f"   Project: {event.project_id}")

        results = {
            "event": event.event,
            "project_id": event.project_id,
            "sent": 0,
            "failed": 0,
            "details": [],
        }

        for webhook in self.webhooks:
            if event.event not in webhook.events:
                continue

            try:
                # Placeholder: In real implementation, use httpx
                # import httpx
                # payload = self._build_payload(event, webhook)
                # response = await httpx.post(webhook.url, json=payload)
                # if response.status_code == 200:
                #     results["sent"] += 1
                # else:
                #     results["failed"] += 1

                # Simulated success
                logger.info(f"   ✅ Sent to {webhook.url[:30]}...")
                results["sent"] += 1
                results["details"].append({
                    "url": webhook.url,
                    "status": "sent",
                    "simulated": True,
                })

            except Exception as e:
                logger.error(f"   ❌ Failed to send to {webhook.url}: {e}")
                results["failed"] += 1
                results["details"].append({
                    "url": webhook.url,
                    "status": "failed",
                    "error": str(e),
                })

        logger.info(f"✅ Notification complete: {results['sent']} sent, {results['failed']} failed")
        return results

    def _build_payload(self, event: WebhookEvent, webhook: WebhookConfig) -> Dict[str, Any]:
        """Build webhook payload based on target."""
        base_payload = {
            "event": event.event,
            "project_id": event.project_id,
            "timestamp": "2026-04-26T12:00:00Z",
        }

        if event.url:
            base_payload["url"] = event.url
        if event.message:
            base_payload["message"] = event.message

        # Slack-specific formatting
        if "slack.com" in webhook.url:
            return {
                "text": f"🎉 Product {event.project_id} is ready!",
                "attachments": [
                    {
                        "color": "#36a64a" if event.status == "deployed" else "#ff0000",
                        "fields": [
                            {"title": "Project", "value": event.project_id, "short": True},
                            {"title": "Status", "value": event.status, "short": True},
                            {"title": "URL", "value": event.url or "N/A", "short": False},
                        ],
                    }
                ],
            }

        # Telegram-specific formatting
        if "telegram.org" in webhook.url:
            text = f"🎉 *ProdSynth Notification*\n\n"
            text += f"Project: `{event.project_id}`\n"
            text += f"Status: *{event.status}*\n"
            if event.url:
                text += f"URL: {event.url}\n"
            return {"text": text, "parse_mode": "Markdown"}

        return base_payload

    async def register_webhook(self, url: str, events: List[str]) -> bool:
        """Register a new webhook."""
        logger.info(f"🔔 Registering webhook: {url}")

        # Placeholder: In real implementation, save to DB
        new_webhook = WebhookConfig(url=url, events=events)
        self.webhooks.append(new_webhook)

        logger.info(f"✅ Webhook registered")
        return True

    async def unregister_webhook(self, url: str) -> bool:
        """Remove a webhook."""
        logger.info(f"🔔 Unregistering webhook: {url}")

        initial_count = len(self.webhooks)
        self.webhooks = [w for w in self.webhooks if w.url != url]

        if len(self.webhooks) < initial_count:
            logger.info(f"✅ Webhook removed")
            return True
        else:
            logger.warning(f"⚠️ Webhook not found")
            return False


# Singleton instance
_webhook_notifier: Optional[WebhookNotifier] = None


def get_webhook_notifier(graph_adapter=None) -> WebhookNotifier:
    """Get or create WebhookNotifier singleton."""
    global _webhook_notifier
    if _webhook_notifier is None:
        _webhook_notifier = WebhookNotifier(graph_adapter=graph_adapter)
    return _webhook_notifier
