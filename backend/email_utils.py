import requests
import logging
from config import settings

logger = logging.getLogger(__name__)

async def send_email(subject: str, email_to: list, body: dict):
    if not settings.N8N_WEBHOOK_URL or not settings.N8N_WEBHOOK_TOKEN:
        logger.warning("N8N_WEBHOOK_URL ou N8N_WEBHOOK_TOKEN não configurados. Email não enviado.")
        return

    message = body.get("message", "")
    link = body.get("link", "")
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
        response = requests.post(
            settings.N8N_WEBHOOK_URL,
            json=payload,
            headers=headers,
            timeout=10,
        )
        response.raise_for_status()
    except Exception as e:
        logger.error(f"Erro ao enviar email via n8n webhook: {e}")
