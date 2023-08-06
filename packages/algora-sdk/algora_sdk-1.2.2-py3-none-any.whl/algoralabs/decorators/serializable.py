from typing import Callable, Union, Type

from pydantic import Field
from typing_extensions import Literal

from algoralabs.common import Base


def serializable(
        _cls: Base = None
) -> Union[Callable, Base]:
    """
    A decorator that sets the needed serializable fields on a class.

    Args:
        _cls (object): The class being decorated

    Returns:
        cls: The updated class with the configuration methods
    """

    def wrap(cls):
        annotations = {"descriptor": Literal[cls.name()]}
        return type(cls.name(), (cls,), {'__annotations__': annotations, 'descriptor': Field(cls.name())})

    if _cls is None:
        return wrap

    return wrap(_cls)
