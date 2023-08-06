"""
Version : 1.0 ( 06-13-2022).

DEPENDENCIES:
    -'AbsValue.py'  - located in the folder 'utils'

Author  : Mbaye Diongue

Copyright (C) 2022

This file is part of the codes provided at http://proximity-operator.net

By downloading and/or using any of these files, you implicitly agree to
all the terms of the license CeCill-B (available online).
"""""

from typing import Union, Optional
import numpy as np


class L1Norm:
    r"""Compute the proximity operator and the evaluation of gamma*f.

    Where f is the L1 norm:

                        f(x) = \sum_{i=1}^{N}( |x_i| )

    'gamma' is the scale factor

     INPUTS
    ========
     x         - ND array
     gamma     - positive, scalar or ND array compatible with the blocks of 'x'
                 [default: gamma=1]
     axis    - None or int, axis of block-wise processing [default: axis=None]
                  axis = None --> 'x' is processed as a single vector [DEFAULT] In this
                  case 'gamma' must be a scalar.
                  axis >=0   --> 'x' is processed block-wise along the specified axis
                  (0 -> rows, 1-> columns ect. In this case, 'gamma' must be singleton
                  along 'axis'.
    """

    def __init__(self, axis: Optional[int] = None):
        if (axis is not None) and (axis < 0):
            axis = None
        self.axis = axis

    def prox(self, x: np.ndarray, gamma: Union[float, np.ndarray] = 1) -> np.ndarray:
        self._check(x, gamma)
        prox_x = np.sign(x)*np.maximum(np.abs(x)-gamma, 0)
        return prox_x

    def __call__(self, x: np.ndarray, gamma: Union[float, np.ndarray] = 1,) -> float:
        l1_x = np.linalg.norm(x, ord=1, axis=self.axis)
        return np.sum(l1_x)

    def _check(self, x, gamma):
        if np.any(gamma <= 0):
            raise ValueError(
                "'gamma' (or all of its components if it is an array)" +
                " must be strictly positive"
            )
        if self.axis is None and np.size(gamma) > 1:
            raise ValueError(
                "'gamma' must be a scalar when the parameter 'axis' is equal to 'None'"
            )
        if np.size(gamma) <= 1:
            return
        sz = np.shape(x)
        if len(sz) <= 1:
            self.axis = None
        if len(sz) <= 1:
            raise ValueError(
                "'gamma' must be scalar when 'x' is one dimensional"
            )
        if len(sz) > 1 and (self.axis is not None):
            sz = np.array(sz, dtype=int)
            sz[self.axis] = 1
            if np.size(gamma) > 1 and (np.prod(sz) != np.size(gamma)):
                raise ValueError(
                    "The dimension of 'gamma' is not compatible" +
                    " with the blocks of 'x'"
                )
