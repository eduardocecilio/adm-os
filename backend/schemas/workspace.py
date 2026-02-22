from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import enum

class WorkspaceRole(str, enum.Enum):
    OWNER = "OWNER"
    ADMIN = "ADMIN"
    MEMBER = "MEMBER"
    GUEST = "GUEST"

class WorkspaceBase(BaseModel):
    name: str

class WorkspaceCreate(WorkspaceBase):
    pass

class WorkspaceOut(WorkspaceBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True
        from_attributes = True

class WorkspaceUserBase(BaseModel):
    workspace_id: int
    user_id: int
    role: WorkspaceRole

class WorkspaceUserOut(WorkspaceUserBase):
    id: int
    joined_at: datetime
    
    class Config:
        orm_mode = True
        from_attributes = True

class WorkspaceWithRole(WorkspaceOut):
    role: WorkspaceRole

class WorkspaceInvite(BaseModel):
    email: str
    role: WorkspaceRole = WorkspaceRole.MEMBER

class WorkspaceUpdate(BaseModel):
    name: str

class WorkspaceMemberOut(BaseModel):
    user_id: int
    email: str
    role: WorkspaceRole
    joined_at: datetime
    
    class Config:
        from_attributes = True
        orm_mode = True
