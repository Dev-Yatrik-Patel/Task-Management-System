from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.core.responses import success_response, error_response
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.services.task_service import (
    create_task,
    get_tasks_for_user,
    get_task_by_id,
    update_task,
    delete_task,
)

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task_api(
    task_in: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = create_task(db, current_user, task_in)
    return success_response(data = TaskResponse.model_validate(task).model_dump(mode="json"))


@router.get("", response_model=list[TaskResponse])
async def list_tasks_api(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    tasks = get_tasks_for_user(db, current_user)
    data = [
        TaskResponse.model_validate(task).model_dump(mode="json")
        for task in tasks
    ]
    return success_response(data = data)


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task_api(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = get_task_by_id(db, task_id, current_user)
    if not task:
        return error_response(status_code = status.HTTP_404_NOT_FOUND, message="Task not found", error_code = "TASK_NOT_FOUND")
    return success_response(data = TaskResponse.model_validate(task).model_dump(mode="json"))

@router.put("/{task_id}", response_model=TaskResponse)
async def update_task_api(
    task_id: int,
    task_in: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = get_task_by_id(db, task_id, current_user)
    if not task:
        return error_response(status_code = status.HTTP_404_NOT_FOUND, message="Task not found", error_code = "TASK_NOT_FOUND")
        
    try:
        updated_task = update_task(db, task, task_in)
        return success_response(data = TaskResponse.model_validate(updated_task).model_dump(mode="json"))
    except ValueError as exc:
        return error_response(status_code = status.HTTP_400_BAD_REQUEST, message=str(exc), error_code = "VALUE_ERROR")


@router.delete("/{task_id}", status_code=status.HTTP_200_OK)
async def delete_task_api(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = get_task_by_id(db, task_id, current_user)
    if not task:
        return error_response(status_code = status.HTTP_404_NOT_FOUND, message="Task not found", error_code = "TASK_NOT_FOUND")

    delete_task(db, task)
    
    return success_response(message = "Task has been deleted successfully!")