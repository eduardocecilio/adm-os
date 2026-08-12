from typing import Optional
from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from config import settings

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 300
RESET_TOKEN_EXPIRE_MINUTES = 30
INVITE_TOKEN_EXPIRE_MINUTES = 10080  # 7 dias

TOKEN_TYPE_CLAIM = "token_type"
ACCESS_TOKEN_TYPE = "access"
RESET_TOKEN_TYPE = "reset"
INVITE_TOKEN_TYPE = "invite"
INVITABLE_ROLES = frozenset({"MEMBER", "ADMIN"})

SECRET_KEY = settings.SECRET_KEY
RESET_SECRET_KEY = settings.RESET_SECRET_KEY

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
    # The token type is assigned here instead of trusting caller-provided data.
    to_encode.update({"exp": expire, TOKEN_TYPE_CLAIM: ACCESS_TOKEN_TYPE})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_reset_token(email: str):
    expire = datetime.utcnow() + timedelta(minutes=RESET_TOKEN_EXPIRE_MINUTES)
    to_encode = {
        "sub": email,
        "exp": expire,
        TOKEN_TYPE_CLAIM: RESET_TOKEN_TYPE,
    }
    encoded_jwt = jwt.encode(to_encode, RESET_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_reset_token(token: str) -> Optional[str]:
    try:
        payload = jwt.decode(token, RESET_SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if (
            payload.get(TOKEN_TYPE_CLAIM) != RESET_TOKEN_TYPE
            or not isinstance(email, str)
            or not email
        ):
            return None
        return email
    except JWTError:
        return None

def create_invite_token(email: str, workspace_id: int, role: str):
    role_value = getattr(role, "value", role)
    if role_value not in INVITABLE_ROLES:
        raise ValueError("Convites só podem conceder os papéis MEMBER ou ADMIN.")

    expire = datetime.utcnow() + timedelta(minutes=INVITE_TOKEN_EXPIRE_MINUTES)
    to_encode = {
        "sub": email,
        "workspace_id": workspace_id,
        "role": role_value,
        "exp": expire,
        TOKEN_TYPE_CLAIM: INVITE_TOKEN_TYPE,
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_invite_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        workspace_id = payload.get("workspace_id")
        role = payload.get("role")

        if (
            payload.get(TOKEN_TYPE_CLAIM) != INVITE_TOKEN_TYPE
            or not isinstance(email, str)
            or not email
            or not isinstance(workspace_id, int)
            or isinstance(workspace_id, bool)
            or workspace_id <= 0
            or role not in INVITABLE_ROLES
        ):
            return None

        return {
            "email": email,
            "workspace_id": workspace_id,
            "role": role,
        }
    except (JWTError, TypeError, ValueError):
        return None
