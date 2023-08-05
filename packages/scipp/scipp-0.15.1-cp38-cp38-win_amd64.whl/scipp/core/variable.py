# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2022 Scipp contributors (https://github.com/scipp)
# @author Matthew Andrew
# flake8: noqa: E501

from __future__ import annotations

from contextlib import contextmanager
from typing import Any, Iterable, Optional, Sequence, TypeVar, Union
import warnings

import numpy as _np
from numpy.typing import ArrayLike

from .._scipp import core as _cpp
from .cpp_classes import DType, Unit, Variable
from ..units import default_unit
from ._sizes import _parse_dims_shape_sizes
from ..typing import DTypeLike

NumberOrVar = TypeVar('NumberOrVar', Union[int, float], Variable)


def scalar(value: Any,
           *,
           variance: Any = None,
           unit: Union[Unit, str, None] = default_unit,
           dtype: Optional[DTypeLike] = None) -> Variable:
    """Constructs a zero dimensional :class:`Variable` with a unit and optional
    variance.

    Parameters
    ----------
    value:
        Initial value.
    variance:
        Optional, initial variance.
    unit:
        Optional, unit.
    dtype: scipp.typing.DTypeLike
        Optional, type of underlying data. By default,
        the dtype is inferred from the `value` argument.
        Cannot be specified for value types of
        Dataset or DataArray.

    Returns
    -------
    :
        A scalar (zero-dimensional) Variable.

    See Also
    --------
    scipp.array, scipp.empty, scipp.index, scipp.ones, scipp.zeros

    Examples
    --------
    With deduced dtype and default unit:

      >>> sc.scalar(3.14)
      <scipp.Variable> ()    float64  [dimensionless]  [3.14]

      >>> sc.scalar('a string')
      <scipp.Variable> ()     string           <no unit>  ["a string"]

    Or specifying a unit and dtype:

      >>> sc.scalar(3.14, unit='m', dtype=int)
      <scipp.Variable> ()      int64              [m]  [3]

    Calling ``scalar`` with a list (or similar array-like object) will store that
    object in a scalar variable and *not* create an array variable:

      >>> sc.scalar([1, 2, 3])
      <scipp.Variable> ()   PyObject           <no unit>  [[1, 2, 3]]
    """
    return _cpp.Variable(dims=(),
                         values=value,
                         variances=variance,
                         unit=unit,
                         dtype=dtype)


def index(value: Any, *, dtype: Optional[DTypeLike] = None) -> Variable:
    """Constructs a zero dimensional :class:`Variable` representing an index.

    This is equivalent to calling :py:func:`scipp.scalar` with unit=None.

    Parameters
    ----------
    value:
        Initial value.
    dtype: scipp.typing.DTypeLike
        Optional, type of underlying data. By default,
        the dtype is inferred from the `value` argument.

    Returns
    -------
    :
        A scalar (zero-dimensional) variable without unit.

    See Also
    --------
    scipp.scalar, scipp.array

    Examples
    --------

      >>> sc.index(123)
      <scipp.Variable> ()      int64           <no unit>  [123]
    """
    return scalar(value=value, dtype=dtype, unit=None)


def zeros(*,
          dims: Sequence[str] = None,
          shape: Sequence[int] = None,
          sizes: dict = None,
          unit: Union[Unit, str, None] = default_unit,
          dtype: DTypeLike = DType.float64,
          with_variances: bool = False) -> Variable:
    """Constructs a :class:`Variable` with default initialized values with
    given dimension labels and shape.

    The dims and shape can also be specified using a `sizes` dict.
    Optionally can add default initialized variances.
    Only keyword arguments accepted.

    Parameters
    ----------
    dims:
        Optional (if sizes is specified), dimension labels.
    shape:
        Optional (if sizes is specified), dimension sizes.
    sizes:
        Optional, dimension label to size map.
    unit:
        Unit of contents.
    dtype: scipp.typing.DTypeLike
        Type of underlying data.
    with_variances:
        If True includes variances initialized to 0.

    See Also
    --------
    scipp.array, scipp.empty, scipp.ones, scipp.scalar, scipp.zeros_like

    Examples
    --------

      >>> sc.zeros(dims=['x'], shape=[4])
      <scipp.Variable> (x: 4)    float64  [dimensionless]  [0, 0, 0, 0]

      >>> sc.zeros(sizes={'x': 4})
      <scipp.Variable> (x: 4)    float64  [dimensionless]  [0, 0, 0, 0]

      >>> sc.zeros(sizes={'y': 3}, with_variances=True)
      <scipp.Variable> (y: 3)    float64  [dimensionless]  [0, 0, 0]  [0, 0, 0]

      >>> sc.zeros(sizes={'z': 3}, unit='kg', dtype=int)
      <scipp.Variable> (z: 3)      int64             [kg]  [0, 0, 0]
    """

    return _cpp.zeros(**_parse_dims_shape_sizes(dims, shape, sizes),
                      unit=unit,
                      dtype=dtype,
                      with_variances=with_variances)


