import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import precision_recall_curve

sns.set_theme()
from matplotlib.ticker import PercentFormatter

from os.path import join

from typing import Optional, Tuple, List, Dict

from .constants import NESTED_CV_RESULTS_PLOT_FILENAME
from .metric_utils import compute_aucpr

def plot_data_hist(
    data_series: pd.Series,
    x_label: str, 
    rel_freq: bool = False, 
    title: Optional[str] = None,
    fig_size: Tuple[float, float] = (6, 4),
    bar_color: str = 'skyblue',
    bins: float = 20,
) -> None:
    """Plots histogram of a data series

    Args:
        data_series: Series of data for which histogram is being plotted
        x_label:     Label for x-axis of histogram
        rel_freq:    Boolean indicating if the relative frequency should be plotted. Defaults to False
                         in which the frequency or the raw count of binned values is plotted.
        title:       Title for histogram. Defaults to None
        fig_size:    Tuple indicating size of the figure as (horizontal width, vertical length) in 
                         inches. Defaults to (6, 4)
        bar_color:   Color of the bars in the histogram. Defaults to 'skyblue'
        bins:        Number of bins to split data into. Defaults to 20

    """
    fig = plt.figure(figsize = fig_size)
    ax = fig.add_subplot(111)
    median_count = int(np.median(data_series))
    ax.set_ylabel("Relative Frequency") if rel_freq else ax.set_ylabel("Frequency")
    if rel_freq:
        ax.yaxis.set_major_formatter(PercentFormatter())
    ax.set_xlabel(x_label)
    if title:
        ax.set_title(title)
    ax.axvline(x = median_count, color = 'red', label = f'Median {x_label} ({median_count})')
    ax.hist(data_series, bins = bins, edgecolor = 'Black', color = bar_color, weights = np.ones_like(data_series)*100 / len(data_series) if rel_freq else None)
    ax.legend(facecolor = 'w', edgecolor = 'black', shadow = True, frameon = True)
    plt.tight_layout()


def plot_data_box_plot(
    data_series: pd.Series,
    x_label: str,
    title: Optional[str] = None,
    fig_size: Tuple[float, float] = (6, 4),
    width: float = 0.4,
    color: str = 'skyblue'
) -> None:  
    """Plots horizontal box-and-whisker plot of a data series

    Args:
        data_series: Series of data for which box-and-whisker plot is being plotted
        x_label:     Label for x-axis of plot
        title:       Title for box-and-whisker plot. Defaults to None
        fig_size:    Tuple indicating size of the figure as (horizontal width, vertical length) in 
                         inches. Defaults to (6, 4)
        width:       Float indicating width of box in box-and-whisker plot. Defaults to 0.4
        color:       Color of the box in the box-and-whisker plot. Defaults to 'skyblue'

    """
    plt.figure(figsize = fig_size)
    sns.boxplot(x = data_series, color = color, width = width).set(xlabel = x_label)
    if title:
        plt.title(title)
    plt.tight_layout()


def plot_box_plot_data_comparison(
    data_series_list: List[pd.Series],
    dataset_names_list: List[str],
    y_label: str,
    title: Optional[str] = None,
    colors_list: List[str] = None,
    fig_size: Tuple[float] = (6, 5),
    width: float = 0.4,
) -> None:
    """Plots a side-by-side comparison of vertical box-and-whisker plots of a list of data series

    Args:
        data_series_list:   List of data series which are being compared and for which a box-and-whisker plot is being plotted for each series
        dataset_names_list: Ordered list of strings representing the names of the data series in data_series_list.
                                I.e. dataset_names_list[0] is the name of the dataset corresponding to the series at 
                                data_series_list[0]
        y_label:            Label for y-axis of the plot, i.e. the identity of the data being compared
        title:              Title for side-by-side box-and-whisker plot. Defaults to None
        colors_list:        Ordered list of color strings corresponding to the box of each data series in data_series_list, i.e. 
                                colors_list[0] will be the color of the box representing the data in series data_series_list[0].
                                Defaults to None
        fig_size:           Tuple indicating size of the figure as (horizontal width, vertical length) in 
                                inches. Defaults to (6, 5)
        width:              Float indicating the width of the boxes in the plots. Defaults to 0.4
    """
    x_label = 'Dataset'
    dataset_df = pd.DataFrame({y_label: pd.concat(data_series_list, axis = 0),
                               x_label: np.repeat(dataset_names_list, [len(series) for series in data_series_list])})
    plt.figure(figsize = fig_size)
    sns.boxplot(
        x = x_label, 
        y = y_label,
        data = dataset_df,
        palette = colors_list,
        width = width
    )
    if title:
        plt.title(title)
    plt.tight_layout()

