from typing import Optional, cast
from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
import os
from dotenv import load_dotenv
from models.user import User # Adicionado para anotação de tipo, se necessário

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "SUA_CHAVE_SECRETA_MUITO_SEGURA_AQUI")
RESET_SECRET_KEY = os.getenv("RESET_SECRET_KEY", "OUTRA_CHAVE_SECRETA_PARA_RESET")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 300
RESET_TOKEN_EXPIRE_MINUTES = 30 # Token de reset expira em 30 min

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_reset_token(email: str):
    expire = datetime.utcnow() + timedelta(minutes=RESET_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": email, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, RESET_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_reset_token(token: str) -> Optional[str]:
    try:
        payload = jwt.decode(token, RESET_SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            return None
        return str(email)
    except JWTError:
        return None
