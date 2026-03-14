import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Database
    # Using a default for development if not set, but allowing override
    SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./adm_os.db")

    # Security
    API_TOKEN = os.getenv("API_TOKEN", "")
    
    # Financial Constants
    ALIQ_EMOLUMENTOS = 0.000345
    ALIQ_IR_SWING_TRADE = 0.15

    # Email config (n8n webhook)
    N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL", "")
    N8N_WEBHOOK_TOKEN = os.getenv("N8N_WEBHOOK_TOKEN", "")
    EMAIL_FROM = os.getenv("EMAIL_FROM", "Adm OS <nao-responda@ceciliolab.com>")
    
    # Frontend settings
    FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:8082")

settings = Settings()
