"""
Document API requests.
"""
import json
from typing import List, Any, Dict

from algoralabs.common.functions import no_transform
from algoralabs.common.requests import (
    __get_request, __put_request, __post_request, __delete_request,
    __async_get_request, __async_put_request, __async_post_request, __async_delete_request
)
from algoralabs.decorators.data import data_request, async_data_request
from algoralabs.document import DocumentRequest, SearchDocumentRequest


def _get_document_request_info(id: str) -> dict:
    return {
        'endpoint': f"config/documents/{id}"
    }


@data_request(transformer=no_transform)
def get_document(id: str) -> Dict[str, Any]:
    """
    Get document by ID.

    Args:
        id: (str): Document ID

    Returns:
        Dict[str, Any]: Document response
    """
    request_info = _get_document_request_info(id)
    return __get_request(**request_info)


@async_data_request(transformer=no_transform)
async def async_get_document(id: str) -> Dict[str, Any]:
    """
    Asynchronously get document by ID.

    Args:
        id: (str): Document ID

    Returns:
        Dict[str, Any]: Document response
    """
    request_info = _get_document_request_info(id)
    return await __async_get_request(**request_info)


def _search_documents_request_info(request: SearchDocumentRequest) -> dict:
    return {
        'endpoint': "config/documents/search",
        'json': json.loads(request.json())
    }


@data_request(transformer=no_transform)
def search_documents(request: SearchDocumentRequest) -> List[Dict[str, Any]]:
    """
    Search all documents.

    Args:
        request: (SearchDocumentRequest): Document search request

    Returns:
        List[Dict[str, Any]]: List of document response
    """
    request_info = _search_documents_request_info(request)
    return __post_request(**request_info)


@async_data_request(transformer=no_transform)
async def async_search_documents(request: SearchDocumentRequest) -> List[Dict[str, Any]]:
    """
    Asynchronously search all documents.

    Args:
        request: (SearchDocumentRequest): Document search request

    Returns:
        List[Dict[str, Any]]: List of document response
    """
    request_info = _search_documents_request_info(request)
    return await __async_post_request(**request_info)


def _create_document_request_info(request: DocumentRequest) -> dict:
    return {
        'endpoint': "config/documents",
        'json': json.loads(request.json())
    }


@data_request(transformer=no_transform)
def create_document(request: DocumentRequest) -> Dict[str, Any]:
    """
    Create document.

    Args:
        request: (DocumentRequest): Document request

    Returns:
        Dict[str, Any]: Document response
    """
    request_info = _create_document_request_info(request)
    return __post_request(**request_info)


@async_data_request(transformer=no_transform)
async def async_create_document(request: DocumentRequest) -> Dict[str, Any]:
    """
    Asynchronously create document.

    Args:
        request: (DocumentRequest): Document request

    Returns:
        Dict[str, Any]: Document response
    """
    request_info = _create_document_request_info(request)
    return await __async_post_request(**request_info)


def _update_document_request_info(id: str, request: DocumentRequest) -> dict:
    return {
        'endpoint': f"config/documents/{id}",
        'json': json.loads(request.json())
    }


@data_request(transformer=no_transform)
def update_document(id: str, request: DocumentRequest) -> Dict[str, Any]:
    """
    Update document.

    Args:
        id (str): Document ID
        request: (DocumentRequest): Document request

    Returns:
        Dict[str, Any]: Document response
    """
    request_info = _update_document_request_info(id, request)
    return __put_request(**request_info)


@async_data_request(transformer=no_transform)
async def async_update_document(id: str, request: DocumentRequest) -> Dict[str, Any]:
    """
    Asynchronously update document.

    Args:
        id (str): Document ID
        request: (DocumentRequest): Document request

    Returns:
        Dict[str, Any]: Document response
    """
    request_info = _update_document_request_info(id, request)
    return await __async_put_request(**request_info)


def _delete_document_request_info(id: str) -> dict:
    return {
        'endpoint': f"config/documents/{id}"
    }


@data_request(transformer=no_transform)
def delete_document(id: str) -> None:
    """
    Delete document by ID.

    Args:
        id (str): Document ID

    Returns:
        None
    """
    request_info = _delete_document_request_info(id)
    return __delete_request(**request_info)


@async_data_request(transformer=no_transform)
async def async_delete_document(id: str) -> None:
    """
    Asynchronously delete document by ID.

    Args:
        id (str): Document ID

    Returns:
        None
    """
    request_info = _delete_document_request_info(id)
    return await __async_delete_request(**request_info)
