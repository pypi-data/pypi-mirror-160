from typing import Union

import pandas as pd

from .exceptions import UserTypeError, UserValueError


def validate_series_has_time_index(data: pd.Series):
    """Helper method to validate if provided pandas.Series is of type pandas.DatetimeIndex."""
    if not isinstance(data.index, pd.DatetimeIndex):
        raise UserTypeError(f"Expected a time series, got index type {data.index.dtype}")


def validate_series_is_not_empty(series: Union[pd.Series, pd.DataFrame]):
    """Helper method to validate if provided pandas.Series has more than 0 values."""
    if len(series) == 0:
        raise UserValueError("Time series is empty.")


def validate_series_has_minimum_length(series: pd.Series, min_len: int):
    """Helper method to validate if provided pandas.Series has the minimum length specified."""
    if len(series) < min_len:
        raise UserValueError(f"Expected series with length >= {min_len}, got length {len(series)}")


def validate_timedelta_unit(timedelta: pd.Timedelta):
    """Helper method to validate if the provided pd.Timedelta is larger or equal to 1 second."""
    if timedelta < pd.Timedelta(seconds=1):
        raise UserValueError("Unit of timedelta should be in days, hours, minutes or seconds")


def validate_series_not_uniform_values(data: pd.Series):
    """Helper method to validate that the data is not uniform."""
    if (data == data[0]).all():
        raise UserValueError("Time series is uniform.")
