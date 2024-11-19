from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
from datetime import datetime
from .address import Address
from .passport import Passport


class Gender(Enum):
    MALE = "male"
    FEMALE = "female"


class PersonData(BaseModel):
    first_name: str = Field(..., description="Имя персоны", max_length=32)
    middle_name: str = Field(..., description="Отчество персоны", max_length=32)
    last_name: str = Field(..., description="Фамилия персоны", max_length=32)
    birthday: datetime = Field(..., description="Дата рождения персоны")
    gender: Gender = Field(Gender.MALE, description="Пол персоны")
    
    email: str = Field(..., description="Электронная почта персоны", max_length=256)
    phone: str = Field(..., description="Телефон персоны", max_length=10)
    snils: str = Field(..., description="СНИЛС персоны", max_length=11)


class PersonInternalCreate(PersonData):
    address_id: int = Field(..., description="Идентификатор адреса", ge=1)
    passport_id: int = Field(..., description="Идентификатор паспорта", ge=1)

class PersonInternal(PersonInternalCreate):
    id: int = Field(..., description="Уникальный идентификатор персоны")

    created_at: datetime = Field(default_factory=datetime.now, description="Дата и время создания записи")
    updated_at: datetime = Field(default_factory=datetime.now, description="Дата и время последнего обновления записи")

class PersonCreate(PersonData):
    address: Address = Field(..., description="Адрес персоны")
    passport: Passport = Field(..., description="Паспорт персоны")

class Person(PersonCreate):
    id: int = Field(..., description="Уникальный идентификатор персоны")
    created_at: datetime = Field(default_factory=datetime.now, description="Дата и время создания записи")
    updated_at: datetime = Field(default_factory=datetime.now, description="Дата и время последнего обновления записи")







class PersonUpdate(BaseModel):
    address: Optional[Address] = Field(None, description="Адрес персоны")
    passport: Optional[Passport] = Field(None, description="Паспорт персоны")
    
    first_name: Optional[str] = Field(None, description="Имя персоны", max_length=32)
    middle_name: Optional[str] = Field(None, description="Отчество персоны", max_length=32)
    last_name: Optional[str] = Field(None, description="Фамилия персоны", max_length=32)
    birthday: Optional[datetime] = Field(None, description="Дата рождения персоны")
    gender: Optional[Gender] = Field(Gender.MALE, description="Пол персоны",)
    
    email: Optional[str] = Field(None, description="Электронная почта персоны", max_length=256)
    phone: Optional[str] = Field(None, description="Телефон персоны", max_length=10)
    snils: Optional[str] = Field(None, description="СНИЛС персоны", max_length=11)


class PersonDump(BaseModel):
    data: list[Person] = Field(..., description="Список персон")
    total_count: int = Field(..., description="Общее количество персон")
