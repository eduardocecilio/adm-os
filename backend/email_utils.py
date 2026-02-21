import smtplib
from email.message import EmailMessage
from pydantic import EmailStr
from config import settings
import asyncio

async def send_email(subject: str, email_to: list[EmailStr], body: dict):
    # Run synchronous SMTP in an executor to avoid blocking the event loop
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, _send_email_sync, subject, email_to, body)
    return True

def _send_email_sync(subject: str, email_to: list[EmailStr], body: dict):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = f"Adm OS <{settings.MAIL_FROM}>"
    msg['To'] = ", ".join(email_to)
    
    content = body.get("message", "") + "\n\n" + body.get("link", "")
    msg.set_content(content)
    
    try:
        # SMTP_SSL is appropriate for port 465 (SMTPS)
        with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(msg)
    except Exception as e:
        print(f"Error sending email via smtplib: {e}")
