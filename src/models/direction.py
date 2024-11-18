from pydantic import BaseModel, Field
from typing import Optional

class Direction(BaseModel):
    id: int = Field(..., description="Уникальный идентификатор направления")
    championship_id: int = Field(..., description="Идентификатор чемпионата")
    name: str = Field(..., description="Название направления")
    is_juniors: bool = Field(False, description="Является ли направление для юниоров")
    created_at: int = Field(..., description="Дата и время создания направления")
    updated_at: int = Field(..., description="Дата и время последнего обновления направления")

class DirectionCreate(BaseModel):
    championship_id: int = Field(..., description="Идентификатор чемпионата")
    name: str = Field(..., description="Название направления")
    is_juniors: bool = Field(False, description="Является ли направление для юниоров")

class DirectionUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Название направления")
    is_juniors: Optional[bool] = Field(False, description="Является ли направление для юниоров")