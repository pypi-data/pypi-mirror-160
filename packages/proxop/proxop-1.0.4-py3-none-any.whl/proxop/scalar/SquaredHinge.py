"""
Version : 1.0 (06-09-2022).

Author  : Mbaye DIONGUE

Copyright (C) 2022

This file is part of the codes provided at http://proximity-operator.net

By downloading and/or using any of these files, you implicitly agree to
all the terms of the license CeCill-B (available online).
"""

from typing import Union
import numpy as np


class SquaredHinge:
    r"""Computes the proximity operator and the evaluation of gamma*f.

    Where f is the hinge Loss function defined as:

                      f(x) = max{1-x,0}^2

    'gamma' is the scale factor

    When the input 'x' is an array, the output is computed element-wise :

    -When calling the function (and not the proximity operator) the result
    is computed element-wise SUM. So the command >>>HingeLoss()(x) will
    return a scalar even if x is a vector.

    - But for the proximity operator (method 'prox'), the output has the
    same shape as the input 'x'. So, the command >>>HingeLoss().prox(x)
    will return an array with the same shape as 'x'

     INPUTS
    ========
     x     - ND array
     gamma  - positive, scalar or array with the same size as 'x' [default: gamma=1]

    =======
    Examples
    ========

     Evaluate the 'direct' function :

     >>> SquaredHinge()(2)
     0

    The output is computed as element-wise sum for vector inputs :

     >>> SquaredHinge()([2., 0.25, -0.5, 0.])
     3.8125

     Compute the proximity operator at a given point :

     >>> SquaredHinge().prox(  [-2, 3, 4 ])
     array([0.,  3.,  4.])

     Use a scale factor 'gamma'>0 to compute the proximity operator of  the function
     'gamma*f':

     >>> SquaredHinge().prox( [-2, 3, 4, np.e ] , gamma=2.5)
     array([0.5       , 3.        , 4.        , 2.71828183]
    """

    def __init__(self):
        pass

    def prox(self, x: np.ndarray, gamma: Union[float, np.ndarray] = 1.0) -> np.ndarray:
        if np.size(x) > 1 and (not isinstance(x, np.ndarray)):
            x = np.array(x)
        if np.size(gamma) > 1 and (not isinstance(gamma, np.ndarray)):
            gamma = np.array(gamma)
        if np.size(x) <= 1:
            x = np.reshape(x, (-1))

        self._check(x, gamma)
        prox_x = (2*gamma + x)/(2*gamma + 1)
        mask = np.logical_and(x >= 1 - gamma, x <= 1)
        prox_x[mask] = 1
        mask = x > 1
        prox_x[mask] = x[mask]
        return prox_x

    def __call__(self, x: np.ndarray) -> np.float:
        if np.size(x) > 1 and (not isinstance(x, np.ndarray)):
            x = np.array(x)
        fun_x = np.maximum(1 - x, 0)**2
        return np.sum(fun_x)

    def _check(self, x, gamma):
        if np.any(gamma <= 0):
            raise ValueError(
                "'gamma' (or all of its elements if it is an array)"
                + "must be strictly positive"
            )
        if (np.size(gamma) > 1) and (np.size(gamma) != np.size(x)):
            raise ValueError("gamma' must be either scalar or the same size as 'x'")

