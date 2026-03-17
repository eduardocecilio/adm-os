import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Database
    SQLALCHEMY_DATABASE_URL: str = os.getenv("DATABASE_URL", "")

    # JWT Security — obrigatórios em produção
    SECRET_KEY: str = os.getenv("SECRET_KEY", "")
    RESET_SECRET_KEY: str = os.getenv("RESET_SECRET_KEY", "")

    # Financial Constants
    ALIQ_EMOLUMENTOS: float = 0.000345
    ALIQ_IR_SWING_TRADE: float = 0.15

    # Email config (n8n webhook)
    N8N_WEBHOOK_URL: str = os.getenv("N8N_WEBHOOK_URL", "")
    N8N_WEBHOOK_TOKEN: str = os.getenv("N8N_WEBHOOK_TOKEN", "")
    EMAIL_FROM: str = os.getenv("EMAIL_FROM", "")

    # Frontend settings
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:8082")

settings = Settings()

if not settings.SECRET_KEY:
    raise RuntimeError(
        "SECRET_KEY não definida. "
        "Gere um valor seguro: python -c \"import secrets; print(secrets.token_hex(32))\" "
        "e defina no arquivo .env"
    )

if not settings.RESET_SECRET_KEY:
    raise RuntimeError(
        "RESET_SECRET_KEY não definida. "
        "Gere um valor seguro: python -c \"import secrets; print(secrets.token_hex(32))\" "
        "e defina no arquivo .env"
    )

if not settings.SQLALCHEMY_DATABASE_URL:
    raise RuntimeError("DATABASE_URL não definida. Defina no arquivo .env")
