"""
Schema API requests.
"""
import json
from typing import List, Dict, Any

from algoralabs.data.datasets import SchemaRequest, FieldRequest
from algoralabs.common.functions import no_transform
from algoralabs.decorators.data import data_request, async_data_request
from algoralabs.common.requests import (
    __get_request, __put_request, __post_request, __delete_request,
    __async_get_request, __async_put_request, __async_post_request, __async_delete_request
)


def _get_schema_request_info(id: str) -> dict:
    return {
        "endpoint": f"config/datasets/schema/{id}"
    }


@data_request(transformer=no_transform)
def get_schema(id: str) -> Dict[str, Any]:
    """
    Get schema by ID.

    Args:
        id (str): Schema ID

    Returns:
        Dict[str, Any]: Schema response
    """
    request_info = _get_schema_request_info(id)
    return __get_request(**request_info)


@async_data_request(transformer=no_transform)
async def async_get_schema(id: str) -> Dict[str, Any]:
    """
    Asynchronously get schema by ID.

    Args:
        id (str): Schema ID

    Returns:
        Dict[str, Any]: Schema response
    """
    request_info = _get_schema_request_info(id)
    return await __async_get_request(**request_info)


def _get_schemas_request_info() -> dict:
    return {
        "endpoint": f"config/datasets/schema"
    }


@data_request(transformer=no_transform)
def get_schemas() -> List[Dict[str, Any]]:
    """
    Get all schemas.

    Returns:
        List[Dict[str, Any]]: List of schema response
    """
    request_info = _get_schemas_request_info()
    return __get_request(**request_info)


@async_data_request(transformer=no_transform)
async def async_get_schemas() -> List[Dict[str, Any]]:
    """
    Asynchronously get all schemas.

    Returns:
        List[Dict[str, Any]]: List of schema response
    """
    request_info = _get_schemas_request_info()
    return await __async_get_request(**request_info)


def _get_schema_fields_request_info(id: str) -> dict:
    return {
        "endpoint": f"config/datasets/schema/{id}/fields"
    }


@data_request(transformer=no_transform)
def get_schema_fields(id: str) -> List[Dict[str, Any]]:
    """
    Get schema fields.

    Args:
        id (str): Schema ID

    Returns:
        List[Dict[str, Any]]: List of field response
    """
    request_info = _get_schema_fields_request_info(id)
    return __get_request(**request_info)


@async_data_request(transformer=no_transform)
async def async_get_schema_fields(id: str) -> List[Dict[str, Any]]:
    """
    Asynchronously get schema fields.

    Args:
        id (str): Schema ID

    Returns:
        List[Dict[str, Any]]: List of field response
    """
    request_info = _get_schema_fields_request_info(id)
    return await __async_get_request(**request_info)


def _create_schema_request_info(request: SchemaRequest) -> dict:
    return {
        "endpoint": f"config/datasets/schema",
        "json": json.loads(request.json())
    }


@data_request(transformer=no_transform)
def create_schema(request: SchemaRequest) -> Dict[str, Any]:
    """
    Create schema.

    Args:
        request (SchemaRequest): Schema request

    Returns:
        Dict[str, Any]: Schema response
    """
    request_info = _create_schema_request_info(request)
    return __put_request(**request_info)


@async_data_request(transformer=no_transform)
async def async_create_schema(request: SchemaRequest) -> Dict[str, Any]:
    """
    Asynchronously create schema.

    Args:
        request (SchemaRequest): Schema request

    Returns:
        Dict[str, Any]: Schema response
    """
    request_info = _create_schema_request_info(request)
    return await __async_put_request(**request_info)


def _update_schema_request_info(id: str, request: SchemaRequest) -> dict:
    return {
        "endpoint": f"config/datasets/schema/{id}",
        "json": json.loads(request.json())
    }


@data_request(transformer=no_transform)
def update_schema(id: str, request: SchemaRequest) -> Dict[str, Any]:
    """
    Update schema.

    Args:
        id (str): Schema ID
        request (SchemaRequest): Schema request

    Returns:
        Dict[str, Any]: Schema response
    """
    request_info = _update_schema_request_info(id, request)
    return __post_request(**request_info)


@async_data_request(transformer=no_transform)
async def async_update_schema(id: str, request: SchemaRequest) -> Dict[str, Any]:
    """
    Asynchronously update schema.

    Args:
        id (str): Schema ID
        request (SchemaRequest): Schema request

    Returns:
        Dict[str, Any]: Schema response
    """
    request_info = _update_schema_request_info(id, request)
    return await __async_post_request(**request_info)


def _update_schema_fields_request_info(id: str, request: List[FieldRequest]) -> dict:
    return {
        "endpoint": f"config/datasets/schema/{id}/fields",
        "json": [json.loads(f.json()) for f in request]
    }


@data_request(transformer=no_transform)
def update_schema_fields(id: str, request: List[FieldRequest]) -> List[Dict[str, Any]]:
    """
    Update schema fields.

    Args:
        id (str): Schema ID
        request (List[FieldRequest]): List of field request

    Returns:
         List[Dict[str, Any]]: List of field response
    """
    request_info = _update_schema_fields_request_info(id, request)
    return __post_request(**request_info)


@async_data_request(transformer=no_transform)
async def async_update_schema_fields(id: str, request: List[FieldRequest]) -> List[Dict[str, Any]]:
    """
    Asynchronously update schema fields.

    Args:
        id (str): Schema ID
        request (List[FieldRequest]): List of field request

    Returns:
         List[Dict[str, Any]]: List of field response
    """
    request_info = _update_schema_fields_request_info(id, request)
    return await __async_post_request(**request_info)


def _delete_schema_request_info(id: str) -> dict:
    return {
        "endpoint": f"config/datasets/schema/{id}"
    }


@data_request(transformer=no_transform)
def delete_schema(id: str) -> None:
    """
    Delete schema by ID.

    Args:
        id (str): Schema ID

    Returns:
        None
    """
    request_info = _delete_schema_request_info(id)
    return __delete_request(**request_info)


@async_data_request(transformer=no_transform)
async def async_delete_schema(id: str) -> None:
    """
    Asynchronously delete schema by ID.

    Args:
        id (str): Schema ID

    Returns:
        None
    """
    request_info = _delete_schema_request_info(id)
    return await __async_delete_request(**request_info)
