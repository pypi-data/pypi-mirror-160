"""
Version : 1.0 ( 06-20-2022).

DEPENDENCIES:
    - 'L2Norm.py' located in the folder 'multi'

Author  : Mbaye Diongue

Copyright (C) 2022

This file is part of the codes provided at http://proximity-operator.net

By downloading and/or using any of these files, you implicitly agree to
all the terms of the license CeCill-B (available online).
"""

from typing import Union
import numpy as np
from proxop.multi.L2Norm import L2Norm


class L21columns:
    r"""Compute the proximity operator and the evaluation of gamma*f.

     Where f is the sum of euclidian norms of the columns of a matrix:

             f(x) = \sum_{j= 1}^M |\sum_{i=1}^N |X(i,j)|^2|^{\frac{1}{2}}

            where X = U*diag(s)*V.T \in R^{M*N}  (Singular Value decomposition)

     INPUTS
    ========
     x         -  (M,N) -array_like ( representing an M*N matrix )
     gamma     - positive, scalar or ND array compatible with the size of 'x'
                 [default: gamma=1]
    """

    def __init__(self):
        pass

    def prox(self, x: np.ndarray, gamma: Union[float, np.ndarray] = 1.0) -> np.ndarray:
        return L2Norm(axis=0).prox(x, gamma)

    def __call__(self, x: np.ndarray) -> float:
        return L2Norm(axis=0)(x)
