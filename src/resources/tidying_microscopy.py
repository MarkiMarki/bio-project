from ..settings.base_settings import *
import numpy as np
import pandas as pd
import re
from os import listdir
from os.path import isfile, join

@np.vectorize
def get_ith_number(input_string,i):
    try:
        return str(re.findall(r'\d+', input_string)[i])
    except TypeError:
        print("Field was not a string")


def get_tidy_data(patient_code):
    route_1 = BASE_DATA_DIRECTORY + FILE_NAME_FORMAT.format(pat=patient_code, p=1)
    route_2 = BASE_DATA_DIRECTORY + FILE_NAME_FORMAT.format(pat=patient_code, p=2)

    column_rename_mapper = {
        'Unnamed: 0': 'Condition',
        'Unnamed: 1': 'Patient',
        ' ': 'Row',
        ' .1': 'Col'
    }
    p1 = (
        pd.read_excel(route_1.format(p=1), header=1)
        .rename(mapper=column_rename_mapper, axis=1)
    )
    p2 = (
        pd.read_excel(route_2.format(p=2), header=1)
        .rename(mapper=column_rename_mapper, axis=1)
    )
    p1['Section'] = p1['Section'].apply(get_ith_number, i=1)
    p2['Section'] = p2['Section'].apply(get_ith_number, i=1)
    columns_to_drop = [s for s in list(p1)
                       if " POS " in s]
    p1.drop(axis=1, labels=columns_to_drop)
    p2.drop(axis=1, labels=columns_to_drop)
    all_data = pd.concat([p1,p2])
    return all_data


def get_all_patient_codes():
    filenames = [f for f in listdir(BASE_DATA_DIRECTORY)
                     if isfile(join(BASE_DATA_DIRECTORY, f)) and '.xls' in f]
    patient_codes = list(get_ith_number(filenames,0))
    return patient_codes

