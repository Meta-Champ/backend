from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class Passport(BaseModel):
    id: int = Field(..., description="Уникальный идентификатор паспорта")
    serial: str = Field(..., description="Серийный номер паспорта", max_length=4)  
    number: str = Field(..., description="Номер паспорта", max_length=6)  
    birthday_city: str = Field(..., description="Город рождения", max_length=32)  
    issued_by: str = Field(..., description="Кем выдан паспорт", max_length=128)  
    issued_code: str = Field(..., description="Код выдачи паспорта", max_length=6)  
    issued_date: datetime = Field(..., description="Дата выдачи паспорта")  
    created_at: datetime = Field(..., description="Дата и время создания записи")  
    updated_at: datetime = Field(..., description="Дата и время последнего обновления записи")  


class PassportCreate(BaseModel):
    serial: str = Field(..., description="Серийный номер паспорта", max_length=4)  
    number: str = Field(..., description="Номер паспорта", max_length=6)  
    birthday_city: str = Field(..., description="Город рождения", max_length=32)  
    issued_by: str = Field(..., description="Кем выдан паспорт", max_length=128)  
    issued_code: str = Field(..., description="Код выдачи паспорта", max_length=6)  
    issued_date: datetime = Field(..., description="Дата выдачи паспорта")  


class PassportUpdate(BaseModel):
    serial: Optional[str] = Field(None, description="Серийный номер паспорта", max_length=4)  
    number: Optional[str] = Field(None, description="Номер паспорта", max_length=6)  
    birthday_city: Optional[str] = Field(None, description="Город рождения", max_length=32)  
    issued_by: Optional[str] = Field(None, description="Кем выдан паспорт", max_length=128)  
    issued_code: Optional[str] = Field(None, description="Код выдачи паспорта", max_length=6)  
    issued_date: Optional[datetime] = Field(None, description="Дата выдачи паспорта")  
