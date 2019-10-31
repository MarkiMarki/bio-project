from ..settings.base_settings import *
from ..settings.tidying_settings import *
import numpy as np
import pandas as pd
import re
from os import listdir
from os.path import isfile, join
import glob


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
def get_all_measurement_codes(folder="raw",mix = "merged"):
    measurement_codes = None
    if folder == "raw":
        filenames = [f for f in listdir(RAW_DATA_DIRECTORY)
                     if isfile(join(RAW_DATA_DIRECTORY, f)) and '.xls' in f]
        measurement_codes = set(get_measurement_code_from_filename(filenames))
    elif folder == "tidy":
        measurement_codes = [f.split('.')[0] for f in listdir(TIDY_DATA_DIRECTORY+mix+"\\")
                             if isfile(join(TIDY_DATA_DIRECTORY+mix+"\\", f)) and '.csv' in f]
    return measurement_codes


# Receives a measurement code and returns a tidy dataframe of the measurement
def get_tidy_data(measurement_code, mix="merged", from_raw = False):
    if not from_raw:
        measurement_data = pd.read_csv(TIDY_DATA_DIRECTORY + mix + "\\" + measurement_code + ".csv",index_col=0)
        return measurement_data

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
                          ['Section', 'Patient', 'Condition', 'NUC CG X', 'NUC CG Y']
        # Adding a measurement chronological order variable
        patient_data["CHRONO_ORDER"] = 0
        j = 0
        for (row, col) in SERPENT_ORDERED_ITERATOR:
            patient_data.loc[(patient_data["Row"] == row) & (patient_data["Col"] == col), 'CHRONO_ORDER'] = j
            j = j + 1
        patient_data = patient_data.drop(axis=1, labels=columns_to_drop)
        # If we need a specific mix - return it
        if not mix == "merged":
            variable_list = list(patient_data)
            if (mix == "mito_tmre" and [s for s in variable_list if "MITO" in s]) or \
                    (mix == "er_lyso" and [s for s in variable_list if "LYSO" in s]):
                return patient_data
        patient_df_list.append(patient_data)

    if mix == "merged":
        # Merging the data collected from all files
        all_data = pd.concat(patient_df_list, sort=False)
        return all_data

    return None

