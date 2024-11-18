from pydantic import BaseModel, Field


class Participant(BaseModel):
    id: int = Field(..., description="Уникальный идентификатор участника")
    user_id: int = Field(..., description="Идентификатор пользователя")
    direction_id: int = Field(..., description="Идентификатор направления")
    created_at: int = Field(..., description="Дата и время создания участника")


class ParticipantCreate(BaseModel):
    user_id: int = Field(..., description="Идентификатор пользователя")
    direction_id: int = Field(..., description="Идентификатор направления")
