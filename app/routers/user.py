from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder

from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.user import UserResponse
from app.core.responses import success_response

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return success_response(data = UserResponse.model_validate(current_user).model_dump(mode="json"))