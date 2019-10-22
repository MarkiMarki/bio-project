from src.resources.plot_helper import *
from src.resources.tidying_microscopy import *

if __name__ == "__main__":
    measurement_codes = get_all_measurement_codes("tidy")
    measurement_count = len(measurement_codes)
    i = 0
    for measurement_code in measurement_codes:
        i += 1
        print("Processing " + measurement_code + ": {index} / {length}".format(index=i, length=measurement_count))
        measurement_path = os.path.join(TIDY_DATA_DIRECTORY, measurement_code + ".csv")
        measurement_data = pd.read_csv(measurement_path, index_col=0)
        measurement_data = measurement_data.drop(columns=HEATMAP_IRRELEVANT_VARIABLES)
        plot_mean_And_median_against_chrono_order(
            data=measurement_data,
            code=measurement_code
        )
