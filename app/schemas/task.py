from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes= True)