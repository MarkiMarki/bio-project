from src.resources.plot_helper import *
from src.resources.tidying_microscopy import *
import seaborn as sns
import pandas as pd

from src.settings.plot_settings import *

# Plot heatmaps for er_lyso mix
def plot_er_lyso(data, code, save=True, show=False):
    variables = set(data)
    if ER_LYSO_UNIQUE_VARIABLES.issubset(variables):
        er_lyso_measurement = data
        if TMRE_UNIQUE_VARIABLES.issubset(variables):
            er_lyso_measurement = data.drop(columns=TMRE_UNIQUE_VARIABLES)
        plot_measurement_corr_heatmap(
            measurement_data=er_lyso_measurement,
            measurement_code=code,
            type="er_lyso",
            save=save,
            show=show
        )

# Plot heatmaps for mito_tmre mix
def plot_mito_tmre(data, code, save=True, show=False):
    variables = set(data)
    if TMRE_UNIQUE_VARIABLES.issubset(variables):
        mito_tmre_measurement = data
        if ER_LYSO_UNIQUE_VARIABLES.issubset(variables):
            mito_tmre_measurement = data.drop(columns=ER_LYSO_UNIQUE_VARIABLES)
        plot_measurement_corr_heatmap(
            measurement_data=mito_tmre_measurement,
            measurement_code=code,
            type="mito_tmre",
            save=save,
            show=show
        )

# Lose irrelevant variables from  the tidy data
def drop_irrelevant_variables(data):
    return data.drop(columns=IRRELEVANT_VARIABLES)

# Plot heatmap by desired mix
def plot_heatmaps_by_mix(data, code, mix, save=True, show=False):
    if mix == "er_lyso":
        plot_er_lyso(data=data,code=code,save=save,show=show)
    elif mix == "mito_tmre":
        plot_mito_tmre(data=data, code=code, save=save, show=show)



# Plots correlarion heatmap for all variables / sorted R squared against chronological order (decided in plot_settings)
if __name__ == "__main__":
    for mix in ["er_lyso", "mito_tmre"]:
        print(mix + "\n ======================================")
        i = 0
        measurement_codes = get_all_patient_codes(
            folder="tidy",
            mix=mix
        )
        measurement_count = len(measurement_codes)
        for measurement_code in measurement_codes:
            i += 1
            print("Processing " + measurement_code + ": {index} / {length}".format(index=i, length=measurement_count))
            measurement_data = get_tidy_data(
                measurement_code=measurement_code,
                mix=mix
            )
            if measurement_data is not None:
                measurement_data = measurement_data.drop(columns=IRRELEVANT_VARIABLES)
                plot_heatmaps_by_mix(data=measurement_data, code= measurement_code, mix=mix)







