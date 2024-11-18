from pydantic import BaseModel, Field
from typing import Optional


class Task(BaseModel):
    id: int = Field(..., description="Уникальный идентификатор задачи")
    direction_id: int = Field(..., description="Идентификатор направления", ge=1)
    name: str = Field(..., description="Название задачи", max_length=128)
    max_score: int = Field(..., description="Максимальный балл задачи", ge=0)
    created_at: int = Field(..., description="Дата и время создания задачи")
    updated_at: int = Field(..., description="Дата и время последнего обновления задачи")


class TaskCreate(BaseModel):
    direction_id: int = Field(..., description="Идентификатор направления", ge=1)
    name: str = Field(..., description="Название задачи", max_length=128)
    max_score: int = Field(..., description="Максимальный балл задачи", ge=0)


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, description="Название задачи")
    name: str = Field(..., description="Название задачи", max_length=128)
    max_score: int = Field(..., description="Максимальный балл задачи", ge=0)
