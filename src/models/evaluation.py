from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class Evaluation(BaseModel):
    id: int = Field(..., description="Уникальный идентификатор оценки")
    direction_id: int = Field(..., description="Идентификатор направления")
    user_id: int = Field(..., description="Идентификатор пользователя")
    task_id: int = Field(..., description="Идентификатор задачи")
    score: float = Field(..., description="Оценка")
    created_at: datetime = Field(..., description="Дата и время создания оценки")
    updated_at: datetime = Field(..., description="Дата и время последнего обновления оценки")


class EvaluationCreate(BaseModel):
    direction_id: int = Field(..., description="Идентификатор направления")
    user_id: int = Field(..., description="Идентификатор пользователя")
    task_id: int = Field(..., description="Идентификатор задачи")
    score: float = Field(..., description="Оценка")

class EvaluationUpdate(BaseModel):
    score: float = Field(..., description="Оценка")

class EvaluationDump(BaseModel):
    data: list[Evaluation] = Field(..., description="Список оценок")
    total_count: int = Field(..., description="Общее количество оценок")
