"""
Base implementation classes for passing on inherited attributes.
"""
from abc import ABC
from datetime import date
from enum import Enum
from typing import Union
from typing_extensions import Annotated
from pydantic import BaseModel, Field, create_model

from algoralabs.common.functions import date_to_timestamp


class BaseEnum(str, Enum):
    """
    Base class for all enum classes.

    Note: Inheriting from str is necessary to correctly serialize output of enum
    """
    pass


class Base(ABC, BaseModel):
    class Config:
        # use enum values when using .dict() on object
        use_enum_values = True
        json_encoders = {
            date: date_to_timestamp
        }

    @classmethod
    def name(cls) -> str:
        return cls.__name__

    @classmethod
    def new_fields(cls, *args, **kwargs):
        return {}

    @classmethod
    def update(cls, *args, **kwargs):
        new_fields = cls.new_fields(*args, **kwargs)
        return create_model(cls.__name__, __base__=cls, **new_fields)


def create_annotation(*types):
    class Annotation:
        types = ()

        @classmethod
        def annotation(cls):
            return Annotated[Union[cls.types], Field(discriminator='descriptor')]

        @classmethod
        def add_types(cls, *new_types):
            updated_types = cls.types + new_types
            cls.types = updated_types

    annotation = Annotation()
    annotation.add_types(*types)
    return Annotation
