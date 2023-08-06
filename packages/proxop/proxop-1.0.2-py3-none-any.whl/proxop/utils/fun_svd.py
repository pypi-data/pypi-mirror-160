"""
Evaluate phi(s) where s is the vector that is composed by singular values of x.

Version : 1.0 (06-14-2022).

Author  : Mbaye Diongue

Copyright (C) 2022

This file is part of the codes provided at http://proximity-operator.net

By downloading and/or using any of these files, you implicitly agree to
all the terms of the license CeCill-B (available online).
"""

import numpy as np


def fun_svd(
        x: np.ndarray,
        gamma: float or np.ndarray,
        fun_phi, hermitian: bool = False
) -> np.ndarray:
    r"""Evaluate phi(s) where s is the vector that is composed by singular values of x.

                        f(x) = gamma * phi(s)

     Where X = U*diag(s)*V.T \in R^{M*N}  is the Singular Value decomposition of X

      INPUTS
     ========
    x       - ND array
    gamma   - positive, scalar or ND array compatible with the size of 'x'
    fun_phi - function handle with one argument at least
    """
    # spectral decomposition
    u, s, vh = np.linalg.svd(x, full_matrices=True, hermitian=hermitian)

    return gamma * fun_phi(s)
