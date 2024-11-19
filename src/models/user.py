from pydantic import Field, BaseModel
from typing import Optional
from src.models.role import SystemRoles


class User(BaseModel):
    id: int
    person_id: Optional[int] = Field(None, description="Идентификатор персоны пользователя")
    role: SystemRoles = Field(..., description="Роль пользователя")
    username: str = Field(..., description="Имя пользователя", max_length=32)
    password: str = Field(..., description="Пароль пользователя", min_length=6)
    password_salt: str = Field(..., description="Соль для пароля пользователя", max_length=16)
    created_at: int = Field(..., description="Дата и время создания пользователя")
    updated_at: int = Field(..., description="Дата и время последнего обновления пользователя")


class UserCreate(BaseModel):
    person_id: Optional[int] = Field(None, description="Идентификатор персоны пользователя")
    role: SystemRoles = Field(..., description="Роль пользователя")
    username: str = Field(..., description="Имя пользователя", max_length=32)
    password: str = Field(..., description="Пароль пользователя", min_length=6)


class UserCreateInternal(UserCreate):
    password_salt: str = Field(..., description="Соль для пароля пользователя", max_length=16)


class UserUpdate(BaseModel):
    person_id: Optional[int] = Field(None, description="Идентификатор персоны пользователя")
    role: Optional[SystemRoles] = Field(None, description="Роль пользователя")
    username: Optional[str] = Field(None, description="Имя пользователя", max_length=32)
    password: Optional[str] = Field(None, description="Пароль пользователя", min_length=6)
