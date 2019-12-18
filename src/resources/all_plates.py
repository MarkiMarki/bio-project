import os
import pandas as pd

from src.resources.tidying_microscopy import mkdir_p
from src.settings.plot_settings import IRRELEVANT_VARIABLES
from .plate import Plate
import seaborn as sns
import matplotlib.pyplot as plt
from src.settings.base_settings import *


class AllPlates:
    def __init__(self, data_type):
        self.data_type = data_type
        self.er_plates = self.get_plates_for_mix("ER")
        self.tmre_plates = self.get_plates_for_mix("TMRE")
        self.plates = self.er_plates + self.tmre_plates

    def get_plate_names_for_mix(self, mix):
        root_dir = None
        if mix == "TMRE":
            root_dir = RAW_TMRE_DIRECTORY
        elif mix == "ER":
            root_dir = RAW_ER_DIRECTORY
        names = []
        for dirpath, dirnames, filenames in os.walk(root_dir):
            names = names + [dirname for dirname in dirnames if PLATE_REGEX.match(dirname)]
        return names

    def get_plates_for_mix(self, mix):
        root_dir = None
        if mix == "TMRE":
            root_dir = RAW_TMRE_DIRECTORY
        elif mix == "ER":
            root_dir = RAW_ER_DIRECTORY

        plates = []
        plate_names = self.get_plate_names_for_mix(mix)
        for plate_name in plate_names:
            mix = mix
            path_to_raw_dir = os.path.join(root_dir, plate_name)
            patients = []
            for dirpath, dirnames, filenames in os.walk(path_to_raw_dir):
                patients = patients + [filename.split('_')[0] for filename in filenames]
            plates.append(Plate(
                code=plate_name,
                mix=mix,
                path_to_raw_dir=path_to_raw_dir,
                patients=set(patients),
                data_type=self.data_type
            ))

        return plates

    def plot_merged_spearman_corr_for_mix(self, mix, show = False, save = True):
        plate_list = None
        if mix == "ER":
            plate_list = self.er_plates
        if mix == "TMRE":
            plate_list = self.tmre_plates

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
                df = corr_df[[var for var in variable_list if ("TMRE" in var or "ER " in var) and not ("CELL" in var or "LYSO" in var)]]
            sns.set(style="whitegrid")
            ax = sns.boxplot(data=df, color="seagreen")
            ax.set_title('Spearman Correlation to Chronological Order')
            ax.set_xticklabels(ax.get_xticklabels(), rotation=20)
            fig = plt.gcf()
            fig.set_size_inches(10, 10)
            if show:
                plt.show()
            if save:
                dir_name = os.path.join(MERGED_SPEARMAN_CORR_DIRECTORY,mix)
                mkdir_p(dir_name)
                filename = "CH" + str(i) + ".png"
                ax.figure.savefig(os.path.join(dir_name,filename))
            plt.close('all')

    def save_tidy_data(self, mix={"ER", "TMRE"}):
        if "ER" in mix:
            for plate in self.er_plates:
                plate.save_tidy_data()
        if "TMRE" in mix:
            for plate in self.tmre_plates:
                plate.save_tidy_data()