def plot_inertia_scores(
    inertia_vals: List[float], 
    x_label: str = "K", 
    y_label: str = "Within-Cluster Sum of Squares",
    label: Optional[str] = None,
    title: Optional[str] = None,
    path: Optional[str] = None
) -> None:
    """Plots Within-Cluster Sum of Squares (WCSS) scores for various number of clusters, K

    Args:
        inertia_vals: List of WCSS scores to plot
        x_label: Label for x-axis which is consecutive K values, denoting number of clusters. Defaults to "K"
        y_label: Label for y-axis values which is the WCSS score for different values of K. 
                    Defaults to "Within-Cluster Sum of Squares"
        label: Label to provide in the legend for the plotted WCSS line. Defaults to None
        title: Title for the plot. Defaults to None
        path: Path to the directory on the host which the .png file will be saved. If provided, the label parameter
                is also required, which will be the name of the saved png of the plot. Defaults to None
    """
    x_vals = range(2, len(inertia_vals) + 2)
    plt.plot(x_vals, inertia_vals, label = label)
    plt.xticks(x_vals)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    if label:
        plt.legend(facecolor = 'w', edgecolor = "black", shadow = True, frameon = True)
    if title:
        plt.title(title)
    if path:
        plt.tight_layout()
        plt.savefig(join(path, f"{label}.png"))
    plt.show()

