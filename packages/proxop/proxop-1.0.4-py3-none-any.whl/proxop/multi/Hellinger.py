"""
Version : 1.0 ( 06-22-2022).

DEPENDENCIES:
    -'Ialpha.py'  - located in the folder 'multi'

Author  : Mbaye Diongue

Copyright (C) 2022

This file is part of the codes provided at http://proximity-operator.net

By downloading and/or using any of these files, you implicitly agree to
all the terms of the license CeCill-B (available online).
"""

from typing import Union, Tuple
import numpy as np
from proxop.multi.Ialpha import Ialpha


class Hellinger:
    r"""Compute the proximity operator and the evaluation of gamma*D.

    Where D is the  Hellinger function defined as:


                  /  ( sqrt(x) - sqrt(y) )^2   if x >= 0 and y >= 0
        D(x,y) = |
                 \  + inf                    otherwise

    'gamma' is the scale factor

     ========
     INPUTS
    ========
    x        - scalar or ND array
    y        - scalar if 'x' is a scalar , ND array with the same size as 'x' otherwise
    gamma    - positive, scalar or ND array with the same size as 'x' [default: gamma=1]
    """

    def __init__(self):
        pass

    def prox(
            self,
            x: np.ndarray,
            y: np.ndarray,
            gamma: Union[float, np.ndarray] = 1
    ) -> Tuple[np.ndarray, np.ndarray]:
        self._check(x)
        return Ialpha(alpha=2).prox(x, y, gamma)

    def __call__(self, x: np.ndarray, y: np.ndarray) -> np.float:
        if np.any(x < 0) or np.any(y < 0):
            return np.inf
        return np.sum((np.sqrt(x) - np.sqrt(y)) ** 2)

    def _check(self, x, gamma=1):
        if np.any(gamma <= 0):
            raise Exception("'gamma'  must be strictly positive")
        if np.size(gamma) > 1 and np.size(gamma) != np.size(x):
            ValueError(
                "'gamma' must be positive scalars or positive ND arrays" +
                " with the same size as 'x'"
            )
