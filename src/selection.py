"""
selection.py
============

This module contains functions for selecting and filtering data related to particle physics, 
specifically in the context of the CMS Z-Boson Analysis project.

Author: Uditangshu Roy
The University of Manchester
Date: August 2026
"""

import numpy as np
import pandas as pd
from .utilities import TABLE_STYLES
from .validation import transverse_momentum_calculation


def select_global_muons(df):
    """
    Selects global muons from the given DataFrame.

    Parameters
    ----------
    df: pandas.DataFrame
        The input DataFrame containing particle data.

    Returns
    -------
    pandas.DataFrame
        A DataFrame containing only the selected global muons.
    """

    global_muon_mask = (
        (df["type1"] == "G") &
        (df["type2"] == "G")
    )

    return df[global_muon_mask]


def select_opposite_charge_pairs(df):
    """
    Selects pairs of particles with opposite charges from the given DataFrame.

    Parameters
    ----------
    df: pandas.DataFrame
        The input DataFrame containing particle data.

    Returns
    -------
    pandas.DataFrame
        A DataFrame containing only the selected pairs with opposite charges.
    """

    charge_mask = (
        df["Q1"] *
        df["Q2"]
        == -1
    )

    return df[charge_mask]


def leading_subleading_pt(df):
    """
    Determines the leading and subleading transverse momentum (p_T) for each pair of particles in the DataFrame.

    Parameters
    ----------
    df: pandas.DataFrame
        The input DataFrame containing particle data.

    Returns
    -------
    tuple of pandas.Series
        Two Series containing the leading and subleading transverse momentum values.
    """

    pt1_calc = transverse_momentum_calculation(df["px1"], df["py1"])
    pt2_calc = transverse_momentum_calculation(df["px2"], df["py2"])

    leading_pt = np.maximum(pt1_calc, pt2_calc)
    subleading_pt = np.minimum(pt1_calc, pt2_calc)

    return leading_pt, subleading_pt


def select_transverse_momentum(df, leading_threshold=20.0, subleading_threshold=20.0):
    """
    Selects pairs of particles with transverse momentum above a given threshold.

    Parameters
    ----------
    df: pandas.DataFrame
        The input DataFrame containing particle data.

    leading_threshold: float, optional
        The threshold for the leading particle's transverse momentum. Default is 20.0 GeV.
    subleading_threshold: float, optional
        The threshold for the subleading particle's transverse momentum. Default is 20.0 GeV.

    Returns
    -------
    pandas.DataFrame
        A DataFrame containing only the selected pairs with transverse momentum above the threshold.
    """

    leading_pt, subleading_pt = leading_subleading_pt(df)

    pt_mask = (
        (leading_pt > leading_threshold) &
        (subleading_pt > subleading_threshold)
    )

    return df[pt_mask]


def select_pseudorapidity(df, eta_threshold=2.4):
    """
    Selects pairs of particles with pseudorapidity within a given threshold.

    Parameters
    ----------
    df: pandas.DataFrame
        The input DataFrame containing particle data.

    eta_threshold: float, optional
        The threshold for the absolute value of pseudorapidity. Default is 2.4.

    Returns
    -------
    pandas.DataFrame
        A DataFrame containing only the selected pairs with pseudorapidity within the threshold.
    """

    eta_mask = (
        (np.abs(df["eta1"]) < eta_threshold) &
        (np.abs(df["eta2"]) < eta_threshold)
    )

    return df[eta_mask]


def select_invariant_mass(df, mass_range=(60.0, 120.0)):
    """
    Selects pairs of particles with invariant mass within a given range.

    Parameters
    ----------
    df: pandas.DataFrame
        The input DataFrame containing particle data.

    mass_range: tuple, optional
        A tuple specifying the lower and upper bounds for the invariant mass. Default is (60.0, 120.0) GeV.

    Returns
    -------
    pandas.DataFrame
        A DataFrame containing only the selected pairs with invariant mass within the specified range.
    """

    invariant_mass_mask = (
        (df["M"] > mass_range[0]) &
        (df["M"] < mass_range[1])
    )

    return df[invariant_mass_mask]


def selection_summary(
    df_before,
    df_after,
    previous_selection_name="Previous Selection",
    current_selection_name="Current Selection",
    caption=""
):
    """
    Provides a summary of the selection process, including the number of events remaining after each selection stage.

    Parameters
    ----------
    df_before: pandas.DataFrame
        The input DataFrame containing particle data before selection.
    df_after: pandas.DataFrame
        The input DataFrame containing particle data after selection.
    previous_selection_name: str, optional
        The name of the previous selection stage. The default is "Previous Selection".
    current_selection_name: str, optional
        The name of the current selection stage. The default is "Current Selection".
    caption: str, optional
        The caption for the summary table.

    Returns
    -------
    pandas.io.formats.style.Styler
        A styled DataFrame summarizing the selection process.
    """

    initial_count = 100000

    selection_summary = (
        pd.DataFrame({
            "Quantity": [
                "Total Events",
                f"Events after {previous_selection_name}",
                f"Events after {current_selection_name}",
                f"Events Discarded by {current_selection_name}",
                "Selection Efficiency (relative to previous selection)",
                "Cumulative Efficiency (relative to total dataset)"
            ],
            "Value": [
                initial_count,
                len(df_before),
                len(df_after),
                len(df_before) - len(df_after),
                f"{100*len(df_after)/len(df_before):.2f}%",
                f"{100*len(df_after)/initial_count:.2f}%"
            ]
        })
        .style
        .hide(axis="index")
        .set_caption(caption)
        .set_table_styles(TABLE_STYLES)
    )

    return selection_summary
