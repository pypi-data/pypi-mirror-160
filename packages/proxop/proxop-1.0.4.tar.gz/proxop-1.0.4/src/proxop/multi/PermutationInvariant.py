"""
Version : 1.0 ( 06-21-2022).

DEPENDENCIES:
     - 'prox_svd.py' located in the folder 'utils'
     - 'fun_svd.py' located in the folder 'utils'

Author  : Mbaye Diongue

Copyright (C) 2022

This file is part of the codes provided at http://proximity-operator.net

By downloading and/or using any of these files, you implicitly agree to
all the terms of the license CeCill-B (available online).
"""

from proxop.utils.prox_svd import prox_svd
from proxop.utils.fun_svd import fun_svd
import numpy as np


class PermutationInvariant:
    r"""Compute the proximity operator and the evaluation of gamma*f.

    Where f is the function defined as:

                            f(X) = phi(s)

    where :
          * X = U*diag(s)*V.T \in R^{M*N}  (the Singular Value decomposition of X)

          * 'gamma' is the scale factor

     INPUTS
    ========
     x           -  (M,N) -array_like ( representing an M*N matrix)
     gamma       - positive scalar  [default: gamma=1]
     ClassPhi    - A class that has at least the two methods: 'ClassPhi.__call___(x)'
                   and 'phi.prox(x, tau)'. >>> ClassPhi.__call__(x) must return phi(x)
                   (i.e. the value of the function phi evaluated at  x) and
                   '>>> ClassPhi.prox(x, tau)' the proximity operator of tau*phi
                   evaluated at x.
    """

    def __init__(
            self,
            class_phi
    ):
        self.class_phi = class_phi

    def prox(self, x: np.ndarray, gamma: float = 1) -> np.ndarray:
        if np.any(gamma <= 0) or np.size(gamma) > 1:
            raise Exception("'gamma'  must be a strictly positive scalar")

        return prox_svd(x, gamma, self.class_phi().prox)

    def __call__(self, x):
        return fun_svd(x, 1, self.class_phi().prox)
