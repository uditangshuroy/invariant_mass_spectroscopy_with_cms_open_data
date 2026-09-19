"""
validation.py
============

Contains functions for validating and analyzing the results of calculations related to particle physics, 
specifically in the context of the CMS Z-Boson Analysis project.

Author: Uditangshu Roy
The University of Manchester
Date: August 2026
"""

# Imports
import numpy as np
import pandas as pd

from .utilities import (
    TABLE_STYLES,
    make_formatter
)


def analyse_residuals(residual):
    """
    Analyses the residuals and returns the mean, standard deviation, maximum absolute difference, and difference limits.

    Parameters
    ----------
    residual: array-like
        The residual values.

    Returns
    -------
    dict
        A dictionary containing the mean, standard deviation, maximum absolute difference, and difference limits.
    """

    def num_fmt(x): return f"{x:.3f}"  # Number formatting

    return {
        "Mean": residual.mean(),
        "Standard Deviation": residual.std(),
        "Maximum Absolute Difference": num_fmt(np.abs(residual).max()),
        "Difference Limits": (float(num_fmt(residual.min())), float(num_fmt(residual.max())))
    }


def residual_analysis_summary(
        residual_analysis_1,
        residual_analysis_2,
        caption="",
        format=make_formatter()
):
    """
    Generates a summary of the residual analysis.

    Parameters
    ----------
    residual_analysis_1: dict
        A dictionary containing the results of the first residual analysis.
    residual_analysis_2: dict
        A dictionary containing the results of the second residual analysis.
    caption: str, optional
        A caption for the summary table. Default is an empty string.
    format: callable, optional
        A formatting function for the numerical values in the summary. Default is scientific notation with 4 decimal places.
    Returns
    -------
    pd.DataFrame
        A DataFrame containing the summary of the residual analysis, formatted as specified.
    """

    summary = (
        pd.DataFrame({
            "Muon": ["Muon 1", "Muon 2"],
            "Mean Residual": [
                residual_analysis_1["Mean"],
                residual_analysis_2["Mean"]
            ],
            "Std. Dev.": [
                residual_analysis_1["Standard Deviation"],
                residual_analysis_2["Standard Deviation"]
            ],
            "Max. Abs. Difference": [
                residual_analysis_1["Maximum Absolute Difference"],
                residual_analysis_2["Maximum Absolute Difference"]
            ],
            "Difference Limits": [
                residual_analysis_1["Difference Limits"],
                residual_analysis_2["Difference Limits"]
            ]
        })
        .rename(index=lambda x: x + 1)
        .style
        .set_caption(caption)
        .set_table_styles(TABLE_STYLES)
        .format(
            subset=[
                "Mean Residual",
                "Std. Dev.",
            ],
            formatter=format
        )
    )

    return summary


def transverse_momentum_calculation(p_x, p_y):
    """
    Calculates the transverse momentum (p_T) given the x and y components of momentum.

    Parameters
    ----------
    p_x: array-like 
        The x-component of momentum.
    p_y: array-like
        The y-component of momentum.

    Returns
    -------
    array-like
    The calculated transverse momentum (p_T).
    """

    p_T = np.sqrt(p_x**2 + p_y**2)

    return p_T


def total_momentum_calculation(p_x, p_y, p_z):
    """
    Calculates the total momentum (p) given the x, y, and z components of momentum.

    Parameters
    ----------
    p_x: array-like
        The x-component of momentum.
    p_y: array-like
        The y-component of momentum.
    p_z: array-like
        The z-component of momentum.

    Returns
    -------
    array-like
        The calculated total momentum (p).
    """

    p = np.sqrt(p_x**2 + p_y**2 + p_z**2)

    return p


def pseudorapidity_calculation(p_total, p_z):
    """
    Calculates the pseudorapidity (eta) given the total momentum and the z-component of momentum.

    Parameters
    ----------
    p_total: array-like
        The total momentum.
    p_z: array-like
        The z-component of momentum.

    Returns
    -------
    array-like
        The calculated pseudorapidity (eta).
    """

    eta = 0.5 * np.log((p_total + p_z) / (p_total - p_z))

    return eta


