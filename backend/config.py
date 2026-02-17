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

settings = Settings()
