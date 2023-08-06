"""
Field group API requests.
"""
import json
from typing import Dict, List, Any

from algoralabs.common.functions import no_transform
from algoralabs.common.requests import (
    __get_request, __put_request, __post_request, __delete_request,
    __async_get_request, __async_put_request, __async_post_request, __async_delete_request
)
from algoralabs.data.datasets import FieldGroupRequest
from algoralabs.decorators.data import data_request, async_data_request


def _get_field_group_request_info(id: str) -> dict:
    return {
        "endpoint": f"config/datasets/field-group/{id}"
    }


@data_request(transformer=no_transform)
def get_field_group(id: str) -> Dict[str, Any]:
    """
    Get field group by ID.

    Args:
        id (str): Field group ID

    Returns:
        Dict[str, Any]: Field group response
    """
    request_info = _get_field_group_request_info(id)
    return __get_request(**request_info)


@async_data_request(transformer=no_transform)
async def async_get_field_group(id: str) -> Dict[str, Any]:
    """
    Asynchronously get field group by ID.

    Args:
        id (str): Field group ID

    Returns:
        Dict[str, Any]: Field group response
    """
    request_info = _get_field_group_request_info(id)
    return await __async_get_request(**request_info)


def _get_field_groups_request_info() -> dict:
    return {
        "endpoint": f"config/datasets/field-group"
    }


@data_request(transformer=no_transform)
def get_field_groups() -> List[Dict[str, Any]]:
    """
    Get all field groups.

    Returns:
        List[Dict[str, Any]]: List of field group response
    """
    request_info = _get_field_groups_request_info()
    return __get_request(**request_info)


@async_data_request(transformer=no_transform)
async def async_get_field_groups() -> List[Dict[str, Any]]:
    """
    Asynchronously get all field groups.

    Returns:
        List[Dict[str, Any]]: List of field group response
    """
    request_info = _get_field_groups_request_info()
    return await __async_get_request(**request_info)


def _create_field_group_request_info(request: FieldGroupRequest) -> dict:
    return {
        "endpoint": f"config/datasets/field-group",
        "json": json.loads(request.json())
    }


@data_request(transformer=no_transform)
def create_field_group(request: FieldGroupRequest) -> Dict[str, Any]:
    """
    Create field group.

    Args:
        request (FieldGroupRequest): Field group request

    Returns:
        Dict[str, Any]: Field group response
    """
    request_info = _create_field_group_request_info(request)
    return __put_request(**request_info)


@async_data_request(transformer=no_transform)
async def async_create_field_group(request: FieldGroupRequest) -> Dict[str, Any]:
    """
    Asynchronously create field group.

    Args:
        request (FieldGroupRequest): Field group request

    Returns:
        Dict[str, Any]: Field group response
    """
    request_info = _create_field_group_request_info(request)
    return await __async_put_request(**request_info)


def _update_field_group_request_info(id: str, request: FieldGroupRequest) -> dict:
    return {
        "endpoint": f"config/datasets/field-group/{id}",
        "json": json.loads(request.json())
    }


@data_request(transformer=no_transform)
def update_field_group(id: str, request: FieldGroupRequest) -> Dict[str, Any]:
    """
    Update field group.

    Args:
        id (str): Field group ID
        request (FieldGroupRequest): Field group request

    Returns:
        Dict[str, Any]: Field group response
    """
    request_info = _update_field_group_request_info(id, request)
    return __post_request(**request_info)


@async_data_request(transformer=no_transform)
async def async_update_field_group(id: str, request: FieldGroupRequest) -> Dict[str, Any]:
    """
    Asynchronously update field group.

    Args:
        id (str): Field group ID
        request (FieldGroupRequest): Field group request

    Returns:
        Dict[str, Any]: Field group response
    """
    request_info = _update_field_group_request_info(id, request)
    return await __async_post_request(**request_info)


def delete_field_group(id: str) -> dict:
    return {
        "endpoint": f"config/datasets/field-group/{id}"
    }


@data_request(transformer=no_transform)
def delete_field_group(id: str) -> None:
    """
    Delete field group by ID.

    Args:
        id (str): Field group ID

    Returns:
        None
    """
    endpoint = f"config/datasets/field-group/{id}"
    return __delete_request(endpoint)


@async_data_request(transformer=no_transform)
async def async_delete_field_group(id: str) -> None:
    """
    Asynchronously delete field group by ID.

    Args:
        id (str): Field group ID

    Returns:
        None
    """
    endpoint = f"config/datasets/field-group/{id}"
    return await __async_delete_request(endpoint)
