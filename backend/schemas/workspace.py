from pydantic import BaseModel, model_validator
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
    id: str
    created_at: datetime
    updated_at: datetime

    @model_validator(mode='before')
    @classmethod
    def map_uuid_to_id(cls, data):
        """Map the ORM model's 'uuid' field to 'id' for API responses."""
        # Handle ORM objects directly
        if hasattr(data, 'uuid'):
            return {
                'id': data.uuid,
                'name': data.name,
                'created_at': data.created_at,
                'updated_at': data.updated_at,
            }
        # Handle dicts that already have 'id' as uuid string (from list_my_workspaces)
        return data
    
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

    @model_validator(mode='before')
    @classmethod
    def map_uuid_to_id(cls, data):
        """Handle both ORM objects and dependency dicts (workspace + role)."""
        # Handle dependency dict: {"workspace": <ORM>, "role": <role>}
        if isinstance(data, dict) and 'workspace' in data:
            ws = data['workspace']
            return {
                'id': ws.uuid,
                'name': ws.name,
                'created_at': ws.created_at,
                'updated_at': ws.updated_at,
                'role': data['role'],
            }
        # Handle plain dicts (from list_my_workspaces)
        return data

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
