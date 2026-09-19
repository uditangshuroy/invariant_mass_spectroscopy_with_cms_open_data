"""
fit_peaks.py
============

Functions for fitting peaks in histograms, such as the Z boson peak, using Gaussian and other models.

Author: Uditangshu Roy
The University of Manchester
Date: August 2026
"""

import numpy as np
from scipy.special import voigt_profile
from scipy.stats import chi2
from scipy.optimize import curve_fit


def gaussian_peak(x, A, mu, sigma, c0, c1):
    """
    Gaussian function with a linear background, used for fitting peaks in histograms.

    Parameters
    ----------
    x: array-like
        The x-values for the fit.
    A: float
        The amplitude of the Gaussian peak.
    mu: float
        The mean of the Gaussian peak.
    sigma: float
        The standard deviation of the Gaussian peak.
    c0: float
        The y-intercept of the linear background.
    c1: float
        The slope of the linear background.

    Returns
    -------
    tuple of array-like
        The fitted values and the FWHM of the Gaussian peak.
    """

    return A * np.exp(-0.5 * ((x - mu) / sigma)**2) + c0 + c1 * (x - mu)


def gaussian_fwhm(sigma, sigma_error):
    """
    Calculate the Full Width at Half Maximum (FWHM) of a Gaussian distribution, along with its error.

    Parameters
    ----------
    sigma: float
        The standard deviation of the Gaussian distribution.
    sigma_error: float
        The error in the standard deviation of the Gaussian distribution.

    Returns
    -------
    tuple of float
        The FWHM of the Gaussian distribution and its error.
    """

    return (
        2 * np.sqrt(2 * np.log(2)) * sigma,
        2 * np.sqrt(2 * np.log(2)) * sigma_error
    )


def breit_wigner_peak(x, A, mu, gamma, c0, c1):
    """
    Breit-Wigner function with a linear background, used for fitting peaks in histograms.

    Parameters
    ----------
    x: array-like
        The x-values for the fit.
    A: float
        The amplitude of the Breit-Wigner peak.
    mu: float
        The mean of the Breit-Wigner peak.
    gamma: float
        The width of the Breit-Wigner peak.
    c0: float
        The y-intercept of the linear background.
    c1: float
        The slope of the linear background.

    Returns
    -------
    tuple of array-like
        The fitted values and the FWHM of the Breit-Wigner peak.
    """

    return A * gamma**2 / ((x - mu)**2 + gamma**2) + c0 + c1 * (x - mu)


def breit_wigner_fwhm(gamma, gamma_error):
    """
    Calculate the Full Width at Half Maximum (FWHM) of a Breit-Wigner distribution, along with its error.

    Parameters
    ----------
    gamma: float
        The width of the Breit-Wigner distribution.
    gamma_error: float
        The error in the width of the Breit-Wigner distribution.

    Returns
    -------
    tuple of float
        The FWHM of the Breit-Wigner distribution and its error.
    """

    return (
        2 * gamma,
        2 * gamma_error
    )


def voigt_peak(x, A, mu, sigma, gamma, c0, c1):
    """
    Voigt function with a linear background, used for fitting peaks in histograms.

    Parameters
    ----------
    x: array-like
        The x-values for the fit.
    A: float
        The amplitude of the Voigt peak.
    mu: float
        The mean of the Voigt peak.
    sigma: float
        The standard deviation of the Gaussian component of the Voigt peak.
    gamma: float
        The width of the Lorentzian component of the Voigt peak.
    c0: float
        The y-intercept of the linear background.
    c1: float
        The slope of the linear background.

    Returns
    -------
    tuple of array-like
        The fitted values and the FWHM of the Voigt peak.
    """

    return A * voigt_profile(x - mu, sigma, gamma) + c0 + c1 * (x - mu)


def voigt_fwhm(sigma, gamma):
    """
    Calculate the Full Width at Half Maximum (FWHM) of a Voigt distribution.

    Parameters
    ----------
    sigma: float
        The standard deviation of the Gaussian component of the Voigt distribution.
    gamma: float
        The width of the Lorentzian component of the Voigt distribution.

    Returns
    -------
    float
        The FWHM of the Voigt distribution.
    """

    # ==========================================
    # Approximate FWHM of the Voigt profile using the empirical formula from Olivero and Longbothum (1977)
    # Reference: Olivero, J. J., & Longbothum, R. L. (1977). Empirical fits to the Voigt line width: A brief review.
    #   Journal of Quantitative Spectroscopy and Radiative Transfer, 17(2), 233-236.
    # URL: https://doi.org/10.1016/0022-4073(77)90161-3
    # Accessed: 12 Aug 2026
    # ==========================================

    return 0.5343 * (2 * gamma) + np.sqrt(0.2169 * (2 * gamma)**2 + (2 * np.sqrt(2 * np.log(2)) * sigma)**2)


