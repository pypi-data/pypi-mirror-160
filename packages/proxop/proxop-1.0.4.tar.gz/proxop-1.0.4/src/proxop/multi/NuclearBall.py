"""
Version : 1.0 ( 06-21-2022).

DEPENDENCIES:
     - 'AbsValue.py' located in the folder 'scalar'
     - 'prox_svd.py' located in the folder 'utils'
     - 'NuclearNorm.py' located in the folder 'multi'
     - 'Linf.py' located in the folder 'multi'
     - 'Max.py' in the folder 'multi'
     - 'L1Ball.py' in the folder 'indicator'

Author  : Mbaye Diongue

Copyright (C) 2022

This file is part of the codes provided at http://proximity-operator.net

By downloading and/or using any of these files, you implicitly agree to
all the terms of the license CeCill-B (available online).
"""

from typing import Union
import numpy as np
from proxop.indicator.L1Ball import L1Ball
from proxop.utils.prox_svd import prox_svd
from proxop.multi.NuclearNorm import NuclearNorm


class NuclearBall:
    r"""Compute the proximity operator and the evaluation of gamma*f.

    Where f is the indicator of the constraint set:

                         ||X||_N =||s||_1 <= eta   (nuclear norm ball constraint)

            where X = U*diag(s)*V.T \in R^{M*N}

     INPUTS
    ========
     x         -  (M,N) -array_like ( representing an M*N matrix )
     gamma     - positive, scalar or ND array compatible with the size of 'x'
                 [default: gamma=1]
     eta       - positive, scalar or ND array compatible with the size of 'x'
    """

    def __init__(
            self,
            eta: Union[float, np.ndarray]
    ):
        if np.any(eta <= 0):
            ValueError("'eta' must be strictly positive")
        self.eta = eta

    def prox(self, x: np.ndarray, gamma: Union[float, np.ndarray] = 1) -> np.ndarray:
        return prox_svd(x, 1, L1Ball(eta=gamma).prox)

    def __call__(self, x: np.ndarray) -> np.float:
        nuclear_norm = NuclearNorm()(x)
        if nuclear_norm <= self.eta:
            return 0
        return np.inf
