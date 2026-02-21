from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from dependencies import get_current_active_user
from pydantic import BaseModel, EmailStr
from auth_utils import get_password_hash
from email_utils import send_email

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

from typing import Optional

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None

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


