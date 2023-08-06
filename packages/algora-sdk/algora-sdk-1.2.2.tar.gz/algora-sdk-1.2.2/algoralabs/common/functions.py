"""
Helper functions.
"""
import calendar
import dataclasses
from datetime import datetime
from functools import reduce
from typing import Dict, Any, Union, List, Optional

import pandas as pd
from aiohttp import ClientResponse
from pandas import DataFrame
from requests import Response

from algoralabs.common.types import Datetime


def coalesce(*args):
    """
    Coalesce operator returns the first arg that isn't None.

    Args:
        *args: Tuple of args passed to the function

    Returns:
        The first non-None value in *args
    """
    return reduce(lambda x, y: x if x is not None else y, args)


def coalesce_callables(*args):
    """
    Coalesce operator returns the first arg that isn't None. If the arg is callable it will check that the value
    returned from calling the arg is not none and then return the value from calling it.

    WARNING: If an argument implements __call__ this method will evaluate the return of the __call__ method and return
    that instead of the argument itself. This is important when using python classes.

    Args:
        *args: Tuple of args passed to the function

    Returns:
        The first non-None value in *args
    """
    for arg in args:
        value = arg() if callable(arg) else arg
        if value is not None:
            return value
    return None


def dataclass_to_dict(data_cls: dataclasses.dataclass, remove_none: bool) -> dict:
    """
    Get all the dataclass fields (i.e. the key value pairs) and build a dict representation.

    Args:
        data_cls (dataclass): The dataclass being converted to json
        remove_none (bool): A flag used to remove key value pairs where the value is None from the json conversion

    Returns:
        dict: A dict representation of the dataclass
    """

    def factory(data):
        return dict(x for x in data if not (x[1] is None and remove_none))

    return dict(dataclasses.asdict(data_cls, dict_factory=factory))


def transform_one_or_many(
        data: Union[List[Dict[str, Any]], Dict[str, List[Dict[str, Any]]]],
        key: Optional[str] = None
) -> Union[DataFrame, Dict[str, DataFrame]]:
    """
    Converts data to a dataframe or multiple dataframes.

    Args:
        data (Union[List[Dict[str, Any]], Dict[str, List[Dict[str, Any]]]]): Dict being transformed into Dataframes
        key (Optional[str]): Key for indexing the values of the data dict

    Returns:
        Union[DataFrame, Dict[str, DataFrame]]: A single dataframe or a map of names to dataframes
    """
    if isinstance(data, dict):
        for k in data.keys():
            data[k] = DataFrame(data[k][key])
        return data

    return DataFrame(data)


def to_pandas_with_index(data: Dict[str, Any], index: str = 'date') -> DataFrame:
    """
    Transform input data into pandas dataframe and assign index.

    Args:
        data (Dict[str, Any]): Input data as dict
        index (str): Index column name

    Returns:
        DataFrame: DataFrame
    """
    # necessary to drop column in order to avoid duplicates when converting to json
    return pd.DataFrame(data).set_index(index, drop=True)


def no_transform(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Passthrough data without any transformation.

    Args:
        data (Dict[str, Any]): Input data

    Returns:
        Dict[str, Any]: Output data
    """
    return data


def timestamp_to_datetime(timestamp: int) -> datetime:
    """
    Transform epoch timestamp in milliseconds to datetime.

    Args:
        timestamp (int): Epoch timestamp in milliseconds

    Returns:
        datetime: Datetime object
    """
    return datetime.fromtimestamp(timestamp / 1000)


def date_to_timestamp(date: Datetime) -> int:
    """
    Datetime to epoch timestamp in milliseconds.

    Args:
        date (Datetime): Datetime

    Returns:
        int: Epoch timestamp in milliseconds
    """
    return calendar.timegm(date.timetuple()) * 1000


async def _build_response_obj(aio_response: ClientResponse) -> Response:
    """
    Construct a requests Response object from an aiohttp Client Response object

    Args:
        aio_response (ClientResponse): Response object from aiohttp

    Returns:
        Response: A requests Response object
    """
    content = await aio_response.content.read()

    response = Response()
    response._content = content
    response.url = str(aio_response.url)
    response.status_code = aio_response.status
    headers = {row[0]: row[1] for row in aio_response.headers.items()}
    response.headers = headers
    return response
