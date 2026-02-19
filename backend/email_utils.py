# from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr
# import os
# from config import settings

# MOCK EMAIL FUNCTION TO RESTORE SERVER STABILITY
async def send_email(subject: str, email_to: list[EmailStr], body: dict):
    # Log para debug
    print(f"---- [MOCK EMAIL] ----")
    print(f"To: {email_to}")
    print(f"Subject: {subject}")
    print(f"Body: {body}")
    print(f"----------------------")
    return True
