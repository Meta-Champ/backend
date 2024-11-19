from pydantic import BaseModel, Field
from typing import Optional


class Address(BaseModel):
    id: int = Field(..., description="Уникальный идентификатор адреса")
    city: str = Field(..., description="Название города")
    region: str = Field(..., description="Название региона")
    appartament: str = Field(..., description="Номер квартиры")
    street: str = Field(..., description="Название улицы")
    house: str = Field(..., description="Номер дома")

class AddressCreate(BaseModel):
    city: str = Field(..., description="Название города")
    region: str = Field(..., description="Название региона")
    appartament: str = Field(..., description="Номер квартиры")
    street: str = Field(..., description="Название улицы")
    house: str = Field(..., description="Номер дома")

class AddressUpdate(BaseModel):
    city: Optional[str] = Field(None, description="Название города")
    region: Optional[str] = Field(None, description="Название региона")
    appartament: Optional[str] = Field(None, description="Номер квартиры")
    street: Optional[str] = Field(None, description="Название улицы")
    house: Optional[str] = Field(None, description="Номер дома")
