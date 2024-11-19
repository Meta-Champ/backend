from pydantic import BaseModel, Field
from src.models.role import DirectionRoles  


class Participant(BaseModel):
    id: int = Field(..., description="Уникальный идентификатор участника")
    role: DirectionRoles = Field(..., description="Роль участника")
    user_id: int = Field(..., description="Идентификатор пользователя")
    direction_id: int = Field(..., description="Идентификатор направления")
    created_at: int = Field(..., description="Дата и время создания участника")


class ParticipantCreate(BaseModel):
    role: DirectionRoles = Field(..., description="Роль участника")
    user_id: int = Field(..., description="Идентификатор пользователя")
    direction_id: int = Field(..., description="Идентификатор направления")
