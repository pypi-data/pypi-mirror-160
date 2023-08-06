"""
FRED API requests.
"""
from typing import Dict, Any

import pandas as pd
from pandas import DataFrame

from algoralabs.common.requests import __async_get_request, __get_request
from algoralabs.data.fred import FredQuery
from algoralabs.decorators.data import data_request, async_data_request


def _transform_fred_observations(data: Dict[str, Any]) -> DataFrame:
    return pd.DataFrame(data['observations'])


def _get_series_info(query: FredQuery) -> dict:
    return {
        "endpoint": "/series/observations",
        "url_key": "fred",
        "params": query.dict(exclude_none=True)
    }


@data_request(transformer=_transform_fred_observations)
def get_series(query: FredQuery) -> DataFrame:
    """
    Get FRED series.

    Args:
        query (FredQuery): FRED query

    Returns:
        DataFrame: DataFrame
    """
    request_info = _get_series_info(query)
    return __get_request(**request_info)


@async_data_request(transformer=_transform_fred_observations)
async def async_get_series(query: FredQuery) -> DataFrame:
    """
    Asynchronously get FRED series.

    Args:
        query (FredQuery): FRED query

    Returns:
        DataFrame: DataFrame
    """
    request_info = _get_series_info(query)
    return await __async_get_request(**request_info)
