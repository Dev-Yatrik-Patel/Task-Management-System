from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session
from app.dependencies.db import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.user import UserResponse
from app.core.responses import success_response

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return success_response(data = UserResponse.model_validate(current_user).model_dump(mode="json"))

@router.get("/deleteprofile")
async def delete_my_profile(current_user: User = Depends(get_current_user), db: Session = Depends(get_db) ):
    existing_user_profile = db.query(User).filter(User.id == current_user.id, User.is_active == True).first()
        
    if not existing_user_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    existing_user_profile.is_active = False
    db.commit()
    db.refresh(existing_user_profile)
    
    return success_response(message = "Profile has been deleted successfully!")