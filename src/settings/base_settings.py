import os
from abspath_routing import PROJECT_ROOT_PATH

BASE_DATA_DIRECTORY = os.path.join(PROJECT_ROOT_PATH, "patient_microscopy_data\\")
TIDY_DATA_DIRECTORY = os.path.join(BASE_DATA_DIRECTORY, 'tidy_data\\')
RAW_DATA_DIRECTORY = os.path.join(BASE_DATA_DIRECTORY,'raw_data\\')

BASE_PLOT_DIRECTORY= os.path.join(PROJECT_ROOT_PATH, "plots\\")
PAIR_PLOT_DIRECTORY= os.path.join(BASE_PLOT_DIRECTORY, "pair_plots\\")


FILE_NAME_FORMAT = "{condition}{patient}_{passage}_S{s}P{p}.xls"