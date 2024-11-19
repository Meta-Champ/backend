from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean, Text, BigInteger, Enum, Float
from sqlalchemy.types import TIMESTAMP
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql import func
from datetime import datetime

from src.models.role import SystemRoles, DirectionRoles
from src.models.person import Gender
from src.models.protocol import ProtocolStatus
from src.models.delivery import DeliveryStatus


class Base(DeclarativeBase):
    pass


class Address(Base):
    __tablename__ = 'addresses'

    id: int = Column(Integer, primary_key=True, autoincrement=True)

    city: str = Column(String(32), nullable=False)
    region: str = Column(String(32), nullable=False)
    appartament: str = Column(String(32), nullable=False)
    street: str = Column(String(32), nullable=False)
    house: str = Column(String(8), nullable=False)

    created_at = Column(TIMESTAMP(timezone=True), nullable=False, default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, default=func.now(), onupdate=func.now())


class Passport(Base):
    __tablename__ = 'passports'

    id: int = Column(Integer, primary_key=True, autoincrement=True)

    serial: str = Column(String(4), nullable=False)
    number: str = Column(String(6), nullable=False)
    birthday_city: str = Column(String(32), nullable=False)

    issued_by: str = Column(String(128), nullable=False)
    issued_code: str = Column(String(6), nullable=False)
    issued_date: datetime = Column(Date, nullable=False)

    created_at = Column(TIMESTAMP(timezone=True), nullable=False, default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, default=func.now(), onupdate=func.now())


class Championship(Base):
    __tablename__ = 'championships'

    id: int = Column(Integer, primary_key=True, autoincrement=True)

    name: str = Column(String(32), nullable=False)

    created_at = Column(TIMESTAMP(timezone=True), nullable=False, default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, default=func.now(), onupdate=func.now())


class Direction(Base):
    __tablename__ = 'directions'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    
    championship_id: int = Column(BigInteger, ForeignKey('championships.id'), nullable=False)

    name: str = Column(String(64), nullable=False)
    is_juniors: bool = Column(Boolean, nullable=False, default=False)

    created_at = Column(TIMESTAMP(timezone=True), nullable=False, default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, default=func.now(), onupdate=func.now())


class Person(Base):
    __tablename__ = 'persons'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    
    address_id: int = Column(BigInteger, ForeignKey('addresses.id'), nullable=False)
    passport_id: int = Column(BigInteger, ForeignKey('passports.id'), nullable=False)

    first_name: str = Column(String(32), nullable=False)
    middle_name: str = Column(String(32), nullable=False)
    last_name: str = Column(String(32), nullable=False)

    birthday: datetime = Column(Date, nullable=False)
    gender: Gender = Column(Enum(Gender), nullable=False, default=Gender.MALE)

    email: str = Column(String(256), nullable=False)
    phone: str = Column(String(10), nullable=False)
    snils: str = Column(String(11), nullable=False)

    created_at = Column(TIMESTAMP(timezone=True), nullable=False, default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, default=func.now(), onupdate=func.now())


class Delivery(Base):
    __tablename__ = 'delivery'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    
    direction_id: int = Column(BigInteger, ForeignKey('directions.id'), nullable=False)

    name: str = Column(String(255), nullable=False)
    count: int = Column(BigInteger, nullable=False)
    status: DeliveryStatus = Column(Enum(DeliveryStatus), nullable=False, default=DeliveryStatus.PENDING)

    created_at = Column(TIMESTAMP(timezone=True), nullable=False, default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, default=func.now(), onupdate=func.now())


class Task(Base):
    __tablename__ = 'tasks'

    id: int = Column(BigInteger, primary_key=True, autoincrement=True)
    
    direction_id: int = Column(BigInteger, ForeignKey('directions.id'), nullable=False)

    name: str = Column(String(128), nullable=False)
    max_score: float = Column(Float, nullable=False)

    created_at = Column(TIMESTAMP(timezone=True), nullable=False, default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, default=func.now(), onupdate=func.now())


class User(Base):
    __tablename__ = 'users'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    
    person_id: int = Column(BigInteger, ForeignKey('persons.id'), nullable=True)
    role: SystemRoles = Column(Enum(SystemRoles), nullable=False, default=SystemRoles.USER)

    username: str = Column(String(32), nullable=False)
    password: str = Column(String(64), nullable=False)
    password_salt: str = Column(String(16), nullable=False)

    created_at = Column(TIMESTAMP(timezone=True), nullable=False, default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, default=func.now(), onupdate=func.now())


class Protocol(Base):
    __tablename__ = 'protocols'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    
    direction_id: int = Column(BigInteger, ForeignKey('directions.id'), nullable=False)

    name: str = Column(String(32), nullable=False)
    text: str = Column(Text, nullable=False)
    status: ProtocolStatus = Column(Enum(ProtocolStatus), nullable=False, default=ProtocolStatus.PUBLISHED)
    assigned_by: list[int] = Column(BigInteger, ForeignKey('users.id'), nullable=False)

    created_at = Column(TIMESTAMP(timezone=True), nullable=False, default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, default=func.now(), onupdate=func.now())


class Participant(Base):
    __tablename__ = 'participants'

    id: int = Column(BigInteger, primary_key=True, nullable=False)
    role: DirectionRoles = Column(Enum(DirectionRoles), nullable=False, default=DirectionRoles.PARTICIPANT)

    user_id: int = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    direction_id: int = Column(BigInteger, ForeignKey('directions.id'), nullable=False)

    created_at = Column(TIMESTAMP(timezone=True), nullable=False, default=func.now())


class Evaluation(Base):
    __tablename__ = 'evaluations'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    
    direction_id: int = Column(BigInteger, ForeignKey('directions.id'), nullable=True)
    user_id: int = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    task_id: int = Column(BigInteger, ForeignKey('tasks.id'), nullable=False)

    created_at = Column(TIMESTAMP(timezone=True), nullable=False, default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, default=func.now(), onupdate=func.now())


def get_base():
    return Base
