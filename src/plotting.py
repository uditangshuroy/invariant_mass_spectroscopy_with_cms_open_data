"""
plotting.py
============

Plotting functions for the CMS Z Boson Analysis project.

These functions provide common plotting routines that are reused across multiple notebooks.

Author: Uditangshu Roy
The University of Manchester
Date: August 2026
"""

# Imports
import matplotlib.pyplot as plt
import numpy as np


def set_plot_style():
    """
    Sets a consistent plotting style for the project.
    """

    plt.rcParams["figure.figsize"] = (9, 5.625)  # 1:1.6 aspect ratio
    plt.rcParams["figure.dpi"] = 120

    plt.rcParams["font.size"] = 11
    plt.rcParams["axes.labelsize"] = 12
    plt.rcParams["axes.titlesize"] = 13

    plt.rcParams["legend.fontsize"] = 10

    plt.rcParams["xtick.direction"] = "in"
    plt.rcParams["ytick.direction"] = "in"

    plt.rcParams["axes.grid"] = True


def histogram_peak(data, bins=100):
    """
    Estimate the peak position of a histogram.

    Parameters
    ----------
    data: array-like
        Data for the histogram.
    bins: int, optional
        Number of bins for the histogram. Default is 100.

    Returns
    -------
    float
        The estimated peak position.
    """

    counts, edges = np.histogram(data, bins=bins)

    peak_bin = np.argmax(counts)

    return (edges[peak_bin] + edges[peak_bin + 1]) / 2


def histogram_bin_centers(data, bins=100):
    """
    Calculate the bin centers of a histogram.

    Parameters
    ----------
    data: array-like
        Data for the histogram.
    bins: int, optional
        Number of bins for the histogram. Default is 100.

    Returns
    -------
    tuple of numpy.ndarray
        The bin counts and centers.
    """

    counts, edges = np.histogram(data, bins=bins)

    return counts, ((edges[:-1] + edges[1:]) / 2)


def plot_histogram(
    data,
    bins=50,
    xlabel="",
    ylabel="Events",
    title="",
    color="royalblue",
    vlines=None,
    xlimit=None,
    ylimit=None,
    caption="",
    save_path=None,
    alt_caption=""
):
    """
    Plot a histogram.

    Parameters
    ----------
    data: array-like
        Data to be plotted.
    bins: int, optional
        Number of bins for the histogram. Default is 50.
    xlabel: str, optional
        Label for the x-axis. Default is an empty string.
    ylabel: str, optional
        Label for the y-axis. Default is "Events".
    title: str, optional
        Title for the plot. Default is an empty string.
    color: str, optional
        Colour for the histogram bars. Default is "royalblue".
    vlines : list of tuples
        Each tuple should be (x_position, label, colour).
        Example:
        [
            (91.03, "Peak = 91.03 GeV", "red"),
            (91.19, "PDG = 91.19 GeV", "black")
        ]
    xlimit: tuple, optional
        Limit for the x-axis. Default is None.
    ylimit: tuple, optional
        Limit for the y-axis. Default is None.
    caption: str, optional
        Caption for the plot. Default is an empty string.
    save_path: str, optional
        Path to save the plot. Default is None.
    alt_caption: str, optional
        Caption for the plot if figure is saved. Default is an empty string.
    """

    fig_saved = False

    plt.figure()

    plt.hist(
        data,
        bins=bins,
        color=color,
        edgecolor="black",
        histtype="stepfilled"
    )

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)

    plt.tight_layout()

    if xlimit:
        plt.xlim(xlimit)

    if ylimit:
        plt.ylim(ylimit)

    if vlines:
        for x, label, colour in vlines:
            plt.axvline(
                x,
                label=label,
                color=colour,
                linestyle="--",
                linewidth=2
            )

    plt.grid(alpha=0.3)

    _, labels = plt.gca().get_legend_handles_labels()
    if labels:
        plt.legend()

    plt.tight_layout()

    if save_path:
        # Attach alt_caption (or fallback to caption) for the saved image file
        save_caption_text = alt_caption if alt_caption else caption
        if save_caption_text:
            alt_txt = plt.figtext(
                0, -0.08, save_caption_text, wrap=True, horizontalalignment='left', fontsize=10)

        plt.savefig(save_path, dpi=300, bbox_inches="tight")
        fig_saved = True

        if save_caption_text:
            alt_txt.remove()

    if caption:
        plt.figtext(0, -0.08, caption, wrap=True,
                    horizontalalignment='left', fontsize=10)


def plot_overlay_histogram(
    data1,
    data2,
    bins=50,
    xlabel="",
    ylabel="Events",
    title="",
    colors=("royalblue", "orange"),
    label1="Muon 1",
    label2="Muon 2",
    xlimit=None,
    ylimit=None,
    vlines=None,
    caption="",
    save_path=None,
    alt_caption=""
):
    """
    Plot two histograms together.

    Parameters
    ----------
    data1: array-like
        Data for the first histogram.
    data2: array-like
        Data for the second histogram.
    bins: int, optional
        Number of bins for the histograms. Default is 50.
    xlabel: str, optional
        Label for the x-axis. Default is an empty string.
    ylabel: str, optional
        Label for the y-axis. Default is "Events".
    title: str, optional
        Title for the plot. Default is an empty string.
    colors: tuple, optional
        Colors for the two histograms. Default is ("royalblue", "orange").
    label1: str, optional
        Label for the first histogram. Default is "Muon 1".
    label2: str, optional
        Label for the second histogram. Default is "Muon 2".
    vlines : list of tuples
        Each tuple should be (x_position, label, colour).
        Example:
        [
            (91.03, "Peak = 91.03 GeV", "red"),
            (91.19, "PDG = 91.19 GeV", "black")
        ]
    xlimit: tuple, optional
        Limit for the x-axis. Default is None.
    ylimit: tuple, optional
        Limit for the y-axis. Default is None.
    caption: str, optional
        Caption for the plot. Default is an empty string.
    save_path: str, optional
        Path to save the plot. Default is None.
    alt_caption: str, optional
        Caption for the plot if figure is saved. Default is an empty string.
    """

    fig_saved = False

    plt.figure()

    plt.hist(
        data1,
        bins=bins,
        alpha=0.6,
        color=colors[0],
        edgecolor="black",
        histtype="stepfilled",
        label=label1
    )

    plt.hist(
        data2,
        bins=bins,
        alpha=0.6,
        color=colors[1],
        edgecolor="black",
        histtype="stepfilled",
        label=label2
    )

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)

    if xlimit:
        plt.xlim(xlimit)

    if ylimit:
        plt.ylim(ylimit)

    if vlines:
        for x, label, colour in vlines:
            plt.axvline(
                x,
                label=label,
                color=colour,
                linestyle="--",
                linewidth=2
            )

    plt.grid(alpha=0.3)

    _, labels = plt.gca().get_legend_handles_labels()
    if labels:
        plt.legend()

    plt.tight_layout()

    if save_path:
        # Attach alt_caption (or fallback to caption) for the saved image file
        save_caption_text = alt_caption if alt_caption else caption
        if save_caption_text:
            alt_txt = plt.figtext(
                0, -0.08, save_caption_text, wrap=True, horizontalalignment='left', fontsize=10)

        plt.savefig(save_path, dpi=300, bbox_inches="tight")
        fig_saved = True

        if save_caption_text:
            alt_txt.remove()

    if caption:
        plt.figtext(0, -0.08, caption, wrap=True,
                    horizontalalignment='left', fontsize=10)


