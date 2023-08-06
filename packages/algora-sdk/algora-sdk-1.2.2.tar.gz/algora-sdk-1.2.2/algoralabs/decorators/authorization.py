"""
Authorization decorators.
"""
import functools
import json
import logging
from typing import Any, Callable, Optional

import aiohttp
import requests
from aiocache.decorators import cached as aiocached
from cachetools import cached, TTLCache
from requests import Response

from algoralabs.common.config import EnvironmentConfig
from algoralabs.common.errors import AuthenticationError
from algoralabs.common.functions import _build_response_obj

logger = logging.getLogger(__name__)


# TODO: Figure out max size
@cached(cache=TTLCache(maxsize=100, ttl=1740))
def authenticate(
        base_url: Optional[str],
        username: Optional[str],
        password: Optional[str],
        access_token: Optional[str],
        refresh_token: Optional[str]
) -> dict:
    """
    Authenticate user and create user authentication headers.

    Args:
        base_url (Optional[str]): Base request URL
        username (Optional[str]): Algora username
        password (Optional[str]): Algora password
        access_token (Optional[str]): Algora access token
        refresh_token (Optional[str]): Algora refresh token

    Returns:
        dict: Auth headers for a request
    """
    auth_headers = {}
    if username and password:
        auth_headers = _sign_in(
            base_url=base_url,
            username=username,
            password=password
        )
    elif access_token:
        auth_headers = _access_token(access_token)
    elif refresh_token:
        auth_headers = _refresh_token(base_url, refresh_token)
    return auth_headers


@aiocached(ttl=1740)
async def async_authenticate(
        base_url: Optional[str],
        username: Optional[str],
        password: Optional[str],
        access_token: Optional[str],
        refresh_token: Optional[str]
) -> dict:
    """
    Asynchronously authenticate user and create user authentication headers.

    Args:
        base_url (Optional[str]): Base request URL
        username (Optional[str]): Algora username
        password (Optional[str]): Algora password
        access_token (Optional[str]): Algora access token
        refresh_token (Optional[str]): Algora refresh token

    Returns:
        dict: Auth headers for a request
    """
    auth_headers = {}
    if username and password:
        auth_headers = await _async_sign_in(
            base_url=base_url,
            username=username,
            password=password
        )
    elif access_token:
        auth_headers = _access_token(access_token)
    elif refresh_token:
        auth_headers = _refresh_token(base_url, refresh_token)
    return auth_headers


def _handle_auth_response(auth_response: Response, error_msg: str) -> dict:
    if auth_response.status_code == 200:
        bearer_token = auth_response.json()['access_token']
        return {'Authorization': f'Bearer {bearer_token}'}
    else:
        error = AuthenticationError(error_msg)
        logger.error(error)
        raise error


