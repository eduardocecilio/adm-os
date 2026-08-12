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

def _validate_secret(name: str, value: str) -> None:
    normalized = value.strip().lower()
    placeholder_markers = (
        "change-me",
        "changeme",
        "placeholder",
        "replace-me",
        "seu-token",
        "troque-",
    )

    if len(value) < 32 or any(marker in normalized for marker in placeholder_markers):
        raise RuntimeError(
            f"{name} ausente ou insegura. "
            "Gere um valor único: python -c \"import secrets; print(secrets.token_hex(32))\""
        )


_validate_secret("SECRET_KEY", settings.SECRET_KEY)
_validate_secret("RESET_SECRET_KEY", settings.RESET_SECRET_KEY)

if settings.SECRET_KEY == settings.RESET_SECRET_KEY:
    raise RuntimeError("SECRET_KEY e RESET_SECRET_KEY devem ser diferentes")

if not settings.SQLALCHEMY_DATABASE_URL:
    raise RuntimeError("DATABASE_URL não definida. Defina no arquivo .env")

if bool(settings.N8N_WEBHOOK_URL) != bool(settings.N8N_WEBHOOK_TOKEN):
    raise RuntimeError(
        "N8N_WEBHOOK_URL e N8N_WEBHOOK_TOKEN devem ser definidos juntos ou deixados vazios"
    )