def plot_mass_fits(
    x_data,
    y_data,
    y_error,
    fits_dict,
    x_limits=None,
    y_limits=None,
    x_plot=None,
    xlabel="",
    ylabel="Events",
    title="",
    vlines=None,
    save_path=None,
    caption="",
    alt_caption=""
):
    """
    Plots experimental data points with error bars overlaid with fitted curves.

    Parameters:
    -----------
    x_data, y_data : array-like
        Data points.
    y_error : array-like
        Uncertainties on y_data.
    fits_dict : dict
        Dictionary of fit curves, e.g. {"Gaussian": (y_gauss, "red"), "Voigt": (y_voigt, "blue")}.
    x_limits, y_limits : tuple, optional
        Axis limits for the plot. Default is None.
    x_plot : array-like, optional
        Smooth x-values for fit curves. Defaults to x_data if None.
    colours : dict or None, optional
        Dictionary mapping fit labels to colours. If None, default colours are used.
    vlines : list of tuples
            Each tuple should be (x_position, label, colour).
            Example:
            [
                (91.03, "Peak = 91.03 GeV", "red"),
                (91.19, "PDG = 91.19 GeV", "black")
            ]
    xlabel, ylabel, title : str, optional
        Labels and title for the plot.
    caption: str, optional
        Caption for the plot. Default is an empty string.
    save_path: str, optional
        Path to save the plot. Default is None.
    alt_caption: str, optional
        Caption for the plot if figure is saved. Default is an empty string.
    """

    fig_saved = False

    if x_plot is None:
        x_plot = x_data

    plt.figure()

    # Plot data with error bars
    plt.errorbar(
        x_data,
        y_data,
        yerr=y_error,
        fmt="o",
        color="royalblue",
        markersize=3,
        capsize=2,
        label="Data"
    )

    # Dynamically plots each fitted curve
    for label, item in fits_dict.items():
        # fits_dict values are tuples of (y_fit, color)
        y_fit, color = item

        plt.plot(x_plot, y_fit, label=label, color=color)

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)

    if x_limits:
        plt.xlim(x_limits)

    if y_limits:
        plt.ylim(y_limits)

    if vlines:
        for x, label, colour in vlines:
            plt.axvline(
                x,
                label=label,
                color=colour,
                linestyle="--",
                linewidth=2
            )

    plt.grid(alpha=0.3)

    _, labels = plt.gca().get_legend_handles_labels()
    if labels:
        plt.legend()

    plt.tight_layout()

    if save_path:
        # Attach alt_caption (or fallback to caption) for the saved image file
        save_caption_text = alt_caption if alt_caption else caption
        if save_caption_text:
            alt_txt = plt.figtext(
                0, -0.08, save_caption_text, wrap=True, horizontalalignment='left', fontsize=10)

        plt.savefig(save_path, dpi=300, bbox_inches="tight")
        fig_saved = True

        if save_caption_text:
            alt_txt.remove()

    if caption:
        plt.figtext(0, -0.08, caption, wrap=True,
                    horizontalalignment='left', fontsize=10)

    plt.show()

    if fig_saved:
        print("Figure saved at:", save_path)


def plot_scatter(
    x_data,
    y_datasets,
    xlabel="",
    ylabel="",
    title="",
    alpha=0.5,
    size=12,
    color="blue",
    label=None,
    vlines=None,
    hlines=None,
    caption="",
    save_path=None,
    alt_caption=""
):
    """
    Plot a scatter graph.

    Parameters
    ----------
    x_data: array-like
        The x dataset to be plotted. Common data for all y datasets.
    y_datasets : array-like OR list of tuples
        Either a single y-dataset array/Series OR a list of tuples formatted 
        as [(y_data, label, color), ...]
    xlabel: str, optional
        Label for the x-axis. Default is an empty string.
    ylabel: str, optional
        Label for the y-axis. Default is an empty string.
    title: str, optional
        Title for the plot. Default is an empty string.
    alpha: float, optional
        Transparency of the points. Default is 0.5.
    size: float, optional
        Size of the points. Default is 12.
    color : str, optional
        Color for single-dataset calls. Default is 'blue'.
    label : str, optional
        Legend label for single-dataset calls.
    vlines : list of tuples
                Each tuple should be (x_position, label, colour).
                Example:
                [
                    (91.03, "Peak = 91.03 GeV", "red"),
                    (91.19, "PDG = 91.19 GeV", "black")
                ]
    hlines : list of tuples
                Each tuple should be (y_position, label, colour).
                Example:
                [
                    (0.5, "Median = 0.5", "blue"),
                    (0.8, "90% Quantile = 0.8", "green")
                ]
    caption: str, optional
        Caption for the plot. Default is an empty string.
    save_path: str, optional
        Path to save the plot. Default is None.
    alt_caption: str, optional
        Caption for the plot if figure is saved. Default is an empty string.
    """

    fig_saved = False
    plt.figure()

    # Detect if y_datasets is a single dataset (1D array/Series) or a list of tuples

    is_single_dataset = False
    if isinstance(y_datasets, (list, tuple)) and len(y_datasets) > 0:
        # Check if first element is a 3-element tuple (y_data, label, color)
        if not (isinstance(y_datasets[0], tuple) and len(y_datasets[0]) == 3):
            is_single_dataset = True
    else:
        is_single_dataset = True

    if is_single_dataset:
        datasets = [(y_datasets, label, color)]
    else:
        datasets = y_datasets

    # Plot scatter points
    for y_data, lbl, c in datasets:
        plt.scatter(
            x_data,
            y_data,
            label=lbl,
            s=size,
            alpha=alpha,
            c=c
        )

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)

    if vlines:
        for x, lbl, c in vlines:
            plt.axvline(
                x,
                label=lbl,
                color=c,
                linestyle="--",
                linewidth=2
            )

    # Horizontal reference lines
    if hlines:
        for y, lbl, c in hlines:
            plt.axhline(
                y,
                label=lbl,
                color=c,
                linestyle="--",
                linewidth=2
            )

    plt.grid(alpha=0.3)

    # Only show legend if at least one label was provided
    _, labels = plt.gca().get_legend_handles_labels()
    if labels:
        plt.legend()

    plt.tight_layout()

    if (not save_path) and caption:
        plt.figtext(0, -0.08, caption, wrap=True,
                    horizontalalignment='left', fontsize=10)

    if save_path:
        plt.figtext(0, -0.08, alt_caption, wrap=True,
                    horizontalalignment='left', fontsize=10)
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
        fig_saved = True

    plt.show()

    plt.close()

    if fig_saved:
        print("Figure saved at:", save_path)


def plot_bar(
    categories,
    values,
    width=0.6,
    xlabel="",
    ylabel="Events",
    title="",
    caption="",
    save_path=None,
    alt_caption=""
):
    """
    Plot a bar chart.

    Parameters
    ----------
    categories: array-like
        Categories for the x-axis.
    values: array-like
        Values for the y-axis.
    width: float, optional
        Width of the bars. Default is 0.6.
    xlabel: str, optional
        Label for the x-axis. Default is an empty string.
    ylabel: str, optional
        Label for the y-axis. Default is "Events".
    title: str, optional
        Title for the plot. Default is an empty string.
    caption: str, optional
        Caption for the plot. Default is an empty string.
    save_path: str, optional
        Path to save the plot. Default is None.
    alt_caption: str, optional
        Caption for the plot if figure is saved. Default is an empty string.
    """

    fig_saved = False

    plt.figure()

    plt.bar(
        categories,
        values,
        edgecolor="black",
        width=width
    )

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)

    plt.grid(alpha=0.3)

    _, labels = plt.gca().get_legend_handles_labels()
    if labels:
        plt.legend()

    plt.tight_layout()

    if save_path:
        # Attach alt_caption (or fallback to caption) for the saved image file
        save_caption_text = alt_caption if alt_caption else caption
        if save_caption_text:
            alt_txt = plt.figtext(
                0, -0.08, save_caption_text, wrap=True, horizontalalignment='left', fontsize=10)

        plt.savefig(save_path, dpi=300, bbox_inches="tight")
        fig_saved = True

        if save_caption_text:
            alt_txt.remove()

    if caption:
        plt.figtext(0, -0.08, caption, wrap=True,
                    horizontalalignment='left', fontsize=10)

    plt.show()

    if fig_saved:
        print("Figure saved at:", save_path)


def plot_correlation_matrix(
    correlation,
    title="",
    label="Correlation Coefficient",
    save_path=None,
    caption="",
    alt_caption=""
):
    """
    Plot a correlation matrix.

    Parameters
    ----------
    correlation: pandas.DataFrame
        The correlation matrix to plot.
    title: str, optional
        Title for the plot. Default is an empty string.
    label: str, optional
        Label for the colorbar. Default is "Correlation Coefficient".
    save_path: str, optional
        Path to save the plot. Default is None.
    caption: str, optional
        Caption for the plot. Default is an empty string.
    alt_caption: str, optional
        Caption for the plot if figure is saved. Default is an empty string.
    """

    fig_saved = False

    plt.figure(figsize=(8, 6))

    image = plt.imshow(
        correlation,
        cmap="coolwarm",
        vmin=-1,
        vmax=1
    )

    plt.colorbar(image, label=label)

    labels = correlation.columns

    plt.xticks(range(len(labels)), labels, rotation=45)
    plt.yticks(range(len(labels)), labels)

    for i in range(len(labels)):
        for j in range(len(labels)):
            plt.text(
                j,
                i,
                f"{correlation.iloc[i, j]:.2f}",
                ha="center",
                va="center",
                fontsize=8
            )

    plt.title(title)

    plt.grid(alpha=0.3)

    _, labels = plt.gca().get_legend_handles_labels()
    if labels:
        plt.legend()

    plt.tight_layout()

    if save_path:
        # Attach alt_caption (or fallback to caption) for the saved image file
        save_caption_text = alt_caption if alt_caption else caption
        if save_caption_text:
            alt_txt = plt.figtext(
                0, -0.08, save_caption_text, wrap=True, horizontalalignment='left', fontsize=10)

        plt.savefig(save_path, dpi=300, bbox_inches="tight")
        fig_saved = True

        if save_caption_text:
            alt_txt.remove()

    if caption:
        plt.figtext(0, -0.08, caption, wrap=True,
                    horizontalalignment='left', fontsize=10)

    plt.show()

    if fig_saved:
        print("Figure saved at:", save_path)


def plot_line(selection_labels,
              selection_counts,
              color="royalblue",
              color_scatter="orange",
              xlabel="Selection Stage",
              ylabel="Events Remaining",
              save_path=None,
              caption="",
              alt_caption=""
              ):
    """
    Plot a line graph showing the number of events remaining after each selection stage.

    Parameters
    ----------
    selection_labels: list or array-like
        The labels for each selection stage.
    selection_counts: list or array-like
        The number of events remaining after each selection stage.
    color: str, optional
        Color for the line. Default is "royalblue".
    color_scatter: str, optional
        Color for the scatter points. Default is "orange".
    xlabel: str, optional
        Label for the x-axis. Default is "Selection Stage".
    ylabel: str, optional
        Label for the y-axis. Default is "Events Remaining".
    save_path: str, optional
        Path to save the plot. Default is None.
    caption: str, optional
        Caption for the plot. Default is an empty string.
    alt_caption: str, optional
        Caption for the plot if figure is saved. Default is an empty string.
    """

    fig_saved = False

    plt.figure(figsize=(8, 5))

    plt.step(
        range(len(selection_counts)),
        selection_counts,
        where="mid",
        color=color,
        linewidth=2
    )

    plt.scatter(
        range(len(selection_counts)),
        selection_counts,
        color=color_scatter
    )

    plt.xticks(
        range(len(selection_labels)),
        selection_labels
    )

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title("Event Cut Flow")

    # Annotations

    for i, count in enumerate(selection_counts):
        plt.annotate(
            str(int(count)),
            xy=(i, count),
            xytext=(0, 3),
            textcoords="offset points",
            ha='center',
            fontsize=10,
            fontweight='bold',
            color='#333333'
        )

    plt.grid(alpha=0.3)

    _, labels = plt.gca().get_legend_handles_labels()
    if labels:
        plt.legend()

    plt.tight_layout()

    if save_path:
        # Attach alt_caption (or fallback to caption) for the saved image file
        save_caption_text = alt_caption if alt_caption else caption
        if save_caption_text:
            alt_txt = plt.figtext(
                0, -0.08, save_caption_text, wrap=True, horizontalalignment='left', fontsize=10)

        plt.savefig(save_path, dpi=300, bbox_inches="tight")
        fig_saved = True

        if save_caption_text:
            alt_txt.remove()

    if caption:
        plt.figtext(0, -0.08, caption, wrap=True,
                    horizontalalignment='left', fontsize=10)

    plt.show()

    if fig_saved:
        print("Figure saved at:", save_path)


