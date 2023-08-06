"""
Keycloak API requests.
"""
from typing import List, Dict

from algoralabs.common.functions import no_transform
from algoralabs.common.requests import (
    __get_request, __put_request, __post_request, __delete_request,
    __async_get_request, __async_put_request, __async_post_request, __async_delete_request
)
from algoralabs.decorators.data import data_request, async_data_request


def _get_client_id_args() -> dict:
    return {
        "endpoint": "clients?clientId=realm-management",
        "url_key": "keycloak"
    }


@data_request(transformer=no_transform)
def get_client_id():
    """
    Get keycloak client ID.

    Returns:
        Keycloak client ID.
    """
    request_info = _get_client_id_args()
    return __get_request(**request_info)


@async_data_request(transformer=no_transform)
async def async_get_client_id():
    """
    Asynchronously get keycloak client ID.

    Returns:
        Keycloak client ID.
    """
    request_info = _get_client_id_args()
    return await __async_get_request(**request_info)


def _get_users_request_info() -> dict:
    return {
        "endpoint": "users",
        "params": {"max": 500},
        "url_key": "keycloak"
    }


@data_request
def get_users():
    """
    Get all users.

    Returns:
        List of user response.
    """
    request_info = _get_users_request_info()
    return __get_request(**request_info)


@async_data_request
async def async_get_users():
    """
    Asynchronously get all users.

    Returns:
        List of user response.
    """
    request_info = _get_users_request_info()
    return await __async_get_request(**request_info)


def _get_user_request_info(user_id: str) -> dict:
    return {
        "endpoint": f"users/{user_id}",
        "url_key": "keycloak"
    }


@data_request(transformer=no_transform)
def get_user(user_id: str):
    """
    Get user by ID.

    Args:
        user_id (str): User ID

    Returns:
        User response
    """
    request_info = _get_user_request_info(user_id)
    return __get_request(**request_info)


@async_data_request(transformer=no_transform)
async def async_get_user(user_id: str):
    """
    Asynchronously get user by ID.

    Args:
        user_id (str): User ID

    Returns:
        User response
    """
    request_info = _get_user_request_info(user_id)
    return await __async_get_request(**request_info)


def _update_user_request_info(user_id: str, data: dict) -> dict:
    return {
        "endpoint": f"users/{user_id}",
        "url_key": "keycloak",
        "json": data
    }


@data_request(transformer=no_transform, processor=lambda r: r)
def update_user(user_id: str, data: dict):
    """
    Update user.

    Args:
        user_id (str): User ID
        data (dict): User request

    Returns:
        User response
    """
    request_info = _update_user_request_info(user_id, data)
    return __put_request(**request_info)


@async_data_request(transformer=no_transform, processor=lambda r: r)
async def async_update_user(user_id: str, data: dict):
    """
    Asynchronously update user.

    Args:
        user_id (str): User ID
        data (dict): User request

    Returns:
        User response
    """
    request_info = _update_user_request_info(user_id, data)
    return await __async_put_request(**request_info)


def _get_groups_request_info() -> dict:
    return {
        "endpoint": "groups",
        "url_key": "keycloak"
    }


@data_request(transformer=no_transform)
def get_groups():
    """
    Get groups.

    Returns:
        List of groups.
    """
    request_info = _get_groups_request_info()
    return __get_request(**request_info)


@async_data_request(transformer=no_transform)
async def async_get_groups():
    """
    Asynchronously get groups.

    Returns:
        List of groups.
    """
    request_info = _get_groups_request_info()
    return await __async_get_request(**request_info)


def _get_group_members_request_info(id: str) -> dict:
    return {
        "endpoint": f"groups/{id}/members",
        "url_key": "keycloak"
    }


@data_request(transformer=no_transform)
def get_group_members(id: str):
    """
    Get group members given group ID.

    Args:
        id (str): Group ID

    Returns:
        List of user response
    """
    request_info = _get_group_members_request_info(id)
    return __get_request(**request_info)


@async_data_request(transformer=no_transform)
async def async_get_group_members(id: str):
    """
    Asynchronously get group members given group ID.

    Args:
        id (str): Group ID

    Returns:
        List of user response
    """
    request_info = _get_group_members_request_info(id)
    return await __async_get_request(**request_info)


