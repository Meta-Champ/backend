from pydantic import BaseModel, Field
from typing import Optional


class Championship(BaseModel):
    id: int = Field(..., description="Уникальный идентификатор чемпионата")
    name: str = Field(..., description="Название чемпионата")
    created_at: int = Field(..., description="Дата и время создания чемпионата")
    updated_at: int = Field(..., description="Дата и время последнего обновления чемпионата")


class ChampionshipCreate(BaseModel):
    name: str = Field(..., description="Название чемпионата")


class ChampionshipUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Название чемпионата")
