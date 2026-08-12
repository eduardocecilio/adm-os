from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from dependencies import get_current_active_user
from pydantic import BaseModel, EmailStr, Field
from auth_utils import get_password_hash, verify_password

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

from typing import Optional

class UserUpdate(BaseModel):
    current_password: str = Field(min_length=1)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(default=None, min_length=8)

class UserOut(BaseModel):
    id: int
    email: EmailStr
    is_active: bool

    class Config:
        from_attributes = True

@router.get("/me", response_model=UserOut)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@router.put("/me", response_model=UserOut)
async def update_user_me(user_update: UserUpdate,
                        current_user: User = Depends(get_current_active_user),
                        db: Session = Depends(get_db)):
    if not verify_password(user_update.current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Senha atual incorreta",
        )

    if user_update.email is None and user_update.password is None:
        raise HTTPException(status_code=400, detail="Nenhuma alteração informada")

    if user_update.email and user_update.email != current_user.email:
        # Check if email is taken
        existing_user = db.query(User).filter(User.email == user_update.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        current_user.email = user_update.email

    if user_update.password:
        current_user.hashed_password = get_password_hash(user_update.password)

    db.commit()
    db.refresh(current_user)
    return current_user
