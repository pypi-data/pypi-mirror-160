"""
Decorator utilities.
"""
import dataclasses
import json
from typing import Any, Callable, _GenericAlias

from algoralabs.common.errors import CastingError
from algoralabs.common.functions import coalesce_callables, coalesce, dataclass_to_dict


def __dataclass_to_json_str(data_cls: dataclasses.dataclass, remove_none: bool) -> str:
    """
    Get all the dataclass fields (i.e. the key value pairs) and build a json string representation.

    NOTE: This is used by the decorators and is set as the __str__ method for the class being decorated.

    Args:
        data_cls (dataclass): The dataclass being converted to json
        remove_none (bool): A flag used to remove key value pairs where the value is None from the json conversion

    Returns:
        str: A string representation of the dataclass
    """
    data_cls_dict = dataclass_to_dict(data_cls, remove_none)
    return json.dumps(data_cls_dict, indent=4)


def __get_input(default_callable: Callable[[], Any], *args, **kwargs):
    """
    Determine the input that is used to populate the class.

    Args:
        default_callable (Callable[[], Any]): A callable method that returns the input for populating the class
        *args: The arg tuple passed to the method
        **kwargs: The keyword dictionary passed to the method

    Returns:
        Any: The input used to populate the class
    """

    return coalesce_callables(
        kwargs or None,
        # args[0] if args else None,
        default_callable,
    )


# TODO: Make the cast recursive to handle nested classes at any depth
def __attempt_cast(name: str, value: Any, typ: type, exception: CastingError = CastingError) -> Any:
    """
    Attempt to cast the value in the name-value pair to the desired type. Throw an exception if the casting fails.

    Args:
        name (str): The name of the variable being cast
        value (Any): The value to be cast
        typ (type): The desired type to cast the value too
        exception (CastingError): The exception type thrown if the casting fails

    Returns:
        Any: Any
    """
    if isinstance(value, typ):
        return value

    value_typ = type(value)

    # TODO: Handle SpecialForm Types
    # Recursive case
    if isinstance(typ, _GenericAlias):
        origin = typ.__origin__
        nested_types = typ.__args__

        # TODO: support k, v pair casts
        if nested_types:
            nested_obj = [__attempt_cast(name, val, nested_types[0], exception) for val in value]
        else:
            nested_obj = value

        return __attempt_cast(name, nested_obj, origin, exception)

    try:
        # Base Case
        if value_typ is dict and typ is not dict:
            return typ(**value)
        return typ(value)
    except (ValueError, TypeError) as e:
        raise exception(f"\nField {name} with value {value} is of the wrong type."
                        f"\n\tExpected type: {typ}"
                        f"\n\tError: {e}")


def __initialize_data_class(data_cls: dataclasses.dataclass, inp: dict, exception) -> None:
    """
    Initialize the dataclasses fields using the input provided. Throw an exception if the field value is missing and
    there is no default present.

    Args:
        data_cls (dataclass): The class being initialized
        inp (dict): The input used to initialize the dataclass
        exception: The error thrown if the dataclass field value is missing

    Returns:
        None
    """
    for name, field_info in data_cls.__dataclass_fields__.items():
        value = coalesce(inp.get(name, None), getattr(data_cls, name, None), field_info.default)
        if value is dataclasses.MISSING:
            raise exception(f"Missing the required field {name}")
        attr = __attempt_cast(name, value, field_info.type, exception=exception) if value is not None else value
        setattr(data_cls, name, attr)
