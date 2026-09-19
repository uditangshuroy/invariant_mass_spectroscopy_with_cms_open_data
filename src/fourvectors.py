"""
fourvectors.py
============

Functions for reconstructing invariant masses from CMS Open Data.

Author: Uditangshu Roy
The University of Manchester
Date: August 2026
"""

# Imports
import numpy as np


def invariant_mass_exact(df, rest_mass):
    """
    Calculate the exact invariant mass using four-vector kinematics.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing pt1, pt2, eta1, eta2, phi1 and phi2.

    rest_mass : float
        Rest mass of the lepton in GeV.

    Returns
    -------
    numpy.ndarray
        Invariant mass for each event.
    """

    E1 = np.sqrt(
        rest_mass**2 +
        (df["pt1"] * np.cosh(df["eta1"]))**2
    )

    E2 = np.sqrt(
        rest_mass**2 +
        (df["pt2"] * np.cosh(df["eta2"]))**2
    )

    p_dot = (
        df["pt1"] *
        df["pt2"] *
        (
            np.cos(df["phi1"] - df["phi2"])
            +
            (np.sinh(df["eta1"]) *
             np.sinh(df["eta2"]))
        )
    )

    M2 = 2 * (rest_mass**2 + (E1 * E2) - p_dot)

    # Makes sure to avoid negative values under the square root due to numerical errors.
    return np.sqrt(np.maximum(M2, 0))


def invariant_mass_massless(df):
    """
    Calculate the invariant mass using the massless approximation.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing pt1, pt2, eta1, eta2, phi1 and phi2.

    Returns
    -------
    numpy.ndarray
        Invariant mass for each event.
    """

    M2 = (
        2
        * df["pt1"]
        * df["pt2"]
        * (
            np.cosh(df["eta1"] - df["eta2"])
            - np.cos(df["phi1"] - df["phi2"])
        )
    )

    # Makes sure to avoid negative values under the square root due to numerical errors.
    return np.sqrt(np.maximum(M2, 0))


def invariant_mass_fourvector(df):
    """
    Calculate the invariant mass from the measured four-vector
    components of two particles, for the larger dataset.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing E1, px1, py1, pz1, E2, px2, py2 and pz2.

    Returns
    -------
    numpy.ndarray
        Invariant mass for each event in GeV.
    """

    E_total = df["E1"] + df["E2"]

    px_total = df["px1"] + df["px2"]
    py_total = df["py1"] + df["py2"]
    pz_total = df["pz1"] + df["pz2"]

    M2 = (
        E_total**2
        - px_total**2
        - py_total**2
        - pz_total**2
    )

    # Makes sure to avoid negative values under the square root due to numerical errors.
    return np.sqrt(np.maximum(M2, 0))


def momentum_components(pt, eta, phi):
    """
    Converts transverse momentum (pt), pseudorapidity (eta), and azimuthal angle (phi) into the Cartesian components of momentum (px, py, pz).

    Returns
    -------
    numpy.ndarray
        px, py, pz components of momentum.
    """

    px = pt * np.cos(phi)
    py = pt * np.sin(phi)
    pz = pt * np.sinh(eta)

    return np.array([px, py, pz])