def voigt_fwhm_error(sigma, gamma, covariance_matrix):
    """
    Calculate the error in the Full Width at Half Maximum (FWHM) of a Voigt distribution using error propagation.

    Parameters
    ----------
    sigma: float
        The standard deviation of the Gaussian component of the Voigt distribution.
    gamma: float
        The width of the Lorentzian component of the Voigt distribution.
    covariance_matrix: array-like
        The covariance matrix of the fitted parameters, used to calculate the error in FWHM.

    Returns
    -------
    float
        The error in the FWHM of the Voigt distribution.
    """

    covariance_sigma_gamma = covariance_matrix[2, 3]

    sigma_error = np.sqrt(covariance_matrix[2, 2])
    gamma_error = np.sqrt(covariance_matrix[3, 3])

    delta = 1e-7  # Arbitrary delta for numerical differentiation, much smaller than the expected errors in sigma and gamma

    # Compute the derivatives of the FWHM with respect to sigma and gamma using central difference approximation

    d_fwhm_d_sigma = (
        voigt_fwhm(sigma + delta, gamma)
        - voigt_fwhm(sigma - delta, gamma)
    ) / (2 * delta)

    d_fwhm_d_gamma = (
        voigt_fwhm(sigma, gamma + delta)
        - voigt_fwhm(sigma, gamma - delta)
    ) / (2 * delta)

    variance = (
        (d_fwhm_d_sigma * sigma_error)**2 +
        (d_fwhm_d_gamma * gamma_error)**2 +
        2 * d_fwhm_d_sigma * d_fwhm_d_gamma * covariance_sigma_gamma
    )

    return np.sqrt(variance)


def initial_parameter_guess(x_fit, y_fit):
    """
    Provides an initial guess for the parameters of the peak fitting functions.

    Parameters
    ----------
    x_fit: array-like
        The x-values for the fit.
    y_fit: array-like
        The y-values for the fit.

    Returns
    -------
    dict
        A dictionary containing initial guesses for the parameters of Gaussian, Breit-Wigner, and Voigt peaks.
    """

    peak_index = np.argmax(y_fit)

    mu_guess = x_fit[peak_index]

    background_guess = np.min(y_fit)

    amplitude_guess = np.max(y_fit) - background_guess

    x_span = np.ptp(x_fit)  # Dynamic width guess (about 5% of total fit range)
    width_guess = np.clip(x_span * 0.05, 0.01, 5.0)

    return {
        "gaussian": {
            "A": amplitude_guess,
            "mu": mu_guess,
            "sigma": width_guess,
            "c0": background_guess,
            "c1": 0.0
        },
        "breit_wigner": {
            "A": amplitude_guess,
            "mu": mu_guess,
            "gamma": width_guess,
            "c0": background_guess,
            "c1": 0.0
        },
        "voigt": {
            "A": amplitude_guess,
            "mu": mu_guess,
            "sigma": width_guess,
            "gamma": width_guess,
            "c0": background_guess,
            "c1": 0.0
        }
    }


def popt_and_pcov(model, x, y, y_error, initial_guess=None):
    """
    Fit a model to data and return the optimal parameters and covariance matrix.

    Parameters
    ----------
    model: callable
        The model function to fit.
    x: array-like
        The x-values for the fit.
    y: array-like
        The y-values for the fit.
    y_error: array-like
        The errors in the y-values.
    initial_guess: array-like, optional
        Initial guess for the parameters. Default is None, which means the fitting algorithm will use its own initial guess.

    Returns
    -------
    tuple of array-like
        Optimal parameters and covariance matrix.
    """

    popt, pcov = curve_fit(model, x, y, sigma=y_error,
                           p0=initial_guess, absolute_sigma=True)

    return popt, pcov


def fit_statistics(model, x, y, y_error, parameters):
    """
    Calculate goodness-of-fit statistics for a fitted model.

    Parameters
    ----------
    model: callable
        The fitted model function.
    x: array-like
        The x-values for the fit.
    y: array-like
        The y-values for the fit.
    y_error: array-like
        The errors in the y-values.
    parameters: array-like
        The fitted parameters.

    Returns
    -------
    dict
        Chi-squared, degrees of freedom, reduced chi-squared,
        p-value, AIC and BIC.
    """

    y_model = model(x, *parameters)

    residuals = y - y_model

    chi_squared = np.sum(
        (residuals / y_error)**2
    )

    degrees_of_freedom = (
        len(y) - len(parameters)
    )

    reduced_chi_squared = (
        chi_squared / degrees_of_freedom
    )

    p_value = chi2.sf(
        chi_squared,
        degrees_of_freedom
    )

    aic = chi_squared + 2 * len(parameters)

    bic = (
        chi_squared
        + len(parameters) * np.log(len(y))
    )

    return {
        "Chi-squared": chi_squared,
        "Degrees of Freedom": degrees_of_freedom,
        "Reduced Chi-squared": reduced_chi_squared,
        "p-value": p_value,
        "AIC": aic,
        "BIC": bic
    }
