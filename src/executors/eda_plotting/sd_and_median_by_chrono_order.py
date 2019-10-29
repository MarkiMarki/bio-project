from src.resources.plot_helper import *
from src.resources.tidying_microscopy import *

if __name__ == "__main__":
    measurement_codes = get_all_measurement_codes("raw")
    measurement_count = len(measurement_codes)
    i = 0
    for measurement_code in measurement_codes:
        i += 1
        print("Processing " + measurement_code + ": {index} / {length}".format(index=i, length=measurement_count))
        for mix in ["er_lyso", "mito_tmre"]:
            measurement_data = get_tidy_data(
                measurement_code=measurement_code,
                mix=mix
            )
            if measurement_data is not None:
                measurement_data = measurement_data.drop(columns=HEATMAP_IRRELEVANT_VARIABLES)
                plot_sd_and_median_against_chrono_order(
                    data=measurement_data,
                    code=measurement_code,
                    mix=mix
                )