def _add_group_to_user_request_info(user_id: str, group_id: str) -> dict:
    return {
        "endpoint": f"users/{user_id}/groups/{group_id}",
        "url_key": "keycloak"
    }


@data_request(transformer=no_transform, processor=lambda r: r)
def add_group_to_user(user_id: str, group_id: str):
    """
    Add user to group.

    Args:
        user_id (str): User ID
        group_id (str): Group ID

    Returns:
        None
    """
    request_info = _add_group_to_user_request_info(user_id, group_id)
    return __put_request(**request_info)


@async_data_request(transformer=no_transform, processor=lambda r: r)
async def async_add_group_to_user(user_id: str, group_id: str):
    """
    Asynchronously add user to group.

    Args:
        user_id (str): User ID
        group_id (str): Group ID

    Returns:
        None
    """
    request_info = _add_group_to_user_request_info(user_id, group_id)
    return await __async_put_request(**request_info)


def _delete_group_from_user_request_info(user_id: str, group_id: str) -> dict:
    return {
        "endpoint": f"users/{user_id}/groups/{group_id}",
        "url_key": "keycloak"
    }


@data_request(transformer=no_transform, processor=lambda r: r)
def delete_group_from_user(user_id: str, group_id: str):
    """
    Delete user from group.

    Args:
        user_id (str): User ID
        group_id (str): Group ID

    Returns:
        None
    """
    request_info = _delete_group_from_user_request_info(user_id, group_id)
    return __delete_request(**request_info)


@async_data_request(transformer=no_transform, processor=lambda r: r)
async def async_delete_group_from_user(user_id: str, group_id: str):
    """
    Asynchronously delete user from group.

    Args:
        user_id (str): User ID
        group_id (str): Group ID

    Returns:
        None
    """
    request_info = _delete_group_from_user_request_info(user_id, group_id)
    return await __async_delete_request(**request_info)


def _get_roles_request_info() -> dict:
    return {
        "endpoint": "roles",
        "url_key": "keycloak"
    }


@data_request(transformer=no_transform)
def get_roles():
    """
    Get roles.

    Returns:
        List of role response.
    """
    request_info = _get_roles_request_info()
    return __get_request(**request_info)


@async_data_request(transformer=no_transform)
async def async_get_roles():
    """
    Asynchronously get roles.

    Returns:
        List of role response.
    """
    request_info = _get_roles_request_info()
    return await __async_get_request(**request_info)


def _get_roles_for_user_request_info(user_id: str) -> dict:
    return {
        "endpoint": f"users/{user_id}/role-mappings",
        "url_key": "keycloak"
    }


@data_request(transformer=no_transform)
def get_roles_for_user(user_id: str):
    """
    Get roles for user.

    Args:
        user_id (str): User ID

    Returns:
        List of role response
    """
    request_info = _get_roles_for_user_request_info(user_id)
    return __get_request(**request_info)


@async_data_request(transformer=no_transform)
async def async_get_roles_for_user(user_id: str):
    """
    Asynchronously get roles for user.

    Args:
        user_id (str): User ID

    Returns:
        List of role response
    """
    request_info = _get_roles_for_user_request_info(user_id)
    return await __async_get_request(**request_info)


def _add_role_mapping_to_user_request_info(user_id: str, role_ids: List[Dict[str, str]]) -> dict:
    return {
        "endpoint": f"users/{user_id}/role-mappings/realm",
        "url_key": "keycloak",
        "json": role_ids
    }


@data_request(transformer=no_transform, processor=lambda r: r)
def add_role_mapping_to_user(user_id: str, role_ids: List[Dict[str, str]]):
    """
    Add role mapping to user.

    Args:
        user_id (str): User ID
        role_ids (List[Dict[str, str]]): List of role ID mapping

    Returns:
        None
    """
    request_info = _add_role_mapping_to_user_request_info(user_id, role_ids)
    return __post_request(**request_info)


@async_data_request(transformer=no_transform, processor=lambda r: r)
async def async_add_role_mapping_to_user(user_id: str, role_ids: List[Dict[str, str]]):
    """
    Asynchronously add role mapping to user.

    Args:
        user_id (str): User ID
        role_ids (List[Dict[str, str]]): List of role ID mapping

    Returns:
        None
    """
    request_info = _add_role_mapping_to_user_request_info(user_id, role_ids)
    return await __async_post_request(**request_info)
