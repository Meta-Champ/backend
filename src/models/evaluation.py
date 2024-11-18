from pydantic import BaseModel, Field
from typing import Optional


class Evaluation(BaseModel):
    id: int = Field(..., description="Уникальный идентификатор оценки")
    direction_id: int = Field(..., description="Идентификатор направления")
    user_id: int = Field(..., description="Идентификатор пользователя")
    task_id: int = Field(..., description="Идентификатор задачи")
    created_at: int = Field(..., description="Дата и время создания оценки")
    updated_at: int = Field(..., description="Дата и время последнего обновления оценки")


class EvaluationCreate(BaseModel):
    direction_id: int = Field(..., description="Идентификатор направления")
    user_id: int = Field(..., description="Идентификатор пользователя")
    task_id: int = Field(..., description="Идентификатор задачи")


class EvaluationUpdate(BaseModel):
    task_id: int = Field(..., description="Идентификатор задачи")