def plot_clustering(
    red_data: np.ndarray, 
    cluster_id_arr: np.ndarray, 
    cluster_centers: np.ndarray, 
    x_label: str = None, 
    y_label: str = None, 
    title: str = None, 
    path: str = None, 
    cluster_category_names: Optional[Dict[int, str]] = None,
    fig_size = (8, 6)
) -> None:
    """Plots 2D resulting, color-coded clustering of the dimensionality reduced data, red_data

    Args:
        red_data: Numpy data matrix which has been reduced to 2-dimensions. Must be of shape (num_data_points by 2)
        cluster_id_arr: Cluster assignment found from applying the clustering algorithm for the data points in red_data.
                            Numpy array of intergers of length red_data.shape[0], since each data point must be assigned to a cluster
        cluster_centers: Numpy matrix of shape (num_clusters by 2) corresponding to vectors of the cluster centers found in 
            the 2D space
        x_label: X-axis label corresponding to the first feature in red_data. Default is None
        y_label: Y-axis label corresponding to the second feature in red_data. Default is None
        title: Title of the 2D clustering plot. Default is None
        path: Path to .png filename on host's system the file will be saved as. Default is None
        cluster_category_names: Dictionary mapping cluster integer id to human-annotated class string label
                                    for that cluster for providing an labeled legend. Default is None
        fig_size: Tuple indicating size of the figure as (horizontal width, vertical length) in 
                    inches. Default is (8, 6)
    """
    assert red_data.shape[1] == 2
    assert len(cluster_id_arr) == red_data.shape[0]
    num_clusters = len(np.unique(cluster_id_arr))
    plt.figure(figsize = fig_size)
    for c in np.unique(cluster_id_arr):
        ix = np.where(cluster_id_arr == c)[0]
        label = cluster_category_names[c] if cluster_category_names else 'Cluster {}'.format(c)
        plt.scatter(red_data[ix, 0], red_data[ix, 1], label = label)
    if title:
        plt.title(title)
    if x_label:
        plt.xlabel(x_label)
    if y_label:    
        plt.ylabel(y_label)
    plt.scatter(cluster_centers[:, 0], cluster_centers[:, 1], s = 40, marker = 'x', color = 'k')
    plt.legend(loc = 'upper center', bbox_to_anchor = (0.5, -0.05), fancybox = True, shadow = True, ncol = num_clusters//2)
    if path:
        plt.tight_layout(w_pad = 10)
        plt.savefig(path)
    plt.show()

def plot_nested_cv_results(
    nested_cv_results_dict: Dict[str, Tuple[float, float]], 
    title: str = "Outer Folds {OPTIMIZE_METRIC} Scores", 
    xlabel: str = "Score", 
    save_dir: str = None
) -> None:
    """Plots the results of Nested Cross Validation (Nested CV), namely the mean performance (with standard deviation error bars) of various algorithms and hyperparameter grids 
        on the test folds of the outer cross validation procedure. The algorithms are sorted in decreasing order from top to bottom by the left-cap, i.e. the difference between
        the mean score and the standard deviation in order to help identify algorithms + hyperparameter grids which had relatively high mean and low variance in their performance

    Args:
        nested_cv_results_dict: Dictionary storing the results of the outer cv of nested cv for various algorithms, of the form:
            {
                <algo-1>: (<mean-score-on-outer-folds>, <standard-deviation-on-outer-folds>),
                ...
            }
        title: Title of the plot. Default is "Outer Folds {OPTIMIZE_METRIC} Scores", which is a template/example title depending on the metric which was optimized in Nested CV
        xlabel: Label for the variable of comparison, i.e. the mean scores (with standard deviation error bars) on the outer cv test folds. Default is 'Score'
        save_dir: Path to directory on the host's filesystem where the plot of the results will be saved. Default is None. If provided, the filename is the value of the constant,
                    NESTED_CV_RESULTS_PLOT_FILENAME
    """
    alg_names = list(nested_cv_results_dict.keys())
    # Sort by the left cap i.e. mean score - std... 
    # we use this for finding an algorithm + search procedure with high mean score and low variance
    alg_names.sort(key = lambda alg_name: nested_cv_results_dict[alg_name][0] - nested_cv_results_dict[alg_name][1])
    cv_mean_scores = np.array([nested_cv_results_dict[alg_name][0] for alg_name in alg_names])
    errors = np.array([nested_cv_results_dict[alg_name][1] for alg_name in alg_names])

    plt.errorbar(
        cv_mean_scores, 
        alg_names, 
        xerr = errors, 
        linestyle='None', 
        solid_capstyle='projecting',
        color='royalblue',
        markersize=8, 
        capsize=7,
        capthick=2,
        marker='o'
    )
    
    plt.yticks(alg_names, weight = 'bold')
    plt.title(title)
    plt.xlabel(xlabel)
    if save_dir:
        save_path = join(save_dir, NESTED_CV_RESULTS_PLOT_FILENAME)
        plt.savefig(save_path, dpi = 300, bbox_inches = "tight")
    plt.show()

def plot_precision_recall_curve_for_model(
    model_name: str, 
    test_pos_probs_or_decision_func_scores: np.ndarray, 
    y_test: np.ndarray, 
    title: str = 'Precision-Recall Curve', 
    save_path: Optional[str] = None, 
    fig_size: Tuple[int, int] = (6, 5),
    legend_position: Tuple[float, float] = (0.837, -0.17),
) -> None:
    """Plots the Precision-Recall curve for a trained model on test data. Also plots typical PR No-Skill baseline

    Note:
        This implementation is only compatible with binary classification
    
    Args:
        model_name: Name of the model whose predictions are being plotted in the precision-recall curve plot
        test_pos_probs_or_decision_func_scores: The probabilities given to the positive class by the classifier
                                                or the scores given by the decision function to the test data points
        y_test: Ground-truth labels for the test data points
        title: Title of the precision-recall curve plot. Default is 'Precision-Recall Curve'
        save_path: Path (including .png filename) on host's filesystem to save the plot. Default is None
        fig_size: Tuple indicating size of the figure as (horizontal width, vertical length) in inches. Default is (6, 5)
        legend_position: Tuple which positions the legend
    """
    # plot the precision-recall curves
    model_aucpr_score = compute_aucpr(y_test, test_pos_probs_or_decision_func_scores)
    precision, recall, _ = precision_recall_curve(y_test, test_pos_probs_or_decision_func_scores)
    fig, ax = plt.subplots(figsize = fig_size)
    no_skill = sum(y_test[y_test == 1]) / len(y_test)
    plt.plot(recall, precision, label=f'{model_name} (AUCPR = {round(model_aucpr_score, 3)})', color='tab:blue')
    plt.plot([0, 1], [no_skill, no_skill], linestyle='--', label = f'No Skill (AUCPR = {round(no_skill, 3)})', color='tab:red')
    # axis labels
    plt.title(title, fontsize = 13)
    plt.xlabel('Recall', fontsize = 13)
    plt.ylabel('Precision', fontsize = 13)
    # show the legend
    plt.legend(bbox_to_anchor = legend_position, borderaxespad = 0, fontsize = 10, edgecolor = "black", shadow = True, frameon = True)
    if save_path:
        fig.savefig(save_path, bbox_inches = 'tight', dpi = 150)
    plt.show()