def ones(*,
         dims: Sequence[str] = None,
         shape: Sequence[int] = None,
         sizes: dict = None,
         unit: Union[Unit, str, None] = default_unit,
         dtype: DTypeLike = DType.float64,
         with_variances: bool = False) -> Variable:
    """Constructs a :class:`Variable` with values initialized to 1 with
    given dimension labels and shape.

    The dims and shape can also be specified using a `sizes` dict.

    Parameters
    ----------
    dims:
        Optional (if sizes is specified), dimension labels.
    shape:
        Optional (if sizes is specified), dimension sizes.
    sizes:
        Optional, dimension label to size map.
    unit:
        Unit of contents.
    dtype: scipp.typing.DTypeLike
        Type of underlying data.
    with_variances:
        If True includes variances initialized to 1.

    See Also
    --------
    scipp.array, scipp.empty, scipp.ones_like, scipp.scalar, scipp.zeros

    Examples
    --------

      >>> sc.ones(dims=['x'], shape=[4])
      <scipp.Variable> (x: 4)    float64  [dimensionless]  [1, 1, 1, 1]

      >>> sc.ones(sizes={'x': 4})
      <scipp.Variable> (x: 4)    float64  [dimensionless]  [1, 1, 1, 1]

      >>> sc.ones(sizes={'y': 3}, with_variances=True)
      <scipp.Variable> (y: 3)    float64  [dimensionless]  [1, 1, 1]  [1, 1, 1]

      >>> sc.ones(sizes={'z': 3}, unit='kg', dtype=int)
      <scipp.Variable> (z: 3)      int64             [kg]  [1, 1, 1]
    """
    return _cpp.ones(**_parse_dims_shape_sizes(dims, shape, sizes),
                     unit=unit,
                     dtype=dtype,
                     with_variances=with_variances)


def empty(*,
          dims: Sequence[str] = None,
          shape: Sequence[int] = None,
          sizes: dict = None,
          unit: Union[Unit, str, None] = default_unit,
          dtype: DTypeLike = DType.float64,
          with_variances: bool = False) -> Variable:
    """Constructs a :class:`Variable` with uninitialized values with given
    dimension labels and shape.

    The dims and shape can also be specified using a `sizes` dict.

    Warning
    -------
    'Uninitialized' means that values have undetermined values.
    Reading elements before writing to them is undefined behavior.
    Consider using :py:func:`scipp.zeros` unless you
    know what you are doing and require maximum performance.

    Parameters
    ----------
    dims:
        Optional (if sizes is specified), dimension labels.
    shape:
        Optional (if sizes is specified), dimension sizes.
    sizes:
        Optional, dimension label to size map.
    unit:
        Unit of contents.
    dtype: scipp.typing.DTypeLike
        Type of underlying data.
    with_variances:
        If True includes uninitialized variances.

    See Also
    --------
    scipp.array, scipp.empty_like, scipp.ones, scipp.scalar, scipp.zeros

    Examples
    --------

      >>> var = sc.empty(dims=['x'], shape=[4])
      >>> var[:] = sc.scalar(2.0)  # initialize values before printing
      >>> var
      <scipp.Variable> (x: 4)    float64  [dimensionless]  [2, 2, 2, 2]
    """
    return _cpp.empty(**_parse_dims_shape_sizes(dims, shape, sizes),
                      unit=unit,
                      dtype=dtype,
                      with_variances=with_variances)


def full(*,
         value: Any,
         variance: Any = None,
         dims: Sequence[str] = None,
         shape: Sequence[int] = None,
         sizes: dict = None,
         unit: Union[Unit, str, None] = default_unit,
         dtype: Optional[DTypeLike] = None) -> Variable:
    """Constructs a :class:`Variable` with values initialized to the specified
    value with given dimension labels and shape.

    The dims and shape can also be specified using a `sizes` dict.

    Parameters
    ----------
    value:
        The value to fill the Variable with.
    variance:
        The variance to fill the Variable with.
    dims:
        Optional (if sizes is specified), dimension labels.
    shape:
        Optional (if sizes is specified), dimension sizes.
    sizes:
        Optional, dimension label to size map.
    unit:
        Unit of contents.
    dtype: scipp.typing.DTypeLike
        Type of underlying data.

    See Also
    --------
    scipp.empty, scipp.full_like, scipp.ones, scipp.zeros

    Examples
    --------

      >>> sc.full(value=2, dims=['x'], shape=[2])
      <scipp.Variable> (x: 2)      int64  [dimensionless]  [2, 2]

      >>> sc.full(value=2, sizes={'x': 2})
      <scipp.Variable> (x: 2)      int64  [dimensionless]  [2, 2]

      >>> sc.full(value=5, sizes={'y': 3, 'x': 2})
      <scipp.Variable> (y: 3, x: 2)      int64  [dimensionless]  [5, 5, ..., 5, 5]

      >>> sc.full(value=2.0, variance=0.1, sizes={'x': 3}, unit='s')
      <scipp.Variable> (x: 3)    float64              [s]  [2, 2, 2]  [0.1, 0.1, 0.1]
    """
    return scalar(value=value, variance=variance, unit=unit, dtype=dtype)\
        .broadcast(**_parse_dims_shape_sizes(dims, shape, sizes)).copy()


def matrix(*,
           unit: Union[Unit, str, None] = default_unit,
           value: Union[_np.ndarray, list]) -> Variable:
    """Constructs a zero dimensional :class:`Variable` holding a single 3x3
    matrix.


    :param value: Initial value, a list or 1-D numpy array.
    :param unit: Optional, unit. Default=dimensionless
    :returns: A scalar (zero-dimensional) Variable.

    :seealso: :py:func:`scipp.matrices`
    """
    warnings.warn(
        "sc.matrix() has been deprecated in favour of "
        "sc.spatial.linear_transform(), and will be removed in a future "
        "version of scipp.", DeprecationWarning)
    from ..spatial import linear_transform
    return linear_transform(unit=unit, value=value)


def matrices(*,
             dims: Sequence[str],
             unit: Union[Unit, str, None] = default_unit,
             values: Union[_np.ndarray, list]) -> Variable:
    """Constructs a :class:`Variable` with given dimensions holding an array
    of 3x3 matrices.


    :param dims: Dimension labels.
    :param values: Initial values.
    :param unit: Optional, data unit. Default=dimensionless

    :seealso: :py:func:`scipp.matrix`
    """
    warnings.warn(
        "sc.matrices() has been deprecated in favour of "
        "sc.spatial.linear_transforms(), and will be removed in a future "
        "version of scipp.", DeprecationWarning)
    from ..spatial import linear_transforms
    return linear_transforms(dims=dims, unit=unit, values=values)


def vector(value: Union[_np.ndarray, list],
           *,
           unit: Union[Unit, str, None] = default_unit) -> Variable:
    """Constructs a zero dimensional :class:`Variable` holding a single length-3
    vector.

    Parameters
    ----------
    value:
        Initial value, a list or 1-D numpy array.
    unit:
        Unit of contents.

    Returns
    -------
    :
        A scalar (zero-dimensional) Variable.

    See Also
    --------
    scipp.vectors

    Examples
    --------

      >>> sc.vector(value=[1, 2, 3])
      <scipp.Variable> ()    vector3  [dimensionless]  [(1, 2, 3)]

      >>> sc.vector(value=[4, 5, 6], unit='m')
      <scipp.Variable> ()    vector3              [m]  [(4, 5, 6)]
    """
    return _cpp.vectors(dims=[], unit=unit, values=value)


def vectors(*,
            dims: Sequence[str],
            values: Union[_np.ndarray, list],
            unit: Union[Unit, str, None] = default_unit) -> Variable:
    """Constructs a :class:`Variable` with given dimensions holding an array
    of length-3 vectors.

    Parameters
    ----------
    dims:
        Dimension labels.
    values:
        Initial values.
    unit:
        Unit of contents.

    See Also
    --------
    scipp.vector

    Examples
    --------

      >>> sc.vectors(dims=['x'], values=[[1, 2, 3]])
      <scipp.Variable> (x: 1)    vector3  [dimensionless]  [(1, 2, 3)]

      >>> var = sc.vectors(dims=['x'], values=[[1, 2, 3], [4, 5, 6]])
      >>> var
      <scipp.Variable> (x: 2)    vector3  [dimensionless]  [(1, 2, 3), (4, 5, 6)]
      >>> var.values
      array([[1., 2., 3.],
             [4., 5., 6.]])

      >>> sc.vectors(dims=['x'], values=[[1, 2, 3], [4, 5, 6]], unit='mm')
      <scipp.Variable> (x: 2)    vector3             [mm]  [(1, 2, 3), (4, 5, 6)]
    """
    return _cpp.vectors(dims=dims, unit=unit, values=values)


def array(*,
          dims: Iterable[str],
          values: ArrayLike,
          variances: Optional[ArrayLike] = None,
          unit: Union[Unit, str, None] = default_unit,
          dtype: Optional[DTypeLike] = None) -> Variable:
    """Constructs a :class:`Variable` with given dimensions, containing given
    values and optional variances. Dimension and value shape must match.

    Only keyword arguments accepted.

    Parameters
    ----------
    dims:
        Dimension labels
    values: numpy.typing.ArrayLike
        Initial values.
    variances: numpy.typing.ArrayLike
        Initial variances, must be same shape and size as values.
    unit:
        Unit of contents.
    dtype: scipp.typing.DTypeLike
        Type of underlying data. By default, inferred from `values` argument.

    See Also
    --------
    scipp.empty, scipp.ones, scipp.scalar, scipp.zeros

    Examples
    --------

      >>> sc.array(dims=['x'], values=[1, 2, 3])
      <scipp.Variable> (x: 3)      int64  [dimensionless]  [1, 2, 3]

    Multiple dimensions:

      >>> sc.array(dims=['x', 'y'], values=[[1, 2, 3], [4, 5, 6]])
      <scipp.Variable> (x: 2, y: 3)      int64  [dimensionless]  [1, 2, ..., 5, 6]

    DType upcasting:

      >>> sc.array(dims=['x'], values=[1, 2, 3.0])
      <scipp.Variable> (x: 3)    float64  [dimensionless]  [1, 2, 3]

    Manually specified dtype:

      >>> sc.array(dims=['x'], values=[1, 2, 3], dtype=float)
      <scipp.Variable> (x: 3)    float64  [dimensionless]  [1, 2, 3]

    Set unit:

      >>> sc.array(dims=['x'], values=[1, 2, 3], unit='m')
      <scipp.Variable> (x: 3)      int64              [m]  [1, 2, 3]

    Setting variances:

      >>> sc.array(dims=['x'], values=[1.0, 2.0, 3.0], variances=[0.1, 0.2, 0.3])
      <scipp.Variable> (x: 3)    float64  [dimensionless]  [1, 2, 3]  [0.1, 0.2, 0.3]
    """
    return _cpp.Variable(dims=dims,
                         values=values,
                         variances=variances,
                         unit=unit,
                         dtype=dtype)


def _expect_no_variances(args):
    has_variances = [
        key for key, val in args.items()
        if val is not None and val.variances is not None
    ]
    if has_variances:
        raise _cpp.VariancesError('Arguments cannot have variances. '
                                  f'Passed variances in {has_variances}')


# Assumes that all arguments are Variable or None.
def _ensure_same_unit(*, unit, args: dict):
    if unit == default_unit:
        units = {key: val.unit for key, val in args.items() if val is not None}
        if len(set(units.values())) != 1:
            raise _cpp.UnitError(
                f'All units of the following arguments must be equal: {units}. '
                'You can specify a unit explicitly with the `unit` argument.')
        unit = next(iter(units.values()))
    return {
        key: _cpp.to_unit(val, unit, copy=False).value if val is not None else None
        for key, val in args.items()
    }, unit


