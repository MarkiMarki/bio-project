from src.resources.plot_helper import *
from src.resources.tidying_microscopy import *
import seaborn as sns
import pandas as pd

from src.settings.plot_settings import *


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


def plot_mito_tmre(data, code, save=True, show=False):
    variables = set(data)
    if TMRE_UNIQUE_VARIABLES.issubset(variables):
        mito_tmre_measurement = data
        if ER_LYSO_UNIQUE_VARIABLES.issubset(variables):
            mito_tmre_measurement = data.drop(columns=TMRE_UNIQUE_VARIABLES)
        plot_measurement_corr_heatmap(
            measurement_data=mito_tmre_measurement,
            measurement_code=code,
            type="mito_tmre",
            save=save,
            show=show
        )


def drop_irrelevant_variables(data):
    return data.drop(columns=HEATMAP_IRRELEVANT_VARIABLES)


if __name__ == "__main__":
    measurement_codes = get_all_measurement_codes("tidy")
    measurement_count = len(measurement_codes)
    i = 0
    for measurement_code in measurement_codes:
        i += 1
        print("Processing " + measurement_code + ": {index} / {length}".format(index=i, length=measurement_count))
        measurement_path = os.path.join(TIDY_DATA_DIRECTORY, measurement_code + ".csv")
        measurement_data = pd.read_csv(measurement_path, index_col=0)
        measurement_data = drop_irrelevant_variables(measurement_data)
        plot_er_lyso(data=measurement_data, code=measurement_code)
        plot_mito_tmre(data=measurement_data, code=measurement_code)
