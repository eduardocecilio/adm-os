import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Database
    SQLALCHEMY_DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./adm_os.db")

    # JWT Security — obrigatórios em produção
    SECRET_KEY: str = os.getenv("SECRET_KEY", "")
    RESET_SECRET_KEY: str = os.getenv("RESET_SECRET_KEY", "")

    # Financial Constants
    ALIQ_EMOLUMENTOS: float = 0.000345
    ALIQ_IR_SWING_TRADE: float = 0.15

    # Email config (n8n webhook)
    N8N_WEBHOOK_URL: str = os.getenv("N8N_WEBHOOK_URL", "")
    N8N_WEBHOOK_TOKEN: str = os.getenv("N8N_WEBHOOK_TOKEN", "")
    EMAIL_FROM: str = os.getenv("EMAIL_FROM", "Adm OS <nao-responda@ceciliolab.com>")

    # Frontend settings
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:8082")

settings = Settings()

if not settings.SECRET_KEY:
    import warnings
    warnings.warn("SECRET_KEY não definida! Configure a variável de ambiente antes de rodar em produção.", RuntimeWarning, stacklevel=2)

if not settings.RESET_SECRET_KEY:
    import warnings
    warnings.warn("RESET_SECRET_KEY não definida! Configure a variável de ambiente antes de rodar em produção.", RuntimeWarning, stacklevel=2)
