import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline, BSpline
from src.settings.base_settings import *
from src.settings.plot_settings import *

# Transforms pearson correlation values to colors (for heatmap)
def value_to_color(val):
    n_colors = 256  # Use 256 colors for the diverging color palette
    palette = sns.diverging_palette(20, 220, n=n_colors)  # Create the palette
    color_min, color_max = [-1,
                            1]  # Range of values that will be mapped to the palette, i.e. min and max possible correlation
    val_position = float((val - color_min)) / (
            color_max - color_min)  # position of value in the input range, relative to the length of the input range
    ind = int(val_position * (n_colors - 1))  # target index in the color palette
    return palette[ind]

# Self implementation of heatmap from scatter plot (in order to adjust square size to magnitude)
def heatmap(x, y, size, values):
    fig, ax = plt.subplots()

    # Mapping from column names to integer coordinates
    x_labels = [v for v in sorted(x.unique())]
    y_labels = [v for v in sorted(y.unique())]
    x_to_num = {p[1]: p[0] for p in enumerate(x_labels)}
    y_to_num = {p[1]: p[0] for p in enumerate(y_labels)}

    size_scale = 500
    ax.scatter(
        x=x.map(x_to_num),  # Use mapping for x
        y=y.map(y_to_num),  # Use mapping for y
        s=size * size_scale,  # Vector of square sizes, proportional to size parameter
        c=values.apply(value_to_color),
        marker='s'  # Use square as scatterplot marker
    )

    # Show column labels on the axes
    ax.set_xticks([x_to_num[v] for v in x_labels])
    ax.set_xticklabels(x_labels, rotation=45, horizontalalignment='right')
    ax.set_yticks([y_to_num[v] for v in y_labels])
    ax.set_yticklabels(y_labels)

    ax.grid(False, 'major')
    ax.grid(True, 'minor')
    ax.set_xticks([t + 0.5 for t in ax.get_xticks()], minor=True)
    ax.set_yticks([t + 0.5 for t in ax.get_yticks()], minor=True)

    ax.set_xlim([-0.5, max([v for v in x_to_num.values()]) + 0.5])
    ax.set_ylim([-0.5, max([v for v in y_to_num.values()]) + 0.5])

# Gets measurement code and data, plots a correlation heatmap.
# Receives the RESTRICT_HEATMAP_VARIABLES parameter from plot_settings
# and plots a full corr heatmap or top correlations to a single variable accordingly
def plot_measurement_corr_heatmap(measurement_code, measurement_data, type, show=False, save=True):
    if RESTRICT_HEATMAP_VARIABLES:
        fig, ax = plt.subplots(figsize=(12, 12))
        corr = measurement_data.corr()[[HEATMAP_TARGET_VARIABLE]].pow(2)
        sns.heatmap(corr.sort_values(HEATMAP_TARGET_VARIABLE).tail(10),
                    vmax=1, vmin=0, cmap="YlGnBu", annot=True, ax=ax)
        plt.yticks(rotation=0)
        ax.invert_yaxis()
        fig = plt.gcf()
        fig.set_size_inches(20, 12)
    else:
        columns = list(measurement_data)
        corr = measurement_data[columns].corr()
        corr = pd.melt(corr.reset_index(),
                       id_vars='index')  # Unpivot the dataframe, so we can get pair of arrays for x and y
        corr.columns = ['x', 'y', 'value']
        heatmap(
            x=corr['x'],
            y=corr['y'],
            size=corr['value'].abs(),
            values=corr['value']
        )
        fig = plt.gcf()
        fig.set_size_inches(20, 20)
    if show:
        plt.show()
    if save:
        filename = measurement_code + "_" + type + ".png"
        if RESTRICT_HEATMAP_VARIABLES:
            directory_name = PAIR_PLOT_DIRECTORY + "\\" + HEATMAP_TARGET_VARIABLE
        else:
            directory_name = PAIR_PLOT_DIRECTORY + "\\ALL_VARIABLES"
        mkdir_p(directory_name)
        plt.savefig(directory_name + "\\" + filename, dpi=100)
    plt.close('all')

# Plots every variable against chronological order, grouped with boxplots
def plot_all_variables_against_chrono_order(data, code, show=False, save=True):
    variables = set(data)
    variables.remove("CHRONO_ORDER")
    for var in variables:
        sns.set(style="whitegrid")
        box_plot = sns.boxplot(x="CHRONO_ORDER", y=var, data=data, color="seagreen")
        fig = plt.gcf()
        fig.set_size_inches(20, 20)
        if show:
            sns.boxplot(x="CHRONO_ORDER", y=var, data=data, color="seagreen")
        if save:
            dir_name = BOXPLOT_CHRONO_ORDER_DIRECTORY + code + "\\"
            mkdir_p(dir_name)
            filename = var + ".png"
            box_plot.figure.savefig(dir_name + "\\" + filename)
        plt.close('all')

# Plots an interpolated line for the mean and median of every variable grouped by chronological order
def plot_mean_And_median_against_chrono_order(data, code, show=False, save=True):
    median_data = data.groupby(['CHRONO_ORDER']).median()
    mean_data = data.groupby(['CHRONO_ORDER']).mean()
    variables = set(data)
    variables.remove("CHRONO_ORDER")
    for var in variables:
        mean_y = mean_data[[var]].dropna()
        median_y = median_data[[var]].dropna()
        x = mean_y.index.values
        fig = plt.figure()
        ax = plt.subplot(111)
        ax.plot(x, mean_y, label='Mean')
        ax.plot(x, median_y, label='Median')
        plt.title(var)
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), shadow = True, ncol = 2)
        if show:
            plt.show()
        if save:
            dir_name = MEAN_MEDIAN_DIRECTORY + code + "\\"
            mkdir_p(dir_name)
            filename = var + ".png"
            plt.savefig(dir_name + "\\" + filename)
        plt.close('all')
        # y = median_data[[var]].dropna()
        # x = y.index.values
        # xnew = np.linspace(x.min(), x.max(), 300)
        # spl = make_interp_spline(x, y, k=3)  # BSpline object
        # smooth = spl(xnew)
        # plt.plot(xnew, smooth)
        #
        # y = mean_data[[var]].dropna()
        # x = y.index.values
        # xnew = np.linspace(x.min(), x.max(), 300)
        # spl = make_interp_spline(x, y, k=3)  # BSpline object
        # smooth = spl(xnew)
        # plt.plot(xnew, smooth)
        # plt.show()




# Create a new directory in a given path
def mkdir_p(mypath):
    '''Creates a directory. equivalent to using mkdir -p on the command line'''

    from errno import EEXIST
    from os import makedirs, path

    try:
        makedirs(mypath)
    except OSError as exc:  # Python >2.5
        if exc.errno == EEXIST and path.isdir(mypath):
            pass
        else:
            raise
