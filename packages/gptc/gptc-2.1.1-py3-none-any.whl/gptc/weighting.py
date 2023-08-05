# SPDX-License-Identifier: LGPL-3.0-or-later

import math
from typing import Sequence, Union, Tuple, List


def _mean(numbers: Sequence[float]) -> float:
    """Calculate the mean of a group of numbers

    Parameters
    ----------
    numbers : list of int or float
        The numbers to calculate the mean of

    Returns
    -------
    float
        The mean of the numbers
    """
    return sum(numbers) / len(numbers)


def _standard_deviation(numbers: Sequence[float]) -> float:
    """Calculate the standard deviation of a group of numbers

    Parameters
    ----------
    numbers : list of int or float
        The numbers to calculate the mean of

    Returns
    -------
    float
        The standard deviation of the numbers

    """
    mean = _mean(numbers)
    squared_deviations = [(mean - i) ** 2 for i in numbers]
    return math.sqrt(_mean(squared_deviations))


def weight(numbers: Sequence[float]) -> List[float]:
    standard_deviation = _standard_deviation(numbers)
    weight = standard_deviation * 2
    weighted_numbers = [i * weight for i in numbers]
    return weighted_numbers
