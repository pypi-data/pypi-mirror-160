"""
Version : 1.0 (06-18-2022).

Author  : Mbaye DIONGUE

Copyright (C) 2022

This file is part of the codes provided at http://proximity-operator.net

By downloading and/or using any of these files, you implicitly agree to
all the terms of the license CeCill-B (available online).
"""

from typing import Union
import numpy as np


class Truncated:
    r"""Compute the proximity operator and the evaluation of the gamma*f.

      where the function f is defined as:

               f(x) = min{ x^2, w}

    'gamma' is the scale factor

    When the input 'x' is an array, the output is computed element-wise.

     INPUTS
    ========
    x     - ND array
    gamma - positive, scalar or ND array with the same size as 'x' [default: gamma=1]
    w     - positive, scalar or ND array with the same size as 'x'

    Note: When calling the function (and not the proximity operator) the result
    is computed element-wise SUM. So the command >>>Truncated(w=2)(x) will
    return a scalar even if x is a vector:

    >>> Truncated(w=2)(np.array([-1, 2, 3]))
    5

    But as expected, >>>Truncated(w=2).prox(x)
    will return a vector with the same size as x:

    >>> Truncated(w=2).prox(np.array([-1, 2, 3]))
    array([-0.33333333,  0.66666667,  3.        ])
    """

    def __init__(
            self,
            w: Union[float, np.ndarray]
    ):
        self.w = w

    def prox(self, x: np.ndarray, gamma: Union[float, np.ndarray] = 1.0) -> np.ndarray:
        self._check_size(x, gamma)
        mask = x**2 < self.w * (1 + 2 * gamma)
        return x / (1 + 2 * gamma * mask)

    def __call__(self, x: np.ndarray) -> float:
        return np.sum(np.minimum(x**2, self.w))

    def _check_size(self, x, gamma):
        sz_x = np.size(x)
        if np.any(gamma <= 0):
            raise Exception(
                "'gamma' (or all of its components if it"
                + " is an array) must be strictly positive"
            )
        if (np.size(self.w) > 1) and (np.size(self.w) != sz_x):
            raise Exception("'a' must be either scalar or the same size as 'x'")
        if (np.size(gamma) > 1) and (np.size(gamma) != sz_x):
            raise Exception("'gamma' must be either scalar or the same size as 'x'")