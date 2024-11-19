from pydantic import BaseModel, Field
from src.models.role import DirectionRoles  
from datetime import datetime


class Participant(BaseModel):
    id: int = Field(..., description="Уникальный идентификатор участника")
    role: DirectionRoles = Field(..., description="Роль участника")
    user_id: int = Field(..., description="Идентификатор пользователя")
    direction_id: int = Field(..., description="Идентификатор направления")
    created_at: datetime = Field(..., description="Дата и время создания участника")


class ParticipantCreate(BaseModel):
    role: DirectionRoles = Field(..., description="Роль участника")
    user_id: int = Field(..., description="Идентификатор пользователя")
    direction_id: int = Field(..., description="Идентификатор направления")
