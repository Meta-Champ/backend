from enum import Enum


class SystemRoles(Enum):
    OWNER = 'owner'
    ADMIN = 'admin'
    USER = 'user'


class DirectionRoles(Enum):
    CHIEF_EXPERT = 'chief_expert'
    TECHNICAL_ADMINISTRATOR = 'technical_administrator'
    INDUSTRIAL_EXPERT = 'industrial_expert'
    EXPERT = 'expert'
    PARTICIPANT = 'participant'
