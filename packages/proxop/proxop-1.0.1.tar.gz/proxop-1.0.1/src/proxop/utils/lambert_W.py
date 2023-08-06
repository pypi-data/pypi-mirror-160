"""
Compute here the lambert_W function.

Created on Wed Jun  8 2022

Author: Mbaye Diongue
"""
import numpy as np


def lambert_W(x, branch=0):
    r"""Compute here the lambert_W function.

    Parameters:

    x: float or np.ndarray
    branch: int
    """
    # CHose a starting point
    if branch != -1:
        w = np.ones_like(x)
    else:
        w = -2 * np.ones_like(x)

    # Haley's method
    stop = False
    tol = 1e-10
    max_iter = 100
    i = 0
    while (not stop) and (i < max_iter):
        w_old = w
        e = np.exp(w)
        f = w * e - x
        w = w - f / (e * (w + 1) - (w + 2) * f / (2 * w + 2))
        if np.linalg.norm(w - w_old) < np.linalg.norm(w) * tol:
            stop = True
        i += 1

    return w
