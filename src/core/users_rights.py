from enum import Enum


class RightBits(Enum):
    CREATION: int = 1
    FIND: int = 2
    UPDATE: int = 4
    DELETE: int = 8
    PRIVACY: int = 16


class RightSections(Enum):
    ROLE: str = 'role'
    CHAMPIONSHIP: str = 'championship'
    DIRECTION: str = 'direction'
    PERSON: str = 'person'
    DELIVERY: str = 'delivery'
    TASK: str = 'task'
    USER: str = 'user'
    PROTOCOL: str = 'protocol'
    PARTICIPANT: str = 'participant'
    EVALUATION: str = 'evaluation'
