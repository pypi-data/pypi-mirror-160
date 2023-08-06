from enum import Enum

from algoralabs.common.base import BaseEnum, Base


class Order(BaseEnum):
    ASC = 'ASC'
    DESC = 'DESC'


class FieldType(Enum):
    BOOLEAN = 'BOOLEAN'
    DOUBLE = 'DOUBLE'
    INTEGER = 'INTEGER'
    TEXT = 'TEXT'
    TIMESTAMP = 'TIMESTAMP'
    DATETIME = 'DATETIME'
    UNKNOWN = 'UNKNOWN'


class Field(Base):
    logical_name: str
    type: FieldType
