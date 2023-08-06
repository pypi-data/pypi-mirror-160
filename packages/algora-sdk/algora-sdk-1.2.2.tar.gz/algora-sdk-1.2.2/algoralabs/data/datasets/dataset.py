"""
Dataset API requests.
"""
import json
from typing import List, Dict, Any

from algoralabs.common.functions import no_transform
from algoralabs.common.requests import (
    __get_request, __put_request, __post_request, __delete_request,
    __async_get_request, __async_put_request, __async_post_request, __async_delete_request
)
from algoralabs.data.datasets import DatasetSearchRequest, DatasetRequest
from algoralabs.decorators.data import data_request, async_data_request


def _get_dataset_request_info(id: str) -> dict:
    return {
        "endpoint": f"config/datasets/dataset/{id}"
    }


@data_request(transformer=no_transform)
def get_dataset(id: str) -> Dict[str, Any]:
    """
    Get dataset by ID.

    Args:
        id (str): Dataset ID

    Returns:
        Dict[str, Any]: Dataset response
    """
    request_info = _get_dataset_request_info(id)
    return __get_request(**request_info)


@async_data_request(transformer=no_transform)
async def async_get_dataset(id: str) -> Dict[str, Any]:
    """
    Asynchronously get dataset by ID.

    Args:
        id (str): Dataset ID

    Returns:
        Dict[str, Any]: Dataset response
    """
    request_info = _get_dataset_request_info(id)
    return await __async_get_request(**request_info)


def _get_datasets_request_info() -> dict:
    return {
        "endpoint": f"config/datasets/dataset"
    }


@data_request(transformer=no_transform)
def get_datasets() -> List[Dict[str, Any]]:
    """
    Get all datasets.

    Returns:
        List[Dict[str, Any]]: List of dataset response
    """
    request_info = _get_datasets_request_info()
    return __get_request(**request_info)


@async_data_request(transformer=no_transform)
async def async_get_datasets() -> List[Dict[str, Any]]:
    """
    Asynchronously get all datasets.

    Returns:
        List[Dict[str, Any]]: List of dataset response
    """
    request_info = _get_datasets_request_info()
    return await __async_get_request(**request_info)


def _search_datasets_request_info(request: DatasetSearchRequest) -> dict:
    return {
        "endpoint": f"config/datasets/dataset/search",
        "json": json.loads(request.json())
    }


@data_request(transformer=no_transform)
def search_datasets(request: DatasetSearchRequest) -> List[Dict[str, Any]]:
    """
    Search all datasets.

    Args:
        request (DatasetSearchRequest): Dataset search request

    Returns:
        List[Dict[str, Any]]: List of dataset response
    """
    request_info = _search_datasets_request_info(request)
    return __post_request(**request_info)


@async_data_request(transformer=no_transform)
async def async_search_datasets(request: DatasetSearchRequest) -> List[Dict[str, Any]]:
    """
    Asynchronously search all datasets.

    Args:
        request (DatasetSearchRequest): Dataset search request

    Returns:
        List[Dict[str, Any]]: List of dataset response
    """
    request_info = _search_datasets_request_info(request)
    return await __async_post_request(**request_info)


def _create_dataset_request_info(request: DatasetRequest) -> dict:
    return {
        "endpoint": f"config/datasets/dataset",
        "json": json.loads(request.json())
    }


@data_request(transformer=no_transform)
def create_dataset(request: DatasetRequest) -> Dict[str, Any]:
    """
    Create dataset.

    Args:
        request (DatasetRequest): Dataset request

    Returns:
        Dict[str, Any]: Dataset response
    """
    request_info = _create_dataset_request_info(request)
    return __put_request(**request_info)


@async_data_request(transformer=no_transform)
async def async_create_dataset(request: DatasetRequest) -> Dict[str, Any]:
    """
    Asynchronously create dataset.

    Args:
        request (DatasetRequest): Dataset request

    Returns:
        Dict[str, Any]: Dataset response
    """
    request_info = _create_dataset_request_info(request)
    return await __async_put_request(**request_info)


def _update_dataset_request_info(id: str, request: DatasetRequest) -> dict:
    return {
        "endpoint": f"config/datasets/dataset/{id}",
        "json": json.loads(request.json())
    }


@data_request(transformer=no_transform)
def update_dataset(id: str, request: DatasetRequest) -> Dict[str, Any]:
    """
    Update dataset.

    Args:
        id (str): Dataset ID
        request (DatasetRequest): Dataset request

    Returns:
        Dict[str, Any]: Dataset response
    """
    request_info = _update_dataset_request_info(id, request)
    return __post_request(**request_info)


@async_data_request(transformer=no_transform)
async def async_update_dataset(id: str, request: DatasetRequest) -> Dict[str, Any]:
    """
    Asynchronously update dataset.

    Args:
        id (str): Dataset ID
        request (DatasetRequest): Dataset request

    Returns:
        Dict[str, Any]: Dataset response
    """
    request_info = _update_dataset_request_info(id, request)
    return await __async_post_request(**request_info)


def _delete_dataset_request_info(id: str) -> dict:
    return {
        "endpoint": f"config/datasets/dataset/{id}"
    }


@data_request(transformer=no_transform)
def delete_dataset(id: str) -> None:
    """
    Delete dataset by ID.

    Args:
        id (str): Dataset ID

    Returns:
        None
    """
    request_info = _delete_dataset_request_info(id)
    return __delete_request(**request_info)


@async_data_request(transformer=no_transform)
async def async_delete_dataset(id: str) -> None:
    """
    Asynchronously delete dataset by ID.

    Args:
        id (str): Dataset ID

    Returns:
        None
    """
    request_info = _delete_dataset_request_info(id)
    return await __async_delete_request(**request_info)