def histogram_panel_comparison(
    data1,
    data2,
    title_1="",
    title_2="",
    suptitle="",
    range_1=(1.8, 5.2),
    range_2=(59, 121),
    bins=100,
    x_label="",
    y_label="",
    layout=(1, 2),
    figsize=(14, 5),
    color1="#1f77b4",
    color2="#ff7f0e",
    save_path=None,
    caption="",
    alt_caption=""
):
    """
    Plots two histogram distributions side-by-side or stacked.

    Parameters
    ----------
    data1, data2 : array-like
        Series or arrays of values for the respective subplotsC.
    title_1, title_2 : str, optional
        Titles for the respective subplots. Default is empty string.
    suptitle : str, optional
        Overall title for the figure. Default is empty string.
    range_1, range_2 : tuple, optional
        (min, max) ranges for the histograms. Default is (1.8, 5.2) for data1 and (59, 121) for data2.
    bins : int, optional
        Number of histogram bins. Default is 100.
    x_label, y_label : str, optional
        Axis labels applied to both subplots. Default is empty strings.
    layout : tuple, optional
        Grid dimensions (nrows, ncols). Defaults to (1, 2) side-by-side.
    figsize : tuple, optional
        Dimensions of the matplotlib figure. Default is (14, 5).
    color1, color2 : str, optional
        Fill colors for the histograms. Default is "#1f77b4" (blue) and "#ff7f0e" (orange).
    caption : str, optional
        Caption for the entire figure, placed below the plots. Default is empty string.
    alt_caption: str, optional
        Caption for the plot if figure is saved. Default is an empty string.
    """

    fig_saved = False

    fig, axes = plt.subplots(layout[0], layout[1], figsize=figsize)

    # Flatten axes array to simplify indexing regardless of layout shape
    ax_flat = axes.flatten() if hasattr(axes, 'flatten') else [axes]

    # Subplot 1
    ax_flat[0].hist(
        data1,
        bins=bins,
        range=range_1,
        density=True,
        alpha=0.6,
        color=color1,
        edgecolor='black',
        histtype="stepfilled"
    )

    ax_flat[0].set_title(title_1, fontweight='bold', pad=10)
    ax_flat[0].grid(True, linestyle='--', alpha=0.4)

    # Subplot 2
    ax_flat[1].hist(
        data2,
        bins=bins,
        range=range_2,
        density=True,
        alpha=0.6,
        color=color2,
        edgecolor='black',
        histtype="stepfilled"
    )

    ax_flat[1].set_title(title_2, fontweight='bold', pad=10)
    ax_flat[1].grid(True, linestyle='--', alpha=0.4)

    fig.supxlabel(x_label, fontsize=12, fontweight='bold', y=0.02)
    fig.supylabel(y_label, fontsize=12, fontweight='bold')

    if suptitle:
        plt.suptitle(suptitle, fontsize=16, fontweight='bold', y=1.02)

    plt.grid(alpha=0.3)

    _, labels = plt.gca().get_legend_handles_labels()
    if labels:
        plt.legend()

    plt.tight_layout()

    if save_path:
        # Attach alt_caption (or fallback to caption) for the saved image file
        save_caption_text = alt_caption if alt_caption else caption
        if save_caption_text:
            alt_txt = plt.figtext(
                0, -0.08, save_caption_text, wrap=True, horizontalalignment='left', fontsize=10)

        plt.savefig(save_path, dpi=300, bbox_inches="tight")
        fig_saved = True

        if save_caption_text:
            alt_txt.remove()

    if caption:
        plt.figtext(0, -0.08, caption, wrap=True,
                    horizontalalignment='left', fontsize=10)

    plt.show()

    if fig_saved:
        print("Figure saved at:", save_path)
