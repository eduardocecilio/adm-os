from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from database import get_db
from models.user import User
from auth_utils import get_password_hash, verify_password, create_access_token, create_reset_token, verify_reset_token
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from email_utils import send_email
from config import settings
from limiter import limiter

router = APIRouter(prefix="/auth", tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

class UserCreate(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

from models.workspace import Workspace, WorkspaceUser, WorkspaceRole

@router.post("/register", response_model=Token)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Este e-mail já está cadastrado")
    
    hashed_password = get_password_hash(user.password)
    new_user = User(email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # --- AUTO CREATE DEFAULT WORKSPACE ---
    workspace_name = f"Empresa de {user.email.split('@')[0].capitalize()}"
    new_workspace = Workspace(name=workspace_name)
    db.add(new_workspace)
    db.commit()
    db.refresh(new_workspace)
    
    workspace_user = WorkspaceUser(
        workspace_id=new_workspace.id,
        user_id=new_user.id,
        role=WorkspaceRole.OWNER
    )
    db.add(workspace_user)
    db.commit()
    
    access_token = create_access_token(data={"sub": new_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/token", response_model=Token)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="E-mail ou senha incorretos")
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

@router.post("/forgot-password")
@limiter.limit("3/minute")
async def forgot_password(request_data: ForgotPasswordRequest, request: Request, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request_data.email).first()
    if not user:
        # Avoid user enumeration by returning a generic success message
        return {"msg": "Se o e-mail existir, um link de recuperação será enviado."}
    
    reset_token = create_reset_token(email=user.email)
    
    frontend_url = settings.FRONTEND_URL
    reset_link = f"{frontend_url}/reset-password?token={reset_token}"
    
    await send_email(
        subject="Recuperação de Senha - Adm OS",
        email_to=[user.email],
        body={"link": reset_link, "message": "Clique no link para redefinir sua senha: "}
    )
    
    return {"msg": "Se o e-mail existir, um link de recuperação será enviado."}

@router.post("/reset-password")
def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    email = verify_reset_token(request.token)
    if not email:
        raise HTTPException(status_code=400, detail="Token inválido ou expirado")
        
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
        
    hashed_password = get_password_hash(request.new_password)
    user.hashed_password = hashed_password
    db.commit()
    
    return {"msg": "Senha redefinida com sucesso"}
