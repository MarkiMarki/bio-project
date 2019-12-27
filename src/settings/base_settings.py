import os
import re
from abspath_routing import PROJECT_ROOT_PATH

# Paths to data directories
BASE_DATA_DIRECTORY = os.path.join(PROJECT_ROOT_PATH, "data")
TIDY_DATA_DIRECTORY = os.path.join(BASE_DATA_DIRECTORY, 'tidy_data')
RAW_DATA_DIRECTORY = os.path.join(BASE_DATA_DIRECTORY, 'raw_data')
STRATIFIED_DATA_DIRECTORY = os.path.join(BASE_DATA_DIRECTORY, 'stratified_data')

# namaes of plot directories
PAIR_PLOT_DIRNAME = "all_var_pair_plots"
BOXPLOT_CHRONO_ORDER_DIRNAME = "boxplot_by_measurement_order"
MEAN_MEDIAN_DIRNAME = "mean_median_by_measurement_order"
SD_MEDIAN_DIRNAME = "sd_median_by_measurement_order"
MERGED_SPEARMAN_CORR_DIRNAME = "merged_spearman_corr"
FEATURE_MEDIAN_BY_PLATE_DIRNAME = "feature_median_by_plate"

# Regex matchers
PLATE_REGEX = re.compile("S\dP\d")
MEASUREMENT_REGEX_STR = "_{mix}_S\dP\d"