def azimuthal_angle_calculation(p_x, p_y):
    """
    Calculates the azimuthal angle (phi) given the x and y components of momentum.

    Parameters
    ----------
    p_x: array-like
        The x-component of momentum.
    p_y: array-like
        The y-component of momentum.

    Returns
    -------
    array-like
        The calculated azimuthal angle (phi).
    """

    phi = np.arctan2(p_y, p_x)

    return phi


def azimuthal_angle_residual(phi_calculated, phi_provided):
    """
    Calculates the residual of the azimuthal angle (phi) between calculated and provided values.

    Parameters
    ----------
    phi_calculated: array-like
        The calculated azimuthal angle.
    phi_provided: array-like
        The provided azimuthal angle.

    Returns
    -------
    array-like
        The residual of the azimuthal angle.
    """

    residual = phi_calculated - phi_provided

    # Wrap residuals to the interval [-pi, pi] in a vectorized way
    residual = np.where(residual > np.pi,
                        residual - 2 * np.pi,
                        residual)

    residual = np.where(residual < -np.pi,
                        residual + 2 * np.pi,
                        residual)

    return residual


def anamolous_events_validation(
    dataset,
    pt_calc,
    pt_residual,
    summary_caption="",
    outlier_table_caption=""
):
    """
    Validates the transverse momentum calculations by identifying events with significant discrepancies.

    Parameters
    ----------
    dataset: pandas.DataFrame
        The dataset containing the events to validate.
    pt_calc: array-like
        The calculated transverse momentum values.
    pt_residual: array-like
        The residuals of the transverse momentum calculations.
    summary_caption: str, optional
        The caption for the summary table. The default is an empty string.
    outlier_table_caption: str, optional
        The caption for the outlier table. The default is an empty string.

    Returns
    -------
    tuple of pandas.DataFrame
        A summary of the validation results and a table of the anomalous events.
    """

    threshold = 1.0  # GeV

    pt1_outliers = dataset.copy()
    pt1_outliers["Calculated pt"] = pt_calc
    pt1_outliers["Residual"] = pt_residual
    pt1_outliers["Absolute Residual"] = np.abs(pt_residual)
    pt1_outliers["Relative Error (%)"] = (
        100 * np.abs(pt_residual) / pt1_outliers["pt1"]
    )

    pt1_outliers = (
        pt1_outliers[pt1_outliers["Absolute Residual"] > threshold]
        .sort_values("Absolute Residual", ascending=False)
    )

    summary = (
        pd.DataFrame({
            "Quantity": [
                "Total events",
                "Events with |Residual| > 1 GeV",
                "Percentage of dataset"
            ],
            "Value": [
                len(dataset),
                len(pt1_outliers),
                f"{100*len(pt1_outliers)/len(dataset):.3f}%"
            ]
        })
        .style
        .hide(axis="index")
        .set_caption(summary_caption)
        .set_table_styles(TABLE_STYLES)
    )

    outlier_table = (
        pt1_outliers[
            [
                "Run",
                "Event",
                "E1",
                "px1",
                "py1",
                "pz1",
                "pt1",
                "Calculated pt",
                "Residual",
                "Relative Error (%)"
            ]
        ]
        .head(10)
        .style
        .set_caption(outlier_table_caption)
        .hide(axis="index")
        .set_table_styles(TABLE_STYLES)
        .format({
            "E1": "{:.3f}",
            "px1": "{:.3f}",
            "py1": "{:.3f}",
            "pz1": "{:.3f}",
            "pt1": "{:.3f}",
            "Calculated pt": "{:.3f}",
            "Residual": "{:.3f}",
            "Relative Error (%)": "{:.2f}"
        })
    )

    return summary, outlier_table
