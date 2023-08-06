"""
Version : 1.0 ( 06-22-2022).

Author  : Mbaye Diongue

Copyright (C) 2022

This file is part of the codes provided at http://proximity-operator.net

By downloading and/or using any of these files, you implicitly agree to
all the terms of the license CeCill-B (available online).
"""

from typing import Union, Tuple
import numpy as np


class AbsDiff:
    r"""Compute the proximity operator and the evaluation of gamma*D.

    Where D is the  function defined as:

                  /  |x-y|        if x >= 0 and y >= 0
        D(x,y) = |
                 \  + inf         otherwise

    'gamma' is the scale factor

    When the inputs are arrays, the outputs are computed element-wise

    ========
     INPUTS
    ========
    x     - ND array
    y     - ND array with the same size as 'x'
    gamma - positive, scalar or ND array with the same size as 'x' [default: gamma=1]
    """

    def __init__(self):
        pass

    def prox(
            self,
            x: np.ndarray, y: np.ndarray,
            gamma: Union[float, np.ndarray] = 1
    ) -> Tuple[np.ndarray, np.ndarray]:
        if np.size(x) != np.size(y):
            raise ValueError("'x' and 'y' must have the same size")
        scale = gamma
        self._check(x, gamma)

        if np.size(x) <= 1:
            x = np.reshape(x, (-1))
            y = np.reshape(y, (-1))
        sz = np.shape(x)

        # 4th branch
        prox_p = np.zeros(sz)
        prox_q = np.zeros(sz)

        # 3rd branch
        mask = (y > scale) * (x <= -scale)
        yy = y - scale
        prox_q[mask] = yy[mask]

        # 2nd branch
        mask = (x > scale) * (y <= -scale)
        xx = x - scale
        prox_p[mask] = xx[mask]

        # 1st branch
        t = np.sign(x - y) * np.maximum(0, np.abs(x - y) - 2 * scale)
        mask = np.abs(t) < x + y
        xy = x[mask] + y[mask]
        tt = t[mask]
        prox_p[mask] = 0.5 * (xy + tt)
        prox_q[mask] = 0.5 * (xy - tt)

        return tuple([prox_p, prox_q])

    def __call__(self, x: np.ndarray, y: np.ndarray) -> np.float:
        if np.any(x < 0) or np.any(y < 0):
            return np.inf
        return np.sum(np.abs(x - y))

    def _check(self, x, gamma=1):
        if np.any(gamma <= 0):
            raise ValueError("'gamma'  must be strictly positive")
        if np.size(gamma) > 1 and np.size(gamma) != np.size(x):
            ValueError(
                "'gamma' must be positive scalars or positive ND arrays" +
                " with the same size as 'x'"
            )
