from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
from datetime import datetime


class Gender(Enum):
    MALE = "male"
    FEMALE = "female"


class Person(BaseModel):
    id: int = Field(..., description="Уникальный идентификатор человека")
    
    address_id: int = Field(..., description="Идентификатор адреса", ge=1)
    passport_id: int = Field(..., description="Идентификатор паспорта", ge=1)
    
    first_name: str = Field(..., description="Имя человека", max_length=32)
    middle_name: str = Field(..., description="Отчество человека", max_length=32)
    last_name: str = Field(..., description="Фамилия человека", max_length=32)
    birthday: datetime = Field(..., description="Дата рождения человека")
    gender: Gender = Field(Gender.MALE, description="Пол человека")
    
    email: str = Field(..., description="Электронная почта человека", max_length=256)
    phone: str = Field(..., description="Телефон человека", max_length=10)
    snils: str = Field(..., description="СНИЛС человека", max_length=11)

    created_at: datetime = Field(default_factory=datetime.now, description="Дата и время создания записи")
    updated_at: datetime = Field(default_factory=datetime.now, description="Дата и время последнего обновления записи")


class PersonCreate(BaseModel):
    address_id: int = Field(..., description="Идентификатор адреса", ge=1)
    passport_id: int = Field(..., description="Идентификатор паспорта", ge=1)
    
    first_name: str = Field(..., description="Имя человека", max_length=32)
    middle_name: str = Field(..., description="Отчество человека", max_length=32)
    last_name: str = Field(..., description="Фамилия человека", max_length=32)
    birthday: datetime = Field(..., description="Дата рождения человека")
    gender: Gender = Field(Gender.MALE, description="Пол человека")
    
    email: str = Field(..., description="Электронная почта человека", max_length=256)
    phone: str = Field(..., description="Телефон человека", max_length=10)
    snils: str = Field(..., description="СНИЛС человека", max_length=11)


class PersonUpdate(BaseModel):
    address_id: Optional[int] = Field(None, description="Идентификатор адреса", ge=1)
    passport_id: Optional[int] = Field(None, description="Идентификатор паспорта", ge=1)
    
    first_name: Optional[str] = Field(None, description="Имя человека", max_length=32)
    middle_name: Optional[str] = Field(None, description="Отчество человека", max_length=32)
    last_name: Optional[str] = Field(None, description="Фамилия человека", max_length=32)
    birthday: Optional[datetime] = Field(None, description="Дата рождения человека")
    gender: Optional[Gender] = Field(Gender.MALE, description="Пол человека",)
    
    email: Optional[str] = Field(None, description="Электронная почта человека", max_length=256)
    phone: Optional[str] = Field(None, description="Телефон человека", max_length=10)
    snils: Optional[str] = Field(None, description="СНИЛС человека", max_length=11)
