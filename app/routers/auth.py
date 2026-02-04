from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.services.user_service import create_user, authenticate_user, get_user_by_email
from app.core.security import create_access_token
from app.core.responses import success_response, error_response

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate, db: Session = Depends(get_db)):
    existing_user = get_user_by_email(db, user_in.email)
    if existing_user:
        return error_response(status_code=status.HTTP_400_BAD_REQUEST,message="Email already registered",error_code = "ALREADY_REGISTERED_EMAIL")
    user = create_user(db, user_in)
    return success_response(data = UserResponse.model_validate(user).model_dump(mode="json"))


@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = authenticate_user(
        db,
        email=form_data.username,
        password=form_data.password,
    )
    if not user:
        return error_response(status_code=status.HTTP_401_UNAUTHORIZED,message="Invalid credentials",error_code = "UNAUTHORIZED")
    
    access_token = create_access_token(subject=str(user.id))
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
