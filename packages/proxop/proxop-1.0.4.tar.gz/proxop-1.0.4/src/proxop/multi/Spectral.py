"""
Version : 1.0 ( 06-21-2022).

DEPENDENCIES:
     -'prox_svd.py' - located in the folder 'utils'
     -'fun_svd.py'  - located in the folder 'utils'
     -'Linf.py'     - located in the folder 'multi'

Author  : Mbaye Diongue

Copyright (C) 2022

This file is part of the codes provided at http://proximity-operator.net

By downloading and/or using any of these files, you implicitly agree to
all the terms of the license CeCill-B (available online).
"""

from typing import Union
import numpy as np
from proxop.multi.Linf import Linf
from proxop.utils.prox_svd import prox_svd
from proxop.utils.fun_svd import fun_svd


class Spectral:
    r"""Compute the proximity operator and the evaluation of gamma*f.

    Where f is the funtion definded as:

                         f(x)= ||X||_S

            where X = U*diag(s)*V.T \in R^{M*N}


     INPUTS
    ========
     x         -  (M,N) -array_like ( representing an M*N matrix )
     gamma     - positive, scalar or ND array compatible with the size of 'x'
                 [default: gamma=1]
    """

    def __init__(self):
        pass

    def prox(self, x: np.ndarray, gamma: Union[float, np.ndarray] = 1) -> np.ndarray:
        self._check(x, gamma)
        return prox_svd(x, gamma, Linf().prox)

    def __call__(self, x: np.ndarray) -> np.float:
        return fun_svd(x, 1, Linf())

    def _check(self, x, gamma):
        if np.any(gamma <= 0) or np.size(gamma) > 1:
            raise Exception("'gamma'  must be a strictly positive scalar")
        if len(np.shape(x)) != 2:
            raise ValueError(
                "'x' must be an (M,N) -array_like ( representing an M*N matrix )"
            )
