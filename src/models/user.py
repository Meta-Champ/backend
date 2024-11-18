from pydantic import Field, BaseModel
from typing import Optional


class User(BaseModel):
    id: int
    role_id: int = Field(..., description="Идентификатор роли пользователя", ge=1)
    person_id: Optional[int] = Field(None, description="Идентификатор персоны пользователя")
    username: str = Field(..., description="Имя пользователя", max_length=32)
    password: str = Field(..., description="Пароль пользователя", min_length=6)
    password_salt: str = Field(..., description="Соль для пароля пользователя", max_length=16)
    created_at: int = Field(..., description="Дата и время создания пользователя")
    updated_at: int = Field(..., description="Дата и время последнего обновления пользователя")


class UserCreate(BaseModel):
    role_id: int = Field(..., description="Идентификатор роли пользователя", ge=1)
    person_id: Optional[int] = Field(None, description="Идентификатор персоны пользователя")
    username: str = Field(..., description="Имя пользователя", max_length=32)
    password: str = Field(..., description="Пароль пользователя", min_length=6)


class UserUpdate(BaseModel):
    role_id: Optional[int] = Field(None, description="Идентификатор роли пользователя", ge=1)
    person_id: Optional[int] = Field(None, description="Идентификатор персоны пользователя")
    username: Optional[str] = Field(None, description="Имя пользователя", max_length=32)
    password: Optional[str] = Field(None, description="Пароль пользователя", min_length=6)
