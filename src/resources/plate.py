import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from src.resources.plot_helper import heatmap
from src.resources.tidying_microscopy import get_ith_number, mkdir_p
from src.settings.base_settings import FEATURE_MEDIAN_BY_PLATE_DIRECTORY, \
    STRATIFIED_DATA_DIRECTORY, SD_MEDIAN_DIRECTORY, PAIR_PLOT_DIRECTORY, BOXPLOT_CHRONO_ORDER_DIRECTORY
from src.settings.plot_settings import IRRELEVANT_VARIABLES
from src.settings.tidying_settings import COLUMN_RENAME_MAPPER, SERPENT_ORDERED_ITERATOR


class Plate:
    def __init__(self, code, mix, raw_data_paths, tidy_data_dir, patients, data_type="tidy"):
        self.tidy_data_dir = tidy_data_dir
        self.code = code
        self.mix = mix
        self.raw_data_paths = raw_data_paths
        self.patients = patients
        self.data_type = data_type
        self.path_to_tidy_data = self.get_tidy_data_path()

        if not self.does_file_exist(self.path_to_tidy_data):
            self.save_tidy_data()

        self.temp_data = None

    '''
    FILESYSTEM METHODS
    '''

    def does_file_exist(self, path):
        try:
            f = open(path)
            return True
        except IOError:
            return False

    def get_tidy_data_path(self):
        return os.path.join(os.path.join(self.tidy_data_dir, self.mix), self.code + ".csv")

    # get data
    def get_data(self):
        if "tidy" in self.data_type:
            return self.get_tidy_data()
        elif "strat" in self.data_type:
            return self.get_stratified_data()

    def get_tidy_data(self):
        return pd.read_csv(self.path_to_tidy_data, index_col=0)

    def get_stratified_data(self):
        paths = []
        paths = [os.path.join(os.path.join(STRATIFIED_DATA_DIRECTORY, patient), patient + "_" + self.code + ".csv")
                 for patient in self.patients]
        for path in paths:
            if not self.does_file_exist(path):
                self.save_mean_median_stratified_data()

        return pd.concat([pd.read_csv(path, index_col=0) for path in paths])

    # save data
    def save_tidy_data(self):
        print("Saving plate " + self.code)
        df_list = []
        for filepath in self.raw_data_paths:
            # Reading the file to a dataframe with fixed column names
            patient_data = pd.read_excel(filepath, header=1)
            patient_data.rename(columns={
                patient_data.columns[0]: "Condition",
                patient_data.columns[1]: "Patient",
                patient_data.columns[2]: "Row",
                patient_data.columns[3]: "Col"
            }, inplace=True)
            # Renaming LYSOTRACKER / LYSOTRECKER to LYSO
            variables = set(patient_data)
            patient_data.rename(columns={
                variable: variable.replace('TRACKER', '').replace('TRECKER', '')
                for variable in variables
            }, inplace=True)
            # Extracting the field from the Section variable
            patient_data['Field'] = patient_data['Section'].apply(get_ith_number, i=1)
            # Splitting Patient and Passage
            new = []
            if '/' in patient_data["Patient"][0]:
                new = patient_data["Patient"].str.split("/", n=1, expand=True)
            if '\\' in patient_data["Patient"][0]:
                new = patient_data["Patient"].str.split("\\", n=1, expand=True)
            if len(list(new)) == 2:
                patient_data["Passage"] = new[1]
                patient_data["Patient"] = new[0]
            # Getting rid of unwanted variables
            columns_to_drop = [s for s in list(patient_data) if " POS " in s] + \
                              ['Section', 'NUC CG X', 'NUC CG Y']
            # Adding a measurement chronological order variable
            patient_data["Order"] = 0
            j = 0
            for (row, col) in SERPENT_ORDERED_ITERATOR:
                patient_data.loc[(patient_data["Row"] == row) & (patient_data["Col"] == col), 'Order'] = j
                j = j + 1
            patient_data = patient_data.drop(axis=1, labels=columns_to_drop)

            df_list.append(patient_data)
        all_data = pd.concat(df_list, sort=False)

        mkdir_p(os.path.dirname(self.path_to_tidy_data))
        print("Saving " + self.code + " " + self.path_to_tidy_data)
        all_data.to_csv(self.path_to_tidy_data)

    def save_mean_median_stratified_data(self):
        data = self.get_tidy_data()
        for patient in self.patients:
            print("Handling " + patient)
            patient_data = data.loc[data.Patient == patient].drop(columns=['Col', 'Target', 'Field', 'Row'])

            variables = set(patient_data)
            for var in IRRELEVANT_VARIABLES:
                variables.discard(var)
            ###########################################################################
            ############# Subtract the reference (0) from each feature ################
            ###########################################################################

            patient_data[list(variables)] = patient_data[list(variables)].replace(0, 0.000001).apply(np.log)

            log_median_data = patient_data[variables].groupby("Order").median()
            log_medians_mean = log_median_data.mean()
            for index, log_median_row in log_median_data.iterrows():
                for var in log_medians_mean.index:
                    patient_data.loc[patient_data.Order == index, var] += log_medians_mean[var] - log_median_row[var]

            patient_data[list(variables)] = patient_data[list(variables)].apply(np.exp)

            ###########################################################################
            ############# Add the reference (0) from each feature #####################
            ###########################################################################

            print("Saving " + patient)
            dirname = os.path.join(STRATIFIED_DATA_DIRECTORY, patient)
            mkdir_p(dirname)
            filename = patient + "_" + self.code + ".csv"
            filepath = os.path.join(dirname, filename)
            patient_data.to_csv(filepath)

    '''
    SUMMARY METHODS
    '''

    def get_corr_vs_order(self):
        df_list = []
        if self.temp_data is None:
            self.temp_data = self.get_data()
        for patient in self.patients:
            patient_data = self.temp_data.loc[self.temp_data.Patient == patient].drop(columns=IRRELEVANT_VARIABLES)
            patient_corr_data = patient_data.corr(method='spearman')[['Order']].transpose()
            patient_corr_data.drop(columns=['Order'], inplace=True)
            patient_corr_data = patient_corr_data.rename(index={'Order': patient})
            df_list.append(patient_corr_data)

        corr_data = pd.concat(df_list)
        return corr_data

    def get_cutoff_limits(self, series):
        return np.mean(series) - 3 * np.std(series), np.mean(series) + 3 * np.std(series)

    '''
    PLOT METHODS
    '''

    def plot_corr_heatmap(self, show=False, save=True):
        if self.temp_data is None:
            self.temp_data = self.get_data()
        for patient in self.patients:
            patient_data = self.temp_data.loc[self.temp_data.Patient == patient]
            median_data = patient_data.groupby(['Order']).median()
            sd_data = patient_data.groupby(['Order']).std()
            variables = set(patient_data)
            for var in IRRELEVANT_VARIABLES:
                variables.discard(var)
            corr = patient_data[variables].corr(method='spearman')
            corr = pd.melt(corr.reset_index(),
                           id_vars='index')  # Unpivot the dataframe, so we can get pair of arrays for x and y
            corr.columns = ['x', 'y', 'value']
            heatmap(
                x=corr['x'],
                y=corr['y'],
                size=corr['value'].abs(),
                values=corr['value']
            )
            fig = plt.gcf()
            fig.set_size_inches(20, 20)
            if show:
                plt.show()
            if save:
                dirname = os.path.join(PAIR_PLOT_DIRECTORY, patient)
                filename = self.mix + ".png"
                filepath = os.path.join(dirname, filename)
                mkdir_p(dirname)
                plt.savefig(filepath, dpi=100)
        plt.close('all')

    def plot_median_vs_order_in_plate(self, patients=None, show=False, save=True):
        if patients is None:
            patients = self.patients

        if self.temp_data is None:
            self.temp_data = self.get_data()

        variables = set(self.temp_data)
        variables.discard("Order")
        for var in IRRELEVANT_VARIABLES:
            variables.discard(var)

        for var in variables:
            fig = plt.figure()
            ax = plt.subplot(111)

            for patient in patients:
                median_data = self.temp_data.loc[self.temp_data.Patient == patient][[var, "Order"]].groupby(
                    "Order").median()
                median_y = median_data.groupby("Order").median().dropna()
                x = median_y.index.values
                ax.plot(x, median_y, label=patient)

            plt.title(var)
            ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), shadow=True, ncol=2)

            if show:
                plt.show()
            if save:
                dir_name = os.path.join(os.path.join(FEATURE_MEDIAN_BY_PLATE_DIRECTORY, self.mix), self.code)
                mkdir_p(dir_name)
                filename = var + ".png"
                filepath = os.path.join(dir_name, filename)
                plt.savefig(filepath)
            plt.close('all')

    def plot_sd_and_median_vs_order(self, show=False, save=True):
        if self.temp_data is None:
            self.temp_data = self.get_data()

        for patient in self.patients:
            patient_data = self.temp_data.loc[self.temp_data.Patient == patient]
            median_data = patient_data.groupby(['Order']).median()
            sd_data = patient_data.groupby(['Order']).std()
            variables = set(patient_data)
            variables.discard("Order")
            for var in IRRELEVANT_VARIABLES:
                variables.discard(var)
            for var in variables:
                sd_y = sd_data[[var]].dropna()
                median_y = median_data[[var]].dropna()
                x = sd_y.index.values
                fig = plt.figure()
                ax = plt.subplot(111)
                ax.plot(x, sd_y, label='SD')
                ax.plot(x, median_y, label='Median')
                plt.title(var)
                ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), shadow=True, ncol=2)
            if show:
                plt.show()
            if save:
                dir_name = os.path.join(os.path.join(SD_MEDIAN_DIRECTORY, self.code), patient)
                mkdir_p(dir_name)
                filename = var + ".png"
                filepath = os.path.join(dir_name, filename)
                plt.savefig(filepath)
            plt.close('all')

    def plot_mean_and_median_vs_order(self, show=False, save=True):
        if self.temp_data is None:
            self.temp_data = self.get_data()
        for patient in self.patients:
            patient_data = self.temp_data.loc[self.temp_data.Patient == patient]
            median_data = patient_data.groupby(['Order']).median()
            sd_data = patient_data.groupby(['Order']).std()
            variables = set(patient_data)
            variables.discard("Order")
            for var in IRRELEVANT_VARIABLES:
                variables.discard(var)
            for var in variables:
                mean_y = sd_data[[var]].dropna()
                median_y = median_data[[var]].dropna()
                x = mean_y.index.values
                fig = plt.figure()
                ax = plt.subplot(111)
                ax.plot(x, mean_y, label='Mean')
                ax.plot(x, median_y, label='Median')
                plt.title(var)
                ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), shadow=True, ncol=2)
            if show:
                plt.show()
            if save:
                dir_name = os.path.join(os.path.join(SD_MEDIAN_DIRECTORY, self.code), patient)
                mkdir_p(dir_name)
                filename = var + ".png"
                filepath = os.path.join(dir_name, filename)
                plt.savefig(filepath)
            plt.close('all')

    def plot_top_spearman_corr_vs_order(self, show=False, save=True):

        corr_data = self.get_corr_vs_order().pow(2)
        for patient in self.patients:
            fig, ax = plt.subplots(figsize=(12, 12))
            patient_corr = corr_data.loc[patient, :]
            sns.heatmap(patient_corr.sort_values().to_frame().tail(10),
                        vmax=1, vmin=0, cmap="YlGnBu", annot=True, ax=ax)
            plt.yticks(rotation=0)
            ax.invert_yaxis()
            fig = plt.gcf()
            fig.set_size_inches(20, 12)

            if show:
                plt.show()
            if save:
                dirname = os.path.join(os.path.join(PAIR_PLOT_DIRECTORY, patient), "TOP_CORR_VS_ORDER")
                filename = self.mix + ".png"
                filepath = os.path.join(dirname, filename)
                mkdir_p(dirname)
                plt.savefig(filepath, dpi=100)
            plt.close('all')

    def plot_boxplot_vs_order(self, show=False, save=True):
        if self.temp_data is None:
            self.temp_data = self.get_data()
        for patient in self.patients:
            print(patient)
            patient_data = self.temp_data.loc[self.temp_data.Patient == patient]
            variables = set(patient_data)
            variables.discard(IRRELEVANT_VARIABLES)
            variables.discard("Order")
            for var in variables:
                sns.set(style="whitegrid")
                box_plot = sns.boxplot(x="Order", y=var, data=patient_data, color="seagreen")
                fig = plt.gcf()
                fig.set_size_inches(20, 20)
                if show:
                    sns.boxplot(x="Order", y=var, data=patient_data, color="seagreen")
                if save:
                    dirname = os.path.join(os.path.join(BOXPLOT_CHRONO_ORDER_DIRECTORY, patient), self.mix)
                    mkdir_p(dirname)
                    filename = var + ".png"
                    filepath = os.path.join(dirname, filename)
                    box_plot.figure.savefig(filepath)
                plt.close('all')
