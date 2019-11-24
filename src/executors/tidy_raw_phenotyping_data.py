from src.resources.tidying_microscopy import *
from src.settings.base_settings import *

# Execute this file to transform all raw phenotyping data to tidy data

if __name__ == "__main__":
    measurement_codes = get_all_patient_codes()
    measurement_count = len(measurement_codes)
    i = 0
    for measurement_code in measurement_codes:
        i += 1
        print("Processing " + measurement_code + ": {index} / {length}".format(index = i, length = measurement_count))
        for mix in ["er_lyso", "mito_tmre","merged"]:
            measurement_data = get_tidy_data(
                measurement_code=measurement_code,
                mix=mix,
                from_raw=True
            )
            if measurement_data is not None:
                dirname = TIDY_DATA_DIRECTORY + mix + "\\"
                mkdir_p(dirname)
                measurement_data.to_csv(dirname + str(measurement_code) + ".csv")