# Process arguments of arange, linspace, etc and return them as plain numbers or None.
def _normalize_range_args(*, unit, **kwargs):
    is_var = {
        key: isinstance(val, _cpp.Variable)
        for key, val in kwargs.items() if val is not None
    }
    if any(is_var.values()):
        if not all(is_var.values()):
            arg_types = {key: type(val) for key, val in kwargs.items()}
            raise TypeError('Either all of the following arguments or none have to '
                            f'be variables: {arg_types}')
        _expect_no_variances(kwargs)
        return _ensure_same_unit(unit=unit, args=kwargs)
    return kwargs, unit


def linspace(dim: str,
             start: NumberOrVar,
             stop: NumberOrVar,
             num: int,
             *,
             endpoint: bool = True,
             unit: Union[Unit, str, None] = default_unit,
             dtype: Optional[DTypeLike] = None) -> Variable:
    """Constructs a :class:`Variable` with `num` evenly spaced samples,
    calculated over the interval `[start, stop]`.

    Parameters
    ----------
    dim:
        Dimension label.
    start:
        The starting value of the sequence.
    stop:
        The end value of the sequence.
    num:
        Number of samples to generate.
    endpoint:
        If True, `step` is the last returned value.
        Otherwise, it is not included.
    unit:
        Unit of contents.
    dtype: scipp.typing.DTypeLike
        Type of underlying data. By default, inferred from `value` argument.

    See Also
    --------
    scipp.arange, scipp.geomspace, scipp.logspace

    Examples
    --------

      >>> sc.linspace('x', 2.0, 4.0, num=4)
      <scipp.Variable> (x: 4)    float64  [dimensionless]  [2, 2.66667, 3.33333, 4]
      >>> sc.linspace('x', 2.0, 4.0, num=4, endpoint=False)
      <scipp.Variable> (x: 4)    float64  [dimensionless]  [2, 2.5, 3, 3.5]

      >>> sc.linspace('x', 1.5, 3.0, num=4, unit='m')
      <scipp.Variable> (x: 4)    float64              [m]  [1.5, 2, 2.5, 3]
    """
    range_args, unit = _normalize_range_args(unit=unit, start=start, stop=stop)
    return array(dims=[dim],
                 values=_np.linspace(**range_args, num=num, endpoint=endpoint),
                 unit=unit,
                 dtype=dtype)


def geomspace(dim: str,
              start: NumberOrVar,
              stop: NumberOrVar,
              num: int,
              *,
              endpoint: bool = True,
              unit: Union[Unit, str, None] = default_unit,
              dtype: Optional[DTypeLike] = None) -> Variable:
    """Constructs a :class:`Variable` with values spaced evenly on a log scale
    (a geometric progression).

    This is similar to :py:func:`scipp.logspace`, but with endpoints specified
    directly instead of as exponents.
    Each output sample is a constant multiple of the previous.

    Parameters
    ----------
    dim:
        Dimension label.
    start:
        The starting value of the sequence.
    stop:
        The end value of the sequence.
    num:
        Number of samples to generate.
    endpoint:
        If True, `step` is the last returned value.
        Otherwise, it is not included.
    unit:
        Unit of contents.
    dtype: scipp.typing.DTypeLike
        Type of underlying data. By default, inferred from `value` argument.

    See Also
    --------
    scipp.arange, scipp.linspace, scipp.logspace

    Examples
    --------

      >>> sc.geomspace('x', 1.0, 1000.0, num=4)
      <scipp.Variable> (x: 4)    float64  [dimensionless]  [1, 10, 100, 1000]
      >>> sc.geomspace('x', 1.0, 1000.0, num=4, endpoint=False)
      <scipp.Variable> (x: 4)    float64  [dimensionless]  [1, 5.62341, 31.6228, 177.828]

      >>> sc.geomspace('x', 1.0, 100.0, num=3, unit='s')
      <scipp.Variable> (x: 3)    float64              [s]  [1, 10, 100]
    """
    range_args, unit = _normalize_range_args(unit=unit, start=start, stop=stop)
    return array(dims=[dim],
                 values=_np.geomspace(**range_args, num=num, endpoint=endpoint),
                 unit=unit,
                 dtype=dtype)


def logspace(dim: str,
             start: NumberOrVar,
             stop: NumberOrVar,
             num: int,
             *,
             endpoint: bool = True,
             base: Union[int, float] = 10.0,
             unit: Union[Unit, str, None] = default_unit,
             dtype: Optional[DTypeLike] = None) -> Variable:
    """Constructs a :class:`Variable` with values spaced evenly on a log scale.

    This is similar to :py:func:`scipp.geomspace`, but with endpoints specified
    as exponents.

    Parameters
    ----------
    dim:
        Dimension label.
    start:
        The starting value of the sequence.
    stop:
        The end value of the sequence.
    num:
        Number of samples to generate.
    base:
        The base of the log space.
    endpoint:
        If True, `step` is the last returned value.
        Otherwise, it is not included.
    unit:
        Unit of contents.
    dtype: scipp.typing.DTypeLike
        Type of underlying data. By default, inferred from `value` argument.

    See Also
    --------
    scipp.arange, scipp.geomspace, scipp.linspace

    Examples
    --------

      >>> sc.logspace('x', 1, 4, num=4)
      <scipp.Variable> (x: 4)    float64  [dimensionless]  [10, 100, 1000, 10000]
      >>> sc.logspace('x', 1, 4, num=4, endpoint=False)
      <scipp.Variable> (x: 4)    float64  [dimensionless]  [10, 56.2341, 316.228, 1778.28]

    Set a different base:

      >>> sc.logspace('x', 1, 4, num=4, base=2)
      <scipp.Variable> (x: 4)    float64  [dimensionless]  [2, 4, 8, 16]

    Set a unit:

      >>> sc.logspace('x', 1, 3, num=3, unit='m')
      <scipp.Variable> (x: 3)    float64              [m]  [10, 100, 1000]
    """
    # Passing unit='one' enforces that start and stop are dimensionless.
    range_args, _ = _normalize_range_args(unit='one', start=start, stop=stop)
    return array(dims=[dim],
                 values=_np.logspace(**range_args,
                                     num=num,
                                     base=base,
                                     endpoint=endpoint),
                 unit=unit,
                 dtype=dtype)


def arange(dim: str,
           start: Union[NumberOrVar, _np.datetime64],
           stop: Optional[Union[NumberOrVar, _np.datetime64]] = None,
           step: Optional[NumberOrVar] = None,
           *,
           unit: Union[Unit, str, None] = default_unit,
           dtype: Optional[DTypeLike] = None) -> Variable:
    """Constructs a :class:`Variable` with evenly spaced values within a given
    interval.
    Values are generated within the half-open interval [start, stop)
    (in other words, the interval including start but excluding stop).

    Warning
    -------
    The length of the output might not be numerically stable.
    See :func:`numpy.arange`.

    Parameters
    ----------
    dim:
        Dimension label.
    start:
        Optional, the starting value of the sequence. Default=0.
    stop:
        End of interval. The interval does not include this value,
        except in some (rare) cases where step is not an integer and
        floating-point round-off can come into play.
    step:
        Spacing between values.
    unit:
        Unit of contents.
    dtype: scipp.typing.DTypeLike
        Type of underlying data. By default, inferred from `value` argument.

    See Also
    --------
    scipp.geomspace, scipp.linspace, scipp.logspace

    Examples
    --------

      >>> sc.arange('x', 1, 5)
      <scipp.Variable> (x: 4)      int64  [dimensionless]  [1, 2, 3, 4]
      >>> sc.arange('x', 1, 5, 0.5)
      <scipp.Variable> (x: 8)    float64  [dimensionless]  [1, 1.5, ..., 4, 4.5]

      >>> sc.arange('x', 1, 5, unit='m')
      <scipp.Variable> (x: 4)      int64              [m]  [1, 2, 3, 4]
    """
    range_args, unit = _normalize_range_args(unit=unit,
                                             start=start,
                                             stop=stop,
                                             step=step)
    return array(dims=[dim], values=_np.arange(**range_args), unit=unit, dtype=dtype)


@contextmanager
def _timezone_warning_as_error():
    with warnings.catch_warnings():
        warnings.filterwarnings('error',
                                category=DeprecationWarning,
                                message='parsing timezone')
        try:
            yield
        except DeprecationWarning:
            raise ValueError(
                'Parsing timezone aware datetimes is not supported') from None


