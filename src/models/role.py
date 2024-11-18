from pydantic import BaseModel, Field
from typing import Optional


class Role(BaseModel):
    id: int = Field(..., description="Уникальный идентификатор роли")
    name: str = Field(..., description="Название роли", max_length=32)
    code: str = Field(..., description="Код роли", max_length=32)
    is_default: bool = Field(..., description="Является ли роль по умолчанию")
    created_at: int = Field(..., description="Дата и время создания роли")
    updated_at: int = Field(..., description="Дата и время последнего обновления роли")


class RoleCreate(BaseModel):
    name: str = Field(..., description="Название роли", max_length=32)
    code: str = Field(..., description="Код роли", max_length=32)
    is_default: bool = Field(..., description="Является ли роль по умолчанию")


class RoleUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Название роли", max_length=32)
    code: Optional[str] = Field(None, description="Код роли", max_length=32)
    is_default: Optional[bool] = Field(None, description="Является ли роль по умолчанию")


class RoleRights(BaseModel):
    id: int = Field(..., description="Уникальный идентификатор прав")
    role_id: int = Field(..., description="Идентификатор роли, к которой принадлежат права")
    right: str = Field(..., description="Право, связанное с ролью", max_length=32)
    sign: str = Field('00000', description="Подпись прав роли", max_length=5)
    created_at: int = Field(..., description="Дата и время создания прав роли")
    updated_at: int = Field(..., description="Дата и время последнего обновления прав роли")


class RoleRightsCreate(BaseModel):
    role_id: int = Field(..., description="Идентификатор роли, к которой принадлежат права")
    right: str = Field(..., description="Право, связанное с ролью", max_length=32)
    sign: str = Field('00000', description="Подпись прав роли", max_length=5)


class RoleRightsUpdate(BaseModel):
    role_id: Optional[int] = Field(None, description="Идентификатор роли, к которой принадлежат права")
    right: Optional[str] = Field(None, description="Право, связанное с ролью", max_length=32)
    sign: Optional[str] = Field('00000', description="Подпись прав роли", max_length=5)
