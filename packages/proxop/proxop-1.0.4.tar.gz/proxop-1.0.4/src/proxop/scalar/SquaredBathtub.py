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


class SquaredBathtub:
    r"""Computes the proximity operator and the evaluation of gamma*f.

    Where f is the 'squared w-insensitive loss' function defined as:

            f(x) =  (max{|x|-w,0} )^2   with w > 0

    'gamma' is the scale factor

    When the input 'x' is an array, the output is computed element-wise :

    -When calling the function, the output is a scalar (sum of the
    element-wise results ) .

    - But for the proximity operator (method 'prox'), the output has the same
    shape as the input 'x'.

     INPUTS
    ========
     x     - scalar or ND array
     w     - positive, scalar or ND array with the same size as 'x'
     gamma - positive, scalar or ND array with the same size as 'x' (default: gamma=1)

    =======
    Examples
    ========

     Evaluate the function  f:

     >>> SquaredBathtub(3)( 2 )
     0.0

      Compute the result element-wise for vector inputs :

     >>> SquaredBathtub(w=2)( [-1, 3, -5] )
     14.5

     Compute the proximity operator at a given point :

     >>> SquaredBathtub(2).prox(  [-2, 3, 4 ] )
     array([-2. ,  2.5,  3. ])

     Use a scale factor 'gamma'>0 to compute the proximity operator of
     the function 'gamma*f'

     >>> SquaredBathtub( 2).prox( [-2, 3, 4, 6 ], gamma=[1,2,3,3])
     array([-2.        ,  2.33333333,  2.5       ,  3.        ]
    """

    def __init__(self, w: Union[float, np.ndarray]):
        if np.size(w) > 1 and (not isinstance(w, np.ndarray)):
            w = np.array(w)
        if np.any(w <= 0):
            raise ValueError(
                "'w' (or all of its components if it is an array)"
                + " must be strictly positive"
            )
        self.w = w

    def prox(self, x: np.ndarray, gamma: Union[float, np.ndarray] = 1.0) -> np.ndarray:
        if np.size(x) > 1 and (not isinstance(x, np.ndarray)):
            x = np.array(x)
        if np.size(gamma) > 1 and (not isinstance(gamma, np.ndarray)):
            gamma = np.array(gamma)
        if np.size(x) <= 1:
            x = np.reshape(x, (-1))
        self._check(x, gamma)

        # preliminaries
        abs_x = np.abs(x)
        sign_x = np.sign(x)

        # 2nd branch
        prox_x = (x + gamma * self.w * sign_x) / (gamma + 1)

        # 1st branch
        mask = abs_x <= self.w
        prox_x[mask] = x[mask]
        return prox_x

    def __call__(self, x: np.ndarray) -> np.float:
        return np.sum(0.5 * (np.maximum(np.abs(x) - self.w, 0)) ** 2)

    def _check(self, x, gamma):
        if np.any(gamma <= 0):
            raise ValueError(
                "'gamma' (or all of its components if it is an array) must "
                + "be strictly positive"
            )
        if (np.size(gamma) > 1) and (np.size(gamma) != np.size(x)):
            raise ValueError("gamma' must be either scalar or the same size as 'x'")
        if (np.size(self.w) > 1) and (np.size(self.w) != np.size(x)):
            raise ValueError("w' must be either scalar or the same size as 'x'")
