"""
Version : 1.0 ( 06-10-2022).

Author  : Mbaye DIONGUE

Copyright (C) 2019

This file is part of the codes provided at http://proximity-operator.net

By downloading and/or using any of these files, you implicitly agree to
all the terms of the license CeCill-B (available online).
"""

from typing import Union
import numpy as np


class Hyperslab:
    """Compute the projection onto the hyper-slab.

    Where the hyper-slab is the set defined as:

                         low  <= u.T * x <= high

     where u.T denotes the transpose of u

     INPUTS
    ========
     x    - ND array
     u    - ND array with the same size as 'x'
     low  - scalar or ND array compatible with the blocks of 'x' [default: low=0]
     high - scalar or ND array compatible with the blocks of 'x' [default: high=1]
    """

    def __init__(
            self,
            u: np.ndarray,
            low: Union[float, np.ndarray] = 0.0,
            high: Union[float, np.ndarray] = 1.0
    ):
        if np.any(low > high):
            raise ValueError("'low' must be lower than 'high'")
        self.low = low
        self.high = high
        self.u = u

    def prox(self, x: np.ndarray) -> np.ndarray:
        """Compute the proximity operator (i.e. projection of 'x' on the hyper-slab).

        Parameters
        ----------
        x : np.ndarray

        Returns
        -------
        TYPE : np.ndarray with the same size as x
        """
        self._check(x)
        scalar_prod = np.sum(x * self.u)
        u = self.u
        if np.any(scalar_prod < self.low):
            return x + ((self.low - scalar_prod) / np.sum(u**2)) * u
        if np.any(scalar_prod > self.high):
            return x + ((self.high - scalar_prod) / np.sum(u**2)) * u
        return x

    # indicator of the hyperslab
    def __call__(self, x: np.ndarray):
        """
        Indicate if the input 'x' is in the constraint set or not.

        Parameters
        ----------
        x : np.ndarray

        Returns
        -------
        0      if the input 'x' is in the set
        +inf   otherwise
        """
        self._check(x)
        scalar_prod = np.sum(x * self.u)
        tol = 1e-10
        if np.all(scalar_prod >= self.low - tol) and np.all(
            scalar_prod <= self.high + tol
        ):
            return 0
        return np.inf

    def _check(self, x: np.ndarray):
        if (np.shape(self.u)) != np.shape(x):
            raise ValueError("'u' must have the same size as 'x'")
