from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from database import get_db
from models.user import User
from auth_utils import get_password_hash, verify_password, create_access_token, create_reset_token, verify_reset_token
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated, Optional
from email_utils import send_email
from config import settings
from limiter import limiter

router = APIRouter(prefix="/auth", tags=["auth"])
LOCAL_REGISTRATION_HOSTS = frozenset({"127.0.0.1", "::1", "localhost", "testserver"})

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    workspace_name: Optional[str] = None
    invite_token: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str

from models.workspace import Workspace, WorkspaceUser, WorkspaceRole
from auth_utils import verify_invite_token

@router.post("/register", response_model=Token)
@limiter.limit("5/minute")
def register(request: Request, user: UserCreate, db: Session = Depends(get_db)):
    if len(user.password) < 8:
        raise HTTPException(status_code=400, detail="A senha deve ter pelo menos 8 caracteres.")

    if (
        not user.invite_token
        and not settings.ALLOW_PUBLIC_REGISTRATION
        and (request.url.hostname or "").lower() not in LOCAL_REGISTRATION_HOSTS
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=(
                "Cadastro público desativado. Use um convite ou execute a "
                "demonstração em localhost."
            ),
        )

    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Este e-mail já está cadastrado")

    invited_workspace_id = None
    invited_role = None

    if user.invite_token:
        invite_data = verify_invite_token(user.invite_token)
        if not invite_data or invite_data["email"].lower() != user.email.lower():
            raise HTTPException(status_code=400, detail="Token de convite inválido ou expirado para este e-mail.")
        invited_workspace_id = invite_data["workspace_id"]
        invited_role = invite_data["role"]
    hashed_password = get_password_hash(user.password)
    new_user = User(email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    if invited_workspace_id:
        workspace_user = WorkspaceUser(
            workspace_id=invited_workspace_id,
            user_id=new_user.id,
            role=invited_role
        )
        db.add(workspace_user)
        db.commit()
    else:
        ws_name = user.workspace_name if user.workspace_name else f"Empresa de {user.email.split('@')[0].capitalize()}"
        new_workspace = Workspace(name=ws_name)
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

    access_token = create_access_token(
        data={"sub": new_user.email},
        auth_version=new_user.auth_version,
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/token", response_model=Token)
@limiter.limit("10/minute")
def login(request: Request, form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="E-mail ou senha incorretos")

    access_token = create_access_token(
        data={"sub": user.email},
        auth_version=user.auth_version,
    )
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
        return {"msg": "Se o e-mail existir, um link de recuperação será enviado."}

    reset_token = create_reset_token(
        email=user.email,
        auth_version=user.auth_version,
    )
    reset_link = f"{settings.FRONTEND_URL}/reset-password?token={reset_token}"

    await send_email(
        subject="Recuperação de Senha - Adm OS",
        email_to=[user.email],
        body={"link": reset_link, "message": "Clique no link para redefinir sua senha: "}
    )

    return {"msg": "Se o e-mail existir, um link de recuperação será enviado."}

@router.post("/reset-password")
def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    if len(request.new_password) < 8:
        raise HTTPException(status_code=400, detail="A nova senha deve ter pelo menos 8 caracteres.")

    reset_data = verify_reset_token(request.token)
    if not reset_data:
        raise HTTPException(status_code=400, detail="Token inválido ou expirado")

    user = db.query(User).filter(User.email == reset_data["email"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    updated = (
        db.query(User)
        .filter(
            User.id == user.id,
            User.auth_version == reset_data["auth_version"],
        )
        .update(
            {
                User.hashed_password: get_password_hash(request.new_password),
                User.auth_version: User.auth_version + 1,
            },
            synchronize_session=False,
        )
    )
    if updated != 1:
        db.rollback()
        raise HTTPException(status_code=400, detail="Token inválido ou já utilizado")
    db.commit()

    return {"msg": "Senha redefinida com sucesso"}
