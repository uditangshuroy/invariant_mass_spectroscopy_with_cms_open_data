"""
utilities.py
============

General utility functions used throughout the CMS Z-Boson Analysis project.

These functions provide common data inspection, validation and formatting routines that are reused 
across multiple notebooks.

Author: Uditangshu Roy
The University of Manchester
Date: August 2026
"""

# Imports
import pandas as pd
import numpy as np

# Common column groups
IDENTIFIER_COLUMNS = [
    "Run",
    "Event"
]

ADDITIONAL_COLUMNS = [  # For the larger dataset of dimuon events
    "E1", "E2",
    "M",
]

KINEMATIC_COLUMNS = [
    "pt1", "pt2",
    "eta1", "eta2",
    "phi1", "phi2",
    "Q1", "Q2"
]

TRACK_COLUMNS = [
    "dxy1", "dxy2",
    "iso1", "iso2"
]

# For styling summary tables in notebooks
TABLE_STYLES = [
    {
        "selector": "caption",
        "props": [
            ("caption-side", "top"),
            ("font-size", "1.1em"),
            ("color", "#333333"),
            ("padding-bottom", "10px"),
            ("text-align", "left"),
        ],
    },
    {
        "selector": "th",
        "props": [
            ("text-align", "center"),
            ("font-weight", "bold"),
        ],
    },
]


def make_formatter(
    decimals=4,
    small_number_precision=3,
    small_number_threshold=1e-3
):
    """
    Returns a formatting function that formats numbers with a specified number of decimal places, 
    while also handling scientific notation for very small numbers.

    Parameters
    ----------
    decimals: int, optional
        The number of decimal places to display for regular floating-point numbers. Default is 4.
    small_number_precision: int, optional
        The number of decimal places to display for very small numbers in scientific notation. Default is 3.
    small_number_threshold: float, optional
        The threshold below which numbers are considered "small" and formatted in scientific notation. Default is 1e-3.

    Returns
    -------
    callable
        A formatting function.
    """

    return lambda x: (
        f"{x:.{small_number_precision}e}" if isinstance(x, (int, float)) and 0 < abs(x) < small_number_threshold
        else f"{x:.{decimals}f}".rstrip("0").rstrip(".") if isinstance(x, (int, float))
        else str(x)
    )


def dataset_summary(
        df,
        columns=None
):
    """
    Return a concise statistical summary.

    Parameters
    ----------
    df: pandas.DataFrame
        Input DataFrame.

    columns: list, optional
        List of columns to summarise.
        If None, all numerical columns are used.

    Returns
    -------
    DataFrame
        Mean, standard deviation,
        minimum and maximum.
    """

    if columns is None:
        columns = df.select_dtypes(include=np.number).columns

    summary = (
        df[columns]
        .agg(["mean", "std", "min", "max"])
        .T
    )

    summary.columns = [
        "Mean",
        "Standard Deviation",
        "Minimum",
        "Maximum"
    ]

    return summary.round(3)


def missing_values(df):
    """
    Display missing values for every column.

    Parameters
    ----------
    df: pandas.DataFrame
        Input DataFrame.

    Returns
    -------
    DataFrame
        Number and percentage of missing values for each column.
    """

    missing = pd.DataFrame({
        "Missing Values": df.isnull().sum(),
        "Percentage (%)": (
            100 * df.isnull().mean()
        ).apply(lambda x: f"{x:.2f}")
    })

    return missing


def dataset_information(df):
    """
    Return information about each variable.

    Parameters
    ----------
    df: pandas.DataFrame
        Input DataFrame.

    Returns
    -------
    DataFrame
        Data type and number of non-null entries for each column.
    """

    info = pd.DataFrame({
        "Data Type": df.dtypes,
        "Non-Null Entries": df.count()
    })

    return info


def dataset_dimensions(df):
    """
    Return dataset dimensions.

    Parameters
    ----------
    df: pandas.DataFrame
        Input DataFrame.

    Returns
    -------
    tuple
        Number of rows and columns in the DataFrame.
    """

    rows = len(df)
    columns = len(df.columns)

    print(f"Rows    : {rows:,}")
    print(f"Columns : {columns}")

    return rows, columns


