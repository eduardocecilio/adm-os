import asyncio
import requests
import logging
from html import escape
from config import settings

logger = logging.getLogger(__name__)

async def send_email(subject: str, email_to: list, body: dict):
    if not all((
        settings.N8N_WEBHOOK_URL,
        settings.N8N_WEBHOOK_TOKEN,
        settings.EMAIL_FROM,
    )):
        logger.warning(
            "N8N_WEBHOOK_URL, N8N_WEBHOOK_TOKEN ou EMAIL_FROM não configurados. "
            "Email não enviado."
        )
        return

    message = escape(str(body.get("message", "")))
    link = escape(str(body.get("link", "")), quote=True)
    html = f"""<p>{message}</p><p><a href="{link}">{link}</a></p>"""

    payload = {
        "from": settings.EMAIL_FROM,
        "to": email_to[0] if len(email_to) == 1 else ", ".join(email_to),
        "subject": subject,
        "html": html,
    }

    headers = {
        "Content-Type": "application/json",
        "x-api-key": settings.N8N_WEBHOOK_TOKEN,
    }

    try:
        await asyncio.to_thread(
            lambda: requests.post(
                settings.N8N_WEBHOOK_URL,
                json=payload,
                headers=headers,
                timeout=10,
            ).raise_for_status()
        )
    except Exception as e:
        logger.error(f"Erro ao enviar email via n8n webhook: {e}")
