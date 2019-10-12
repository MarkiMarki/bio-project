import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

from src.settings.base_settings import *


def value_to_color(val):
    n_colors = 256  # Use 256 colors for the diverging color palette
    palette = sns.diverging_palette(20, 220, n=n_colors)  # Create the palette
    color_min, color_max = [-1,
                            1]  # Range of values that will be mapped to the palette, i.e. min and max possible correlation
    val_position = float((val - color_min)) / (
            color_max - color_min)  # position of value in the input range, relative to the length of the input range
    ind = int(val_position * (n_colors - 1))  # target index in the color palette
    return palette[ind]


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


def plot_measurement_corr_heatmap(measurement_code, measurement_data, type, show=False, save=True):
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
    if show:
        plt.show()
    if save:
        fig = plt.gcf()
        fig.set_size_inches(20, 20)
        filename = measurement_code + "_" + type + ".png"
        plt.savefig(PAIR_PLOT_DIRECTORY + filename, dpi=100)
    pass
