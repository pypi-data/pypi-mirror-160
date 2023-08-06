"""
Field API requests.
"""
import json
from typing import Dict, Any

from algoralabs.common.functions import no_transform
from algoralabs.common.requests import (
    __get_request, __put_request, __post_request, __delete_request,
    __async_get_request, __async_put_request, __async_post_request, __async_delete_request
)
from algoralabs.data.datasets import FieldRequest
from algoralabs.decorators.data import data_request, async_data_request


def _get_field_request_info(id: str) -> dict:
    return {
        "endpoint": f"config/datasets/field/{id}"
    }


@data_request(transformer=no_transform)
def get_field(id: str) -> Dict[str, Any]:
    """
    Get field by ID.

    Args:
        id (str): Field ID

    Returns:
        Dict[str, Any]: Field response
    """
    request_info = _get_field_request_info(id)
    return __get_request(**request_info)


@async_data_request(transformer=no_transform)
async def async_get_field(id: str) -> Dict[str, Any]:
    """
    Asynchronously get field by ID.

    Args:
        id (str): Field ID

    Returns:
        Dict[str, Any]: Field response
    """
    request_info = _get_field_request_info(id)
    return await __async_get_request(**request_info)


def _create_field_request_info(request: FieldRequest) -> dict:
    return {
        "endpoint": "config/datasets/field",
        "json": json.loads(request.json())
    }


@data_request(transformer=no_transform)
def create_field(request: FieldRequest) -> Dict[str, Any]:
    """
    Create field.

    Args:
        request (FieldRequest): Field request

    Returns:
        Dict[str, Any]: Field response
    """
    request_info = _create_field_request_info(request)
    return __put_request(**request_info)


@async_data_request(transformer=no_transform)
async def async_create_field(request: FieldRequest) -> Dict[str, Any]:
    """
    Asynchronously create field.

    Args:
        request (FieldRequest): Field request

    Returns:
        Dict[str, Any]: Field response
    """
    request_info = _create_field_request_info(request)
    return await __async_put_request(**request_info)


def _update_field_request_info(id: str, request: FieldRequest):
    return {
        "endpoint": f"config/datasets/field/{id}",
        "json": json.loads(request.json())
    }


@data_request(transformer=no_transform)
def update_field(id: str, request: FieldRequest) -> Dict[str, Any]:
    """
    Update field.

    Args:
        id (str): Field ID
        request (FieldRequest): Field request

    Returns:
        Dict[str, Any]: Field response
    """
    request_info = _update_field_request_info(id, request)
    return __post_request(**request_info)


@async_data_request(transformer=no_transform)
async def async_update_field(id: str, request: FieldRequest) -> Dict[str, Any]:
    """
    Asynchronously update field.

    Args:
        id (str): Field ID
        request (FieldRequest): Field request

    Returns:
        Dict[str, Any]: Field response
    """
    request_info = _update_field_request_info(id, request)
    return await __async_post_request(**request_info)


def _delete_field_request_info(id: str):
    return {
        "endpoint": f"config/datasets/field/{id}",
    }


@data_request(transformer=no_transform)
def delete_field(id: str) -> None:
    """
    Delete field by ID.

    Args:
        id (str): Field ID

    Returns:
        None
    """
    request_info = _delete_field_request_info(id, )
    return __delete_request(**request_info)


@async_data_request(transformer=no_transform)
async def async_delete_field(id: str) -> None:
    """
    Asynchronously delete field by ID.

    Args:
        id (str): Field ID

    Returns:
        None
    """
    request_info = _delete_field_request_info(id, )
    return await __async_delete_request(**request_info)
