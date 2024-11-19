from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class Task(BaseModel):
    id: int = Field(..., description="Уникальный идентификатор задачи")
    direction_id: int = Field(..., description="Идентификатор направления", ge=1)
    name: str = Field(..., description="Название задачи", max_length=128)
    max_score: float = Field(..., description="Максимальный балл задачи", ge=0)
    created_at: datetime = Field(..., description="Дата и время создания задачи")
    updated_at: datetime = Field(..., description="Дата и время последнего обновления задачи")


class TaskCreate(BaseModel):
    direction_id: int = Field(..., description="Идентификатор направления", ge=1)
    name: str = Field(..., description="Название задачи", max_length=128)
    max_score: float = Field(..., description="Максимальный балл задачи", ge=0)


class TaskUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Название задачи", max_length=128)
    max_score: Optional[float] = Field(None, description="Максимальный балл задачи", ge=0)


class TaskDump(BaseModel):
    data: list[Task] = Field(..., description="Список задач")
    total_count: int = Field(..., description="Общее количество задач")
