import pandas as pd

from src.resources.utils.data_utils import mkdir_p
from .plate import Plate
import seaborn as sns
import matplotlib.pyplot as plt
from src.settings.base_settings import *


class AllPlates:
    def __init__(self, plot_from="tidy", raw_data_dir=None, tidy_data_dir=None, stratified_data_dir=None):

        # Determine if plots will be generated to stratified or tidy data
        self.plot_from = plot_from

        # Directories for data and plotting
        self.raw_data_dir = self.get_raw_data_dir(raw_data_dir)
        self.tidy_data_dir = self.get_tidy_data_dir(tidy_data_dir)
        self.stratified_data_dir = self.get_stratified_data_dir(stratified_data_dir)
        self.temp_plot_dir = self.get_plot_dest()

        # List of Plate objects per mix & merged
        self.el_plates = self.get_plates_for_mix("EL")
        self.mt_plates = self.get_plates_for_mix("MT")
        self.plates = self.el_plates + self.mt_plates

    '''
    FILESYSTEM METHODS
    '''

    # Get the directory in which to plot
    def get_plot_dest(self):
        if "tidy" in self.plot_from:
            return os.path.join(self.tidy_data_dir, "figs")
        elif "strat" in self.plot_from:
            return os.path.join(self.stratified_data_dir, "figs")

    # Get the raw data directory. If not modified - return default
    def get_raw_data_dir(self, dirname):
        if dirname is None:
            return RAW_DATA_DIRECTORY
        else:
            return os.path.join(BASE_DATA_DIRECTORY, dirname)

    # Get the tidy data directory. If not modified - return default
    def get_tidy_data_dir(self, dirname):
        if dirname is None:
            return TIDY_DATA_DIRECTORY
        else:
            return os.path.join(BASE_DATA_DIRECTORY, dirname)

    # Get the stratified data directory. If not modified - return default
    def get_stratified_data_dir(self, dirname):
        if dirname is None:
            return STRATIFIED_DATA_DIRECTORY
        else:
            return os.path.join(BASE_DATA_DIRECTORY, dirname)

    # Get a set of filepaths in raw data directory for a desired mix
    def get_raw_data_paths_for_mix(self, mix):
        paths = []
        for dirpath, dirnames, filenames in os.walk(self.raw_data_dir):
            paths = paths + [os.path.join(self.raw_data_dir, filename)
                             for filename in filenames
                             if "_" + mix + "_S" in filename and ".xls" in filename]
        return set(paths)

    '''
    SUMMARY METHODS 
    '''

    # Returns a set of all plate codes for a desired mix
    def get_plate_codes_for_mix(self, mix):
        paths = self.get_raw_data_paths_for_mix(mix)
        names = [str(path).split('_')[-1].split('.')[0] for path in paths]
        return set(names)

    # Returns a set of all patients that were placed on a desired plate
    def get_patients_for_plate_code(self, plate_code):
        patients = []
        for dirpath, dirnames, filenames in os.walk(self.raw_data_dir):
            patients = patients + [filename.split('_')[0]
                                   for filename in filenames
                                   if plate_code in filename and ".xls" in filename]
        return set(patients)

    # Returns a list of Plate objects for desired mix
    def get_plates_for_mix(self, mix):
        plate_codes = self.get_plate_codes_for_mix(mix)
        plate_paths = self.get_raw_data_paths_for_mix(mix)
        plates = []
        for plate_code in plate_codes:
            patients = self.get_patients_for_plate_code(plate_code)
            paths = [plate_path for plate_path in plate_paths if plate_code in str(plate_path)]
            plates.append(Plate(
                code=plate_code,
                mix=mix,
                patients=set(patients),
                plot_from=self.plot_from,
                raw_data_paths=paths,
                tidy_data_dir=self.tidy_data_dir,
                stratified_data_dir=self.stratified_data_dir
            ))

        return plates

    '''
    DATA HANDLING METHODS
    '''

    # Loops through plates and invokes "save_tidy_data"
    def save_tidy_data(self, mix={"EL", "MT"}):
        if "EL" in mix:
            for plate in self.el_plates:
                plate.save_tidy_data()
        if "MT" in mix:
            for plate in self.mt_plates:
                plate.save_tidy_data()

    # Loops through plates and invokes "save_stratified_data"
    def save_stratified_data(self, mix={"EL", "MT"}):
        if "EL" in mix:
            for plate in self.el_plates:
                plate.save_stratified_data()
        if "MT" in mix:
            for plate in self.mt_plates:
                plate.save_stratified_data()

    '''
    PLOT METHODS
    '''

    # Plot boxplot for each feature across all plates
    def plot_merged_spearman_corr_for_mix(self, mix, show=False, save=True):
        plate_list = None
        if mix == "EL":
            plate_list = self.el_plates
        if mix == "MT":
            plate_list = self.mt_plates

        corr_lst = []
        for plate in plate_list:
            print("Getting corr from " + plate.code)
            corr_lst.append(plate.get_corr_vs_order())
        corr_df = pd.concat(corr_lst, sort=False)

        variable_list = list(corr_df)
        channel_range = range(1, 5)

        for i in channel_range:
            df = None
            if i == 1:
                df = corr_df[[var for var in variable_list if "NUC" in var]]
            elif i == 2:
                df = corr_df[[var for var in variable_list if "CELL" in var]]
            elif i == 3:
                df = corr_df[[var for var in variable_list if "LYSO" in var or "MITO" in var]]
            elif i == 4:
                df = corr_df[[var for var in variable_list if
                              ("TMRE" in var or "ER " in var) and not ("CELL" in var or "LYSO" in var)]]
            sns.set(style="whitegrid")
            ax = sns.boxplot(data=df, color="seagreen")
            ax.set_title('Spearman Correlation to Chronological Order')
            ax.set_xticklabels(ax.get_xticklabels(), rotation=20)
            fig = plt.gcf()
            fig.set_size_inches(10, 10)
            if show:
                plt.show()
            if save:
                dir_name = os.path.join(self.temp_plot_dir, MERGED_SPEARMAN_CORR_DIRNAME, mix)
                mkdir_p(dir_name)
                filename = "CH" + str(i) + ".png"
                ax.figure.savefig(os.path.join(dir_name, filename))
            plt.close('all')
