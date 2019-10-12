from ..settings.base_settings import *
from ..settings.tidying_settings import *
import numpy as np
import pandas as pd
import re
from os import listdir
from os.path import isfile, join
import glob


# Returning the indexed number from a string
@np.vectorize
def get_ith_number(input_string, i):
    try:
        return str(re.findall(r'\d+', input_string)[i])
    except TypeError:
        print("Field was not a string")

# Returning measurement code - <CONIDITION><PATIENT>_<SET> from a given filename
@np.vectorize
def get_measurement_code_from_filename(input_string):
    try:
        return input_string.split('_S')[0]
    except TypeError:
        print("Field was not a string")


# Getting all measurement codes from the raw / tidy data directory
def get_all_measurement_codes(folder="raw"):
    measurement_codes = None
    if folder == "raw":
        filenames = [f for f in listdir(RAW_DATA_DIRECTORY)
                    if isfile(join(RAW_DATA_DIRECTORY, f)) and '.xls' in f]
        measurement_codes = set(get_measurement_code_from_filename(filenames))
    elif folder == "tidy":
        measurement_codes = [f.split('.')[0] for f in listdir(TIDY_DATA_DIRECTORY)
                             if isfile(join(TIDY_DATA_DIRECTORY, f)) and '.csv' in f]
    return measurement_codes


# Receives a measurement code and returns a tidy dataframe of the measurement
def get_tidy_data(measurement_code):
    # Looping over all file paths that exist for the measurement
    filename_list = glob.glob(RAW_DATA_DIRECTORY + measurement_code + '*.xls')
    patient_df_list = []

    for filename in filename_list:
        # Reading the file to a dataframe with fixed column names
        patient_data = pd.read_excel(filename, header=1).rename(mapper=COLUMN_RENAME_MAPPER, axis=1)
        # Extracting the field from the Section variable
        patient_data['Field'] = patient_data['Section'].apply(get_ith_number, i=1)
        # Getting rid of unwanted variables
        columns_to_drop = [s for s in list(patient_data) if " POS " in s] + \
                          ['Section', 'Patient', 'Condition','NUC CG X','NUC CG Y']
        patient_data = patient_data.drop(axis=1, labels=columns_to_drop)
        patient_df_list.append(patient_data)

    # Merging the data collected from all files
    all_data = pd.concat(patient_df_list, sort=False)

    # Adding a measurement chronological order variable
    all_data["CHRONO_ORDER"] = 0
    j = 0
    for (row, col) in SERPENT_ORDERED_ITERATOR:
        all_data.loc[(all_data["Row"] == row) & (all_data["Col"] == col), 'CHRONO_ORDER'] = j
        j = j + 1

    return all_data