def event_statistics(df):
    """
    Print basic dataset statistics.

    Parameters
    ----------
    df: pandas.DataFrame
        Input DataFrame.
    """

    print(f"Total Events   : {len(df):,}")
    print(f"Variables      : {len(df.columns)}")
    print(f"Unique Runs    : {df['Run'].nunique()}")
    print(f"Unique Events  : {df['Event'].nunique()}")


def variable_list(df):
    """
    Return all variables and data types.

    Parameters
    ----------
    df: pandas.DataFrame
        Input DataFrame.

    Returns
    -------
    DataFrame
        Variable names and data types.
    """

    variables = pd.DataFrame({
        "Variable": df.columns,
        "Data Type": df.dtypes.values
    })

    return variables


def get_value_counts(series):
    """
    Return category labels and counts from a pandas Series.

    Parameters
    ----------
    series : pandas.Series
        Input Series.

    Returns
    -------
    tuple
        Category labels and their corresponding counts.
    """

    counts = series.value_counts()

    return counts.index, counts.values


def dict_to_summary_df(data_dict,
                       metric_col="Quantity",
                       value_col="Value",
                       caption="",
                       format_function=make_formatter()):
    """
    Converts a single-level dictionary of statistics/metrics into a Pandas DataFrame.

    Parameters:
    -----------
    data_dict : dict
        Dictionary containing metric names as keys and values as scalars/strings.
    metric_col : str, optional
        Column header for the metric names. Default is "Quantity".
    value_col : str, optional
        Column header for the values. Default is "Value".
    caption : str, optional
        Caption for the summary table. Default is an empty string.
    format_function : callable, optional
        Function to format the values. Default is the `make_formatter()` function.

    Returns:
    --------
    pd.DataFrame
        A DataFrame with two columns, with proper .style chaining.
    """

    df = pd.DataFrame(list(data_dict.items()), columns=[metric_col, value_col])

    return (df
            .rename(index=lambda x: x + 1)
            .style
            .hide(axis="index")
            .set_caption(caption)
            .set_table_styles(TABLE_STYLES)
            .format(format_function)
            )


def multiple_dicts_to_summary_df(
    data_dicts,
    metric_col="Quantity",
    keys_list=None,
    caption="",
    format_function=make_formatter(
        decimals=2,
        small_number_precision=1
    )
):
    """
    Converts multiple dictionaries of statistics into a styled Pandas DataFrame.

    Parameters:
    -----------
    data_dicts : dict
        A dictionary mapping column names to data dictionaries.
        Example: {"Muon 1": dict1, "Muon 2": dict2}
    metric_col : str, optional
        Column header for the metric names (the row labels). Default is "Quantity".
    keys_list : list, optional
        A specific list of keys to dictate the row order. If None, it automatically 
        extracts all unique keys found across all dictionaries.
    caption : str, optional
        Caption for the summary table. Default is an empty string.
    format_function : callable, optional
        Function to format the values. Default is `make_formatter()`.

    Returns:
    --------
    pandas.io.formats.style.Styler
        A styled table object ready for display.
    """

    if keys_list is None:
        keys_list = []
        for d in data_dicts.values():
            for k in d.keys():
                if k not in keys_list:
                    keys_list.append(k)

    # Data columns
    df_data = {metric_col: keys_list}
    for col_name, d in data_dicts.items():
        # Using "-" if the dictionary doesn't have the key
        df_data[col_name] = [d.get(k, "-") for k in keys_list]

    df = pd.DataFrame(df_data)

    value_cols = list(data_dicts.keys())

    # Additional styling local to this setup

    local_table_styles = TABLE_STYLES + [
        {
            "selector": "td",
            "props": [
                ("text-align", "center")
            ],
        },
        {
            "selector": "td:first-child",
            "props": [
                # Left-align first data column for metric names.
                ("text-align", "left"),
            ],
        }
    ]

    return (df
            .style
            .hide(axis="index")
            .set_caption(caption)
            .set_table_styles(local_table_styles)
            .format(format_function, subset=value_cols)
            )
