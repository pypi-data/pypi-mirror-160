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
from proxop.utils.newton import newton_


class LogBarrier:
    r"""Compute the proximity operator and the evaluation of gamma*f.

    Where f is he logarithmic barrier defined as:

                /  - ( log(x-a) + log(b-x) )    if  a < x < b
         f(x)= |
               \  + INF                                      otherwise

            with a < b

    'gamma' is the scale factor

    When the input 'x' is an array, the output is computed element-wise :

    -When calling the function (and not the proximity operator) the result
    is computed element-wise SUM. So the command >>>LogBarriers()(x) will
    return a scalar even if x is a vector.

    - But for the proximity operator (method 'prox'), the output has the same shape
    as the input 'x'. So, the command >>>LogBarriers().prox(x)   will return
    an array with the same shape as 'x'

     INPUTS
    ========
     x     - scalar or ND array
     a     - scalar or ND array with the same size as 'x' (default: a=1)
     b     - scalar or ND array with the same size as 'x' (default: b=1)
     gamma - positive, scalar or ND array with the same size as 'x' (default: gamma=1)

    =======
    Examples
    ========

     Evaluate the 'direct' function :

     >>>  LogBarrier()( 0.5 )
      1.386294361119890

      Compute the result element-wise for vector inputs :

     >>> LogBarrier(a=[-2, 0, -1], b=[2, 3, 5])( [-1, 0.3, 0.25] )
     -2.6691794267132

     Compute the proximity operator at a given point :

     >>>  LogBarrier(a=[-2, 0, -1], b=[2, 3, 5]).prox(  [-2, 3, 4 ])
     array([-1.54269095,  2.37870272,  3.26376922])

     Use a scale factor 'gamma'>0 to compute the proximity operator of  the function
     'gamma*f'

     >>>  LogBarrier(a=[-2, 0, -1], b=[2, 3, 5]).prox( [-2, 3, 4 ], gamma=2.5)
     array([-0.80311322,  1.93746944,  3.20331613])
    """

    def __init__(
            self,
            a: Union[float, np.ndarray] = 0,
            b: Union[float, np.ndarray] = 1
    ):
        if np.size(a) > 1 and (not isinstance(a, np.ndarray)):
            a = np.array(a)
        if np.size(b) > 1 and (not isinstance(b, np.ndarray)):
            b = np.array(b)
        if np.any(b < a):
            raise ValueError(
                "'b' (or all its components if it is an array) must be greater than 'a'"
            )
        self.a = a
        self.b = b

    def prox(self, x, gamma: Union[float, np.ndarray] = 1.0):
        if np.size(x) > 1 and (not isinstance(x, np.ndarray)):
            x = np.array(x)
        if np.size(gamma) > 1 and (not isinstance(gamma, np.ndarray)):
            gamma = np.array(gamma)
        self._check(x, gamma)
        a = self.a
        b = self.b

        def polynom_phi(t):
            return (
                t**3
                - (a + b + x) * t**2
                + (a * b + (a + b) * x - 2 * gamma) * t
                - a * b * x
                + (a + b) * gamma
            )

        def der_polynom_phi(t):
            return 3 * t**2 - 2 * (a + b + x) * t + a * b + (a + b) * x - 2 * gamma

        # starting point
        prox_x = (a + b) / 2
        prox_x = newton_(polynom_phi, fp=der_polynom_phi, x0=prox_x, low=a, high=b)

        return prox_x

    def __call__(self, x: np.ndarray) -> np.float:
        if np.size(x) > 1 and (not isinstance(x, np.ndarray)):
            x = np.array(x)
        a = self.a
        b = self.b
        self._check(x, 1)
        if np.size(x) <= 1:
            x = np.reshape(x, (-1))

        result = np.zeros_like(x)
        mask = np.logical_and(x > a, x < b)
        aa = a
        bb = b
        if np.size(a) > 1:
            aa = a[mask]
        if np.size(b) > 1:
            bb = b[mask]

        result[mask] = -np.log(x[mask] - aa) - np.log(bb - x[mask])

        result[np.logical_not(mask)] = np.inf

        return np.sum(result)

    def _check(self, x, gamma):
        if np.any(gamma <= 0):
            raise ValueError(
                "'gamma' (or all of its components if it is an array)" +
                " must be strictly positive"
            )

        if (np.size(gamma) > 1) and (np.shape(gamma) != np.shape(x)):
            raise ValueError(
                "''gamma' must be either scalar or have the same size as 'x'"
            )

        if (np.size(self.a) > 1) and (np.shape(self.a) != np.shape(x)):
            raise ValueError("'a' must be either scalar or the same size as 'x'")

        if (np.size(self.b) > 1) and (np.shape(self.b) != np.shape(x)):
            raise ValueError("'b' must be either scalar or the same size as 'x'")
