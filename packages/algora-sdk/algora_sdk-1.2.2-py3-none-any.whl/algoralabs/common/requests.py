"""
Common request methods.
"""
from typing import Optional

import aiohttp
import requests
from requests import Response

from algoralabs.common.config import EnvironmentConfig
from algoralabs.common.functions import _build_response_obj
from algoralabs.decorators.authorization import authenticated_request, async_authenticated_request

config = EnvironmentConfig()


@authenticated_request
def __get_request(
        endpoint: str,
        url_key: str = "algora",
        headers: Optional[dict] = None,
        params: Optional[dict] = None,
        timeout: int = 30
) -> Response:
    """
    Wrapper method for get requests.

    Args:
        endpoint (str): API endpoint
        url_key (str): Key for looking up the url from the environment config
        headers (Optional[dict]): Headers for the API request
        params (Optional[dict]): Params for the API request
        timeout (int): Timeout for API request

    Returns:
        Response: HTTP response object
    """
    return requests.get(
        url=f"{config.get_url(url_key)}/{endpoint}",
        headers=headers or {},
        params=params,
        timeout=timeout
    )


@async_authenticated_request
async def __async_get_request(
        endpoint: str,
        url_key: str = "algora",
        headers: Optional[dict] = None,
        params: Optional[dict] = None,
        timeout: int = 30
) -> Response:
    """
    Wrapper method for asynchronous get requests.

    Args:
        endpoint (str): API endpoint
        url_key (str): Key for looking up the url from the environment config
        headers (Optional[dict]): Headers for the API request
        params (Optional[dict]): Params for the API request
        timeout (int): Timeout for API request

    Returns:
        Response: HTTP response object
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(
                url=f"{config.get_url(url_key)}/{endpoint}",
                headers=headers or {},
                params=params,
                timeout=timeout
        ) as response:
            result = await _build_response_obj(response)

    return result


@authenticated_request
def __put_request(
        endpoint: str,
        url_key: str = "algora",
        data=None,
        json=None,
        files=None,
        headers: Optional[dict] = None,
        params: Optional[dict] = None,
        timeout: int = 30
) -> Response:
    """
    Wrapper method for put requests.

    Args:
        endpoint (str): API endpoint
        url_key (str): Key for looking up the url from the environment config
        data (Any): Data passed to the API
        json (Any): JSON passed to the API
        files (Any): Files passed to the API
        headers (Optional[dict]): Headers for the API request
        params (Optional[dict]): Params for the API request
        timeout (int): Timeout for API request

    Returns:
        Response: HTTP response object
    """
    return requests.put(
        url=f"{config.get_url(url_key)}/{endpoint}",
        data=data,
        json=json,
        files=files,
        headers=headers or {},
        params=params,
        timeout=timeout
    )


@async_authenticated_request
async def __async_put_request(
        endpoint: str,
        url_key: str = "algora",
        data=None,
        json=None,
        files=None,
        headers: Optional[dict] = None,
        params: Optional[dict] = None,
        timeout: int = 30
) -> Response:
    """
    Wrapper method for asynchronous put requests.

    Args:
        endpoint (str): API endpoint
        url_key (str): Key for looking up the url from the environment config
        data (Any): Data passed to the API
        json (Any): JSON passed to the API
        files (Any): Files passed to the API
        headers (Optional[dict]): Headers for the API request
        params (Optional[dict]): Params for the API request
        timeout (int): Timeout for API request

    Returns:
        Response: HTTP response object
    """
    data = data if data is None else data.update({"files": files})
    async with aiohttp.ClientSession() as session:
        async with session.put(
                url=f"{config.get_url(url_key)}/{endpoint}",
                data=data,
                json=json,
                headers=headers or {},
                params=params,
                timeout=timeout
        ) as response:
            result = await _build_response_obj(response)

    return result


@authenticated_request
def __post_request(
        endpoint: str,
        url_key: str = "algora",
        files=None,
        data=None,
        json=None,
        headers: Optional[dict] = None,
        params: Optional[dict] = None,
        timeout: int = 30
) -> Response:
    """
    Wrapper method for post requests.

    Args:
        endpoint (str): API endpoint
        url_key (str): Key for looking up the url from the environment config
        data (Any): Data passed to the API
        json (Any): JSON passed to the API
        files (Any): Files passed to the API
        headers (Optional[dict]): Headers for the API request
        params (Optional[dict]): Params for the API request
        timeout (int): Timeout for API request

    Returns:
        Response: HTTP response object
    """
    return requests.post(
        url=f"{config.get_url(url_key)}/{endpoint}",
        files=files,
        data=data,
        json=json,
        headers=headers or {},
        params=params,
        timeout=timeout
    )


@async_authenticated_request
async def __async_post_request(
        endpoint: str,
        url_key: str = "algora",
        files=None,
        data=None,
        json=None,
        headers: Optional[dict] = None,
        params: Optional[dict] = None,
        timeout: int = 30
) -> Response:
    """
    Wrapper method for asynchronous post requests.

    Args:
        endpoint (str): API endpoint
        url_key (str): Key for looking up the url from the environment config
        data (Any): Data passed to the API
        json (Any): JSON passed to the API
        files (Any): Files passed to the API
        headers (Optional[dict]): Headers for the API request
        params (Optional[dict]): Params for the API request
        timeout (int): Timeout for API request

    Returns:
        Response: HTTP response object
    """
    data = data if data is None else data.update({"files": files})
    async with aiohttp.ClientSession() as session:
        async with session.post(
                url=f"{config.get_url(url_key)}/{endpoint}",
                data=data,
                json=json,
                headers=headers or {},
                params=params,
                timeout=timeout
        ) as response:
            result = await _build_response_obj(response)

    return result


@authenticated_request
def __delete_request(
        endpoint: str,
        url_key: str = "algora",
        headers: Optional[dict] = None,
        params: Optional[dict] = None,
        timeout: int = 30
) -> Response:
    """
    Wrapper method for delete requests.

    Args:
        endpoint (str): API endpoint
        url_key (str): Key for looking up the url from the environment config
        headers (Optional[dict]): Headers for the API request
        params (Optional[dict]): Params for the API request
        timeout (int): Timeout for API request

    Returns:
        Response: HTTP response object
    """
    return requests.delete(
        url=f"{config.get_url(url_key)}/{endpoint}",
        headers=headers or {},
        params=params,
        timeout=timeout
    )


@async_authenticated_request
async def __async_delete_request(
        endpoint: str,
        url_key: str = "algora",
        headers: Optional[dict] = None,
        params: Optional[dict] = None,
        timeout: int = 30
) -> Response:
    """
    Wrapper method for asynchronous delete requests.

    Args:
        endpoint (str): API endpoint
        url_key (str): Key for looking up the url from the environment config
        headers (Optional[dict]): Headers for the API request
        params (Optional[dict]): Params for the API request
        timeout (int): Timeout for API request

    Returns:
        Response: HTTP response object
    """
    async with aiohttp.ClientSession() as session:
        async with session.delete(
                url=f"{config.get_url(url_key)}/{endpoint}",
                headers=headers or {},
                params=params,
                timeout=timeout
        ) as response:
            result = await _build_response_obj(response)

    return result
