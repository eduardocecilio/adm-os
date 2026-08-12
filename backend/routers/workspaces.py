from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.user import User
from models.workspace import Workspace, WorkspaceUser, WorkspaceRole
from schemas.workspace import WorkspaceCreate, WorkspaceOut, WorkspaceWithRole, WorkspaceInvite, WorkspaceUpdate, WorkspaceMemberOut
from dependencies import get_current_active_user, get_workspace_access, get_workspace_admin_access
from limiter import limiter

router = APIRouter(prefix="/workspaces", tags=["workspaces"])

@router.post("/", response_model=WorkspaceOut, status_code=status.HTTP_201_CREATED)
def create_workspace(workspace_in: WorkspaceCreate, current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    name = workspace_in.name.strip()
    if not name:
        raise HTTPException(status_code=400, detail="O nome do workspace não pode ser vazio.")
    if len(name) > 100:
        raise HTTPException(status_code=400, detail="O nome do workspace deve ter no máximo 100 caracteres.")
    workspace = Workspace(name=name)
    db.add(workspace)
    db.commit()
    db.refresh(workspace)

    # Associate the current user as the OWNER of the new workspace
    workspace_user = WorkspaceUser(
        workspace_id=workspace.id,
        user_id=current_user.id,
        role=WorkspaceRole.OWNER
    )
    db.add(workspace_user)
    db.commit()

    return workspace

@router.get("/", response_model=List[WorkspaceWithRole])
def list_my_workspaces(current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    # Get all workspaces where the user is a member
    user_workspaces = db.query(WorkspaceUser).filter(WorkspaceUser.user_id == current_user.id).all()

    results = []
    for wu in user_workspaces:
        ws = wu.workspace
        # Combine the workspace model with the specific user's role
        results.append({
            "id": ws.uuid,
            "name": ws.name,
            "created_at": ws.created_at,
            "updated_at": ws.updated_at,
            "role": wu.role
        })

    return results

@router.get("/{workspace_id}", response_model=WorkspaceWithRole)
def get_workspace(workspace_id: str, workspace_data: dict = Depends(get_workspace_access)):
    # workspace_data is returned by the dependency and contains both workspace and role
    return workspace_data

from auth_utils import create_invite_token
from email_utils import send_email
from config import settings

@router.post("/{workspace_id}/invite", status_code=status.HTTP_200_OK)
@limiter.limit("5/minute")
async def invite_user(
    request: Request,
    workspace_id: str,
    invite_data: WorkspaceInvite,
    workspace_data: dict = Depends(get_workspace_admin_access),
    db: Session = Depends(get_db)
):
    workspace = workspace_data["workspace"]
    invite_role = WorkspaceRole(invite_data.role.value)

    if invite_role not in (WorkspaceRole.MEMBER, WorkspaceRole.ADMIN):
        raise HTTPException(
            status_code=400,
            detail="Convites só podem conceder os papéis MEMBER ou ADMIN.",
        )

    # Check if user to invite already exists in the system
    target_user = db.query(User).filter(User.email == invite_data.email).first()

    if target_user:
        # User exists. Check if they are already in THIS workspace
        existing_link = db.query(WorkspaceUser).filter(
            WorkspaceUser.workspace_id == workspace.id,
            WorkspaceUser.user_id == target_user.id
        ).first()

        if existing_link:
            raise HTTPException(status_code=400, detail="Este usuário já faz parte do workspace.")

        # No authenticated invitation-acceptance flow is implemented yet.
        # Fail closed instead of attaching an existing account without its consent.
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "Convites para usuários já cadastrados exigem um fluxo de "
                "aceite que ainda não está disponível."
            ),
        )

    else:
        # User does NOT exist. Generate Magic Link
        invite_token = create_invite_token(
            email=invite_data.email,
            workspace_id=workspace.id,
            role=invite_role.value,
        )

        frontend_url = settings.FRONTEND_URL
        magic_link = f"{frontend_url}/register?invite={invite_token}"

        await send_email(
            subject=f"Você foi convidado para a organização {workspace.name} - Adm OS",
            email_to=[invite_data.email],
            body={
                "link": magic_link,
                "message": f"Você foi convidado para se juntar à organização '{workspace.name}' no Adm OS. Clique no link abaixo para criar sua conta gratuita e aceitar o convite:"
            }
        )

        return {"msg": f"Um convite foi enviado por e-mail para {invite_data.email}."}

@router.put("/{workspace_id}", response_model=WorkspaceOut)
def update_workspace(
    workspace_id: str,
    workspace_in: WorkspaceUpdate,
    workspace_data: dict = Depends(get_workspace_admin_access),
    db: Session = Depends(get_db)
):
    workspace = workspace_data["workspace"]
    name = workspace_in.name.strip()
    if not name:
        raise HTTPException(status_code=400, detail="O nome do workspace não pode ser vazio.")
    if len(name) > 100:
        raise HTTPException(status_code=400, detail="O nome do workspace deve ter no máximo 100 caracteres.")
    workspace.name = name
    db.commit()
    db.refresh(workspace)
    return workspace

@router.get("/{workspace_id}/members", response_model=List[WorkspaceMemberOut])
def list_workspace_members(
    workspace_id: str,
    workspace_data: dict = Depends(get_workspace_access),
    db: Session = Depends(get_db)
):
    workspace = workspace_data["workspace"]
    # Join WorkspaceUser and User
    members = db.query(WorkspaceUser, User).join(User, WorkspaceUser.user_id == User.id).filter(WorkspaceUser.workspace_id == workspace.id).all()

    results = []
    for wu, user in members:
        results.append({
            "user_id": user.id,
            "email": user.email,
            "role": wu.role,
            "joined_at": wu.joined_at
        })
    return results

@router.delete("/{workspace_id}/members/{user_id}", status_code=status.HTTP_200_OK)
def remove_member(
    workspace_id: str,
    user_id: int,
    workspace_data: dict = Depends(get_workspace_admin_access),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    workspace = workspace_data["workspace"]

    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="Você não pode remover a si mesmo por este canal.")

    link = db.query(WorkspaceUser).filter(
        WorkspaceUser.workspace_id == workspace.id,
        WorkspaceUser.user_id == user_id
    ).first()

    if not link:
        raise HTTPException(status_code=404, detail="Usuário não encontrado neste workspace.")

    if link.role == WorkspaceRole.OWNER:
        if workspace_data["role"] != WorkspaceRole.OWNER:
            raise HTTPException(status_code=403, detail="Apenas o criador (OWNER) pode remover outro dono.")
        owner_count = db.query(WorkspaceUser).filter(
            WorkspaceUser.workspace_id == workspace.id,
            WorkspaceUser.role == WorkspaceRole.OWNER
        ).count()
        if owner_count <= 1:
            raise HTTPException(status_code=400, detail="Não é possível remover o único dono do workspace.")

    db.delete(link)
    db.commit()
    return {"msg": "Usuário removido do workspace com sucesso."}