def _sign_in_request_info(base_url: str, username: str, password: str):
    return {
        'url': f"{base_url}/login",
        'data': json.dumps({"username": username, "password": password}),
        'headers': {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
    }


def _sign_in(base_url: str, username: str, password: str) -> dict:
    request_info = _sign_in_request_info(base_url, username, password)
    auth_response = requests.post(**request_info)
    return _handle_auth_response(auth_response, error_msg="Failed to sign-in the user")


async def _async_sign_in(base_url: str, username: str, password: str) -> dict:
    request_info = _sign_in_request_info(base_url, username, password)
    async with aiohttp.ClientSession() as session:
        async with session.post(**request_info) as response:
            auth_response = await _build_response_obj(response)
    return _handle_auth_response(auth_response, error_msg="Failed to sign-in the user")


def _refresh_token_request_info(base_url: str, refresh_token: Optional[str] = None) -> dict:
    return {
        'url': f"{base_url}/refresh_token",
        'data': json.dumps({"refresh_token": refresh_token}),
        'headers': {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
    }


def _refresh_token(base_url: str, refresh_token: Optional[str] = None) -> dict:
    request_info = _refresh_token_request_info(base_url, refresh_token)
    auth_response = requests.post(**request_info)
    return _handle_auth_response(auth_response, error_msg="Failed to refresh the user's token")


async def _async_refresh_token(base_url: str, refresh_token: Optional[str] = None) -> dict:
    request_info = _refresh_token_request_info(base_url, refresh_token)
    async with aiohttp.ClientSession() as session:
        async with session.post(**request_info) as response:
            auth_response = await _build_response_obj(response)
    return _handle_auth_response(auth_response, error_msg="Failed to refresh the user's token")


def _access_token(access_token: str) -> dict:
    return json.loads(access_token)


def _validate_headers(**kwargs):
    headers = kwargs.get("headers", {})

    if headers.get("Authorization") is None:
        error = AuthenticationError("Authentication for the package was configured incorrectly and is either "
                                    "missing a ALGORA_ACCESS_TOKEN or ALGORA_REFRESH_TOKEN or ALGORA_USER and "
                                    "ALGORA_PWD environment variable(s)")
        logger.error(error)
        # TODO this fails when using FRED API (outside of Algora API, so it doesn't need Authorization header)
        #  raise error


def _make_request(func: Callable, config: EnvironmentConfig, *args, **kwargs) -> Response:
    _validate_headers(**kwargs)

    response: Response = func(*args, **kwargs)
    if response.status_code == 401 and config.auth_config.refresh_token:
        auth_headers = _refresh_token(config.get_url(), config.auth_config.refresh_token)
        kwargs['headers'].update(auth_headers)  # override authentication header
        response: Response = func(*args, **kwargs)

    return response


async def _async_make_request(func, config: EnvironmentConfig, *args, **kwargs) -> Response:
    _validate_headers(**kwargs)

    response: Response = await func(*args, **kwargs)
    if response.status_code == 401 and config.auth_config.refresh_token:
        auth_headers = await _async_refresh_token(config.get_url(), config.auth_config.refresh_token)
        kwargs['headers'].update(auth_headers)  # override authentication header
        response: Response = await func(*args, **kwargs)

    return response


def authenticated_request(
        request: Callable = None,
        *,
        env_config: Optional[EnvironmentConfig] = None
) -> Callable:
    """
    Decorator for requests that need to be authenticated

    Args:
          request (Callable): Method that needs auth headers injected
          env_config (Optional[EnvironmentConfig]): Optional environment config
    Returns:
        Callable: Wrapped function
    """

    @functools.wraps(request)
    def decorator(f):
        @functools.wraps(f)
        def wrap(*args, **kwargs) -> Any:
            """
            Wrapper for the decorated function

            Args:
                *args: args for the function
                **kwargs: keyword args for the function

            Returns:
                Any: The output of the wrapped function
            """
            config = env_config if env_config is not None else EnvironmentConfig()
            headers = kwargs.get("headers", {})

            if config.auth_config.can_authenticate():
                auth_headers = authenticate(
                    base_url=config.get_url(),
                    username=config.auth_config.username,
                    password=config.auth_config.password,
                    access_token=config.auth_config.access_token,
                    refresh_token=config.auth_config.refresh_token
                )
                auth_headers.update(headers)  # override authentication header if already provided
                kwargs["headers"] = auth_headers

            return _make_request(f, config, *args, **kwargs)

        return wrap

    if request is None:
        return decorator
    return decorator(request)


def async_authenticated_request(
        request: Callable = None,
        *,
        env_config: Optional[EnvironmentConfig] = None
) -> Callable:
    """
    Decorator for requests that need to be authenticated

    Args:
          request (Callable): Method that needs auth headers injected
          env_config (Optional[EnvironmentConfig]): Optional environment config
    Returns:
        Callable: Wrapped function
    """

    @functools.wraps(request)
    def decorator(f):
        @functools.wraps(f)
        async def wrap(*args, **kwargs) -> Any:
            """
            Wrapper for the decorated function

            Args:
                *args: args for the function
                **kwargs: keyword args for the function

            Returns:
                Any: The output of the wrapped function
            """
            config = env_config if env_config is not None else EnvironmentConfig()
            headers = kwargs.get("headers", {})

            if config.auth_config.can_authenticate():
                auth_headers = await async_authenticate(
                    base_url=config.get_url(),
                    username=config.auth_config.username,
                    password=config.auth_config.password,
                    access_token=config.auth_config.access_token,
                    refresh_token=config.auth_config.refresh_token
                )
                auth_headers.update(headers)  # override authentication header if already provided
                kwargs["headers"] = auth_headers

            return await _async_make_request(f, config, *args, **kwargs)

        return wrap

    if request is None:
        return decorator
    return decorator(request)
