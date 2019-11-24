import os
from abspath_routing import PROJECT_ROOT_PATH

# Paths to data directories
BASE_DATA_DIRECTORY = os.path.join(PROJECT_ROOT_PATH, "patient_microscopy_data\\")
TIDY_DATA_DIRECTORY = os.path.join(BASE_DATA_DIRECTORY, 'tidy_data\\')
RAW_DATA_DIRECTORY = os.path.join(BASE_DATA_DIRECTORY, 'raw_data\\')
PATIENT_BY_PLATE_FILE_PATH = os.path.join(BASE_DATA_DIRECTORY, "patient_by_plate.json")

# Paths to plot directories
BASE_PLOT_DIRECTORY = os.path.join(PROJECT_ROOT_PATH, "plots\\")
PAIR_PLOT_DIRECTORY = os.path.join(BASE_PLOT_DIRECTORY, "corr_heatmaps\\")
BOXPLOT_CHRONO_ORDER_DIRECTORY = os.path.join(BASE_PLOT_DIRECTORY, "boxplot_chrono_order\\")
MEAN_MEDIAN_DIRECTORY = os.path.join(BASE_PLOT_DIRECTORY, "mean_median_by_chrono_order\\")
SD_MEDIAN_DIRECTORY = os.path.join(BASE_PLOT_DIRECTORY, "sd_median_by_chrono_order\\")
MERGED_SPEARMAN_CORR_DIRECTORY = os.path.join(BASE_PLOT_DIRECTORY, "merged_spearman_corr\\")
FEATURE_MEDIAN_BY_PLATE_DIRECTORY = os.path.join(BASE_PLOT_DIRECTORY, "feature_median_by_plate\\")

FILE_NAME_FORMAT = "{condition}{patient}_{passage}_{plate}.xls"
