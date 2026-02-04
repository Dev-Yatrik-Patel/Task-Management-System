from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.task import Task
from app.models.user import User
from app.schemas.task import TaskCreate, TaskUpdate

VALID_STATUSES = {"pending", "completed"}

def create_task(db: Session, user: User, task_in: TaskCreate) -> Task:
    task = Task(
        title=task_in.title,
        description=task_in.description,
        user_id=user.id,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def get_tasks_for_user( db: Session, user: User, page: int = 1, page_size: int = 20, search: str | None = None ) -> tuple[list[Task], int]:
    query = db.query(Task).filter(Task.user_id == user.id)

    if search:
        ilike = f"%{search}%"
        query = query.filter(
            or_(
                Task.title.ilike(ilike),
                Task.description.ilike(ilike),
            )
        )

    total = query.count()

    tasks = (
        query
        .order_by(Task.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    return tasks, total

def get_task_by_id(db: Session, task_id: int, user: User) -> Task | None:
    return (
        db.query(Task)
        .filter(Task.id == task_id, Task.user_id == user.id)
        .first()
    )

def update_task( db: Session, task: Task, task_in: TaskUpdate) -> Task:
    if task_in.title is not None:
        task.title = task_in.title
    if task_in.description is not None:
        task.description = task_in.description
    if task_in.status is not None:
        if task_in.status not in VALID_STATUSES:
            raise ValueError("Invalid task status")
        task.status = task_in.status
    db.commit()
    db.refresh(task)
    return task

def delete_task(db: Session, task: Task) -> None:
    db.delete(task)
    db.commit()
    return