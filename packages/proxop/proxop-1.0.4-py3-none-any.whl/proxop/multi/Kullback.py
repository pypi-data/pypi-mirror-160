"""
Version : 1.0 ( 06-22-2022).

DEPENDENCIES:
    -'newton.py'  - located in the folder 'utils'

Author  : Mbaye Diongue

Copyright (C) 2022

This file is part of the codes provided at http://proximity-operator.net

By downloading and/or using any of these files, you implicitly agree to
all the terms of the license CeCill-B (available online).
"""

from typing import Union, Tuple
import numpy as np
from proxop.utils.newton import newton_


class Kullback:
    r"""Compute the proximity operator and the evaluation of gamma*D.

    Where D is the function defined as:


                  /  x * log(x/y)                     if x > 0 and y > 0
        D(x,y) = |   0                                if x=y=0
                 \   + inf                            otherwise

    'gamma' is the scale factor

            When the inputs are arrays, the outputs are computed element-wise
    INPUTS
    ========
    x          - scalar or ND array
    y          - scalar or ND array with the same size as 'x'
    gamma      - scalar or ND array compatible with the blocks of 'y'[default: gamma=1]
    """

    def __init__(
            self
    ):
        pass

    def prox(
            self,
            x: np.ndarray,
            y: np.ndarray,
            gamma: Union[float, np.ndarray] = 1
    ) -> Tuple[np.ndarray, np.ndarray]:
        self._check(x, gamma)
        if np.size(x) != np.size(y):
            raise Exception("'x' and 'y' must have the same size")
        # scalar-like inputs handling
        if np.size(x) <= 1:
            x = np.reshape(x, (-1))
            y = np.reshape(y, (-1))

        # 2nd branch
        sz = np.shape(x)
        prox_p = np.zeros(sz)
        prox_q = np.zeros(sz)

        # branch selection
        mask = np.exp(x / gamma - 1) >= -y / gamma
        xx = x[mask]
        yy = y[mask]
        gg = gamma
        if np.size(gg) > 1:
            gg = gamma[mask]

        # newton's method
        def fun_phi(t):
            return t * np.log(t) + (xx / gg - 1) * t - 1 / t - yy / gg

        def der_fun_phi(t):
            return np.log(t) + xx / gg + 1 / t ** 2

        # root finding
        root = np.exp(-xx / gg)
        low = 1 / np.e * root
        root = newton_(fun_phi, fp=der_fun_phi, x0=root, low=low, high=np.inf)

        # 1st branch
        prox_p[mask] = xx + gg * np.log(root) - gg
        prox_q[mask] = yy + gg / root

        return tuple([prox_p, prox_q])

    def __call__(
            self,
            x: np.ndarray,
            y: np.ndarray
    ) -> np.float:
        if np.size(x) != np.size(y):
            raise Exception("'x' and 'y' must have the same size")
        if (
            np.any(x < 0)
            or np.any(y < 0)
            or np.any((x == 0) * (y != 0))
            or np.any((y == 0) * (x != 0))
        ):
            return np.inf
        if np.size(x) <= 1:
            x = np.reshape(x, (-1))
            y = np.reshape(y, (-1))
        mask = y > 0
        res = x[mask] * np.log(x[mask] / y[mask])
        return np.sum(res)

    def _check(self, x, gamma=1):
        if np.any(gamma <= 0):
            raise Exception("'gamma'  must be strictly positive")
        if np.size(gamma) > 1 and np.size(gamma) != np.size(x):
            ValueError(
                "'gamma' must be positive scalars or positive ND arrays" +
                " with the same size as 'x'"
            )
