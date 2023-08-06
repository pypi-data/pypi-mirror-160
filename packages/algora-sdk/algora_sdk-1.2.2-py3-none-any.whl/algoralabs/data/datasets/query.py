"""
Dataset query API requests.
"""
from requests import Response

from algoralabs.common.requests import (
    __get_request, __post_request,
    __async_get_request, __async_post_request
)


def _query_datasets_request_info(id: str, data=None, json=None) -> dict:
    return {
        "endpoint": f"data/datasets/query/{id}",
        "data": data,
        "json": json
    }


def query_dataset(id: str, data=None, json=None) -> Response:
    """
    Query dataset by ID.

    Args:
        id (str): Dataset ID
        data (Any): Data to POST
        json (Any): Data to POST

    Returns:
        Response: HTTP response object
    """
    request_info = _query_datasets_request_info(id, data, json)
    return __post_request(**request_info)


async def async_query_dataset(id: str, data=None, json=None) -> Response:
    """
    Asynchronously query dataset by ID.

    Args:
        id (str): Dataset ID
        data (Any): Data to POST
        json (Any): Data to POST

    Returns:
        Response: HTTP response object
    """
    request_info = _query_datasets_request_info(id, data, json)
    return await __async_post_request(**request_info)


def _query_dataset_csv_request_info(id: str, data=None) -> dict:
    return {
        "endpoint": f"data/datasets/query/{id}.csv",
        "data": data
    }


def query_dataset_csv(id: str, data=None) -> Response:
    """
    Query dataset CSV by ID.

    Args:
        id (str): Dataset ID
        data (Any): Data to POST

    Returns:
        Response: HTTP response object
    """
    request_info = _query_dataset_csv_request_info(id, data)
    return __get_request(**request_info)


async def async_query_dataset_csv(id: str, data=None) -> Response:
    """
    Asynchronously query dataset CSV by ID.

    Args:
        id (str): Dataset ID
        data (Any): Data to POST

    Returns:
        Response: HTTP response object
    """
    request_info = _query_dataset_csv_request_info(id, data)
    return await __async_get_request(**request_info)
