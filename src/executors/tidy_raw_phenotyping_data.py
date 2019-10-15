from src.resources.tidying_microscopy import *
from src.settings.base_settings import *

# Execute this file to transform all raw phenotyping data to tidy data

if __name__ == "__main__":
    measurement_codes = get_all_measurement_codes()
    measurement_count = len(measurement_codes)
    i = 0
    for measurement in measurement_codes:
        i += 1
        print("Processing " + measurement + ": {index} / {length}".format(index = i, length = measurement_count))
        all_data = get_tidy_data(measurement)
        all_data.to_csv(TIDY_DATA_DIRECTORY + str(measurement)+".csv")