def datetime(value: Union[str, int, _np.datetime64],
             *,
             unit: Optional[Union[Unit, str, None]] = default_unit) -> Variable:
    """Constructs a zero dimensional :class:`Variable` with a dtype of datetime64.

    Parameters
    ----------
    value:
     - `str`: Interpret the string according to the ISO 8601 date time format.
     - `int`: Number of time units (see argument ``unit``) since scipp's epoch
              (see :py:func:`scipp.epoch`).
     - `np.datetime64`: Construct equivalent datetime of scipp.
    unit: Unit of the resulting datetime.
                 Can be deduced if ``value`` is a str or np.datetime64 but
                 is required if it is an int.

    See Also
    --------
    scipp.datetimes:
    scipp.epoch:
    Details in:
        'Dates and Times' section in `Data Types <../../reference/dtype.rst>`_

    Examples
    --------

      >>> sc.datetime('2021-01-10T14:16:15')
      <scipp.Variable> ()  datetime64              [s]  [2021-01-10T14:16:15]
      >>> sc.datetime('2021-01-10T14:16:15', unit='ns')
      <scipp.Variable> ()  datetime64             [ns]  [2021-01-10T14:16:15.000000000]
      >>> sc.datetime(1610288175, unit='s')
      <scipp.Variable> ()  datetime64              [s]  [2021-01-10T14:16:15]
    """
    if isinstance(value, str):
        with _timezone_warning_as_error():
            return scalar(_np.datetime64(value), unit=unit)
    return scalar(value, unit=unit, dtype=_cpp.DType.datetime64)


def datetimes(*,
              dims,
              values: ArrayLike,
              unit: Optional[Union[Unit, str, None]] = default_unit) -> Variable:
    """Constructs an array :class:`Variable` with a dtype of datetime64.

    Parameters
    ----------
    dims:
        Dimension labels
    values: numpy.typing.ArrayLike
        Numpy array or something that can be converted to a
        Numpy array of datetimes.
    unit:
        Unit for the resulting Variable.
        Can be deduced if ``values`` contains strings or np.datetime64's.

    See Also
    --------
    scipp.datetime:
    scipp.epoch:
    Details in:
        'Dates and Times' section in `Data Types <../../reference/dtype.rst>`_

    Examples
    --------

      >>> sc.datetimes(dims=['t'], values=['2021-01-10T01:23:45', '2021-01-11T01:23:45'])
      <scipp.Variable> (t: 2)  datetime64              [s]  [2021-01-10T01:23:45, 2021-01-11T01:23:45]
      >>> sc.datetimes(dims=['t'], values=['2021-01-10T01:23:45', '2021-01-11T01:23:45'], unit='h')
      <scipp.Variable> (t: 2)  datetime64              [h]  [2021-01-10T01:00:00, 2021-01-11T01:00:00]
      >>> sc.datetimes(dims=['t'], values=[0, 1610288175], unit='s')
      <scipp.Variable> (t: 2)  datetime64              [s]  [1970-01-01T00:00:00, 2021-01-10T14:16:15]
    """
    if unit is None or unit is default_unit:
        np_unit_str = ''
    else:
        np_unit_str = f'[{_cpp.to_numpy_time_string(unit)}]'
    with _timezone_warning_as_error():
        return array(dims=dims,
                     values=_np.asarray(values, dtype=f'datetime64{np_unit_str}'))


def epoch(*, unit: Union[Unit, str]) -> Variable:
    """Constructs a zero dimensional :class:`Variable` with a dtype of
    datetime64 that contains scipp's epoch.

    Currently, the epoch of datetimes in scipp is the Unix epoch 1970-01-01T00:00:00.

    Parameters
    ----------
    unit:
        Unit of the resulting Variable.

    See Also
    --------
    scipp.datetime:
    scipp.datetimes:
    Details in:
        'Dates and Times' section in `Data Types <../../reference/dtype.rst>`_

    Examples
    --------

      >>> sc.epoch(unit='s')
      <scipp.Variable> ()  datetime64              [s]  [1970-01-01T00:00:00]
    """
    return scalar(0, unit=unit, dtype=_cpp.DType.datetime64)
