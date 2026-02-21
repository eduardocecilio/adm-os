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

    # Email config
    SMTP_USER = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
    SMTP_HOST = os.getenv("SMTP_HOST", "")
    SMTP_PORT = int(os.getenv("SMTP_PORT", 465))
    MAIL_FROM = os.getenv("MAIL_FROM", "suporte@ceciliolab.com")
    
    # Frontend settings
    FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:8082")

settings = Settings()
