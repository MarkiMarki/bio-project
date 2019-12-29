import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from src.resources.utils.plot_utils import heatmap
from src.resources.utils.data_utils import get_ith_number, mkdir_p, does_file_exist
from src.settings.base_settings import FEATURE_MEDIAN_BY_PLATE_DIRNAME, \
    STRATIFIED_DATA_DIRECTORY, SD_MEDIAN_DIRNAME, PAIR_PLOT_DIRNAME, BOXPLOT_CHRONO_ORDER_DIRNAME
from src.settings.plot_settings import IRRELEVANT_VARIABLES
from src.settings.data_settings import SERPENT_ORDERED_ITERATOR, DISCRETE_VARIABLES


class Plate:
    def __init__(self, code, mix, raw_data_paths, tidy_data_dir, stratified_data_dir, patients, plot_from="tidy"):

        # Determine if plots will be generated to stratified or tidy data
        self.plot_from = plot_from

        # Plate metadata
        self.code = code
        self.mix = mix
        self.patients = patients

        # Paths to raw data files
        self.raw_data_paths = raw_data_paths

        # Tidy data paths - create tidy data file if it's absent
        self.tidy_data_dir = tidy_data_dir
        self.path_to_tidy_data = self.get_tidy_data_path()
        if not does_file_exist(self.path_to_tidy_data):
            self.save_tidy_data()

        # Stratified data paths - create stratified data file if it's absent
        self.stratified_data_dir = stratified_data_dir
        self.stratified_data_paths = self.get_stratified_data_paths()
        if not does_file_exist(self.stratified_data_paths[0]):
            self.save_stratified_data()

        # Temporary files: data and plot destination. Determined by plot_from.
        self.temp_data = None
        self.temp_plot_dir = None

    '''
    FILESYSTEM METHODS
    '''

    # Returns a tailored string for the tidy data file
    def get_tidy_data_path(self):
        return os.path.join(self.tidy_data_dir, self.mix + "_" + self.code + ".csv")

    # Returns a tailored string for the stratified data file
    def get_stratified_data_paths(self):
        return [os.path.join(self.stratified_data_dir, patient + "_" + self.mix + "_" + self.code + ".csv")
                for patient in self.patients]

    # Returns a relevant dataframe, and sets the plot destination. Both determined by plot_from.
    def get_data_and_set_plot_dest(self):
        if "tidy" in self.plot_from:
            self.temp_plot_dir = os.path.join(self.tidy_data_dir, "figs")
            return self.get_tidy_data()
        elif "strat" in self.plot_from:
            self.temp_plot_dir = os.path.join(self.stratified_data_dir, "figs")
            return self.get_stratified_data()

    # Returns the tidy dataframe
    def get_tidy_data(self):
        return pd.read_csv(self.path_to_tidy_data, index_col=0)

    # Returns the stratified dataframe
    def get_stratified_data(self):
        return pd.concat([pd.read_csv(path, index_col=0) for path in self.stratified_data_paths])

    # Handles raw data and saves the tidy data
    def save_tidy_data(self):
        print("Saving plate " + self.code)

        # Puts both patient-in-plate dataframes to a list
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

            # Losing TRACKER / TRECKER from feature names
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
                patient_data["Passage"] = new[1].str.split(self.mix, n=1, expand=True)[0].str.split("M", expand=True)[0]
                patient_data["Patient"] = new[0]

            # Getting rid of unwanted variables
            columns_to_drop = [s for s in list(patient_data) if " POS " in s] + \
                              ['Section', 'NUC CG X', 'NUC CG Y']

            # Adding a measurement order variable
            patient_data["Order"] = 0
            j = 0
            for (row, col) in SERPENT_ORDERED_ITERATOR:
                patient_data.loc[(patient_data["Row"] == row) & (patient_data["Col"] == col), 'Order'] = j
                j = j + 1
            patient_data = patient_data.drop(axis=1, labels=columns_to_drop)

            # Add the patient-in-plate dataframe to the list
            df_list.append(patient_data)

        # Concatenates both of patient-in-plate dataframes into one
        all_data = pd.concat(df_list, sort=False)

        mkdir_p(os.path.dirname(self.path_to_tidy_data))
        print("Saving " + self.code + " " + self.path_to_tidy_data)
        all_data.to_csv(self.path_to_tidy_data)

    # Transforms tidy data and saves as stratified data
    def save_stratified_data(self):

        # Stratification will be done on tidy data only
        data = self.get_tidy_data()

        # Separate the plate dataframe to patient-in-plate dataframe
        for patient in self.patients:
            print("Handling " + patient)

            # Gets a subset for the current patient an loses well / field related columns
            patient_data = data.loc[data.Patient == patient].drop(columns=['Col', 'Target', 'Field', 'Row'])

            # Create a set of variables to be treated
            variables = set(patient_data)
            for var in IRRELEVANT_VARIABLES:
                variables.discard(var)

            ###########################################################################
            ############# Subtract the reference (0) from each feature ################
            ###########################################################################

            # For the subset of relevant variables - change 0 values to 0.000001, and log-transform it
            patient_data[list(variables)] = patient_data[list(variables)].replace(0, 0.000001).apply(np.log)

            # Create a dataframe that has the median value for each well for relevant features
            log_median_data = patient_data[variables].groupby("Order").median()

            # Create a series that has the mean of well medians for relevant features
            log_medians_mean = log_median_data.mean()

            # Iterate through the well medians dataframe
            for index, log_median_row in log_median_data.iterrows():
                # For every variable - perform:
                for var in log_medians_mean.index:
                    # Subtract the well median and add the mean of well medians
                    # for current [well, variable] subset of the patients dataframe
                    patient_data.loc[patient_data.Order == index, var] += log_medians_mean[var] - log_median_row[var]

            # Reverse the log transformation with an exponent
            patient_data[list(variables)] = patient_data[list(variables)].apply(np.exp)

            # Creates a set of discrete variables to round back after the transformation
            vars_to_round = DISCRETE_VARIABLES
            if self.mix == "MT":
                vars_to_round.discard("ER COUNT")
                vars_to_round.discard("LYSO COUNT")
            elif self.mix == "EL":
                vars_to_round.discard("MITO COUNT")
                vars_to_round.discard("TMRE COUNT")
            vars_to_round = list(vars_to_round)

            # Perform round for discrete variables
            patient_data[vars_to_round] = patient_data[vars_to_round].round()

            ##########################################################################
            ############# Add the reference (0) from each feature ####################
            ##########################################################################

            print("Saving " + patient)

            # Get the patient-in-well stratified data file path and save to it
            filepath = [path for path in self.stratified_data_paths if patient in str(path)][0]
            mkdir_p(self.stratified_data_dir)
            patient_data.to_csv(filepath)

    '''
    SUMMARY METHODS
    '''

    # Returns a 2-row dataframe - one for each patient.
    # Values are Spearman correlations to measurment order
    def get_corr_vs_order(self):
        df_list = []
        if self.temp_data is None:
            self.temp_data = self.get_data_and_set_plot_dest()
        for patient in self.patients:
            vars_to_drop = IRRELEVANT_VARIABLES.intersection(list(self.temp_data))
            patient_data = self.temp_data.loc[self.temp_data.Patient == patient].drop(columns=vars_to_drop)

            patient_corr_data = patient_data.corr(method='spearman')[['Order']].transpose()
            patient_corr_data.drop(columns=['Order'], inplace=True)
            patient_corr_data = patient_corr_data.rename(index={'Order': patient})
            df_list.append(patient_corr_data)

        corr_data = pd.concat(df_list)
        return corr_data

    # Gets cutoff limits tuple (mean - 3*std, mean + 3*std) for a series
    # Meant to be used as an aggregate function for group_by(Order)
    def get_cutoff_limits(self, series):
        return np.mean(series) - 3 * np.std(series), np.mean(series) + 3 * np.std(series)

    '''
    PLOT METHODS
    '''

    # Spearman correlation heatmap for all variables (pairplot)
    def plot_corr_heatmap(self, show=False, save=True):

        # Retreive data and set plot dir if absent
        if self.temp_data is None:
            self.temp_data = self.get_data_and_set_plot_dest()

        # Get the set of variables and drop irrelevant ones
        variables = set(self.temp_data)
        for var in IRRELEVANT_VARIABLES:
            variables.discard(var)

        # For every patient in plate - perform:
        for patient in self.patients:
            # Get the patient's subset
            patient_data = self.temp_data.loc[self.temp_data.Patient == patient]

            # Get a correlation matrix for all variables
            corr = patient_data[variables].corr(method='spearman')
            corr = pd.melt(corr.reset_index(),
                           id_vars='index')  # Unpivot the dataframe, so we can get pair of arrays for x and y
            corr.columns = ['x', 'y', 'value']

            # Plot the correlation matrix as heatmap with the function implemented in plot_utils
            heatmap(
                x=corr['x'],
                y=corr['y'],
                size=corr['value'].abs(),
                values=corr['value']
            )

            # Modify the plot's size for improved readability
            fig = plt.gcf()
            fig.set_size_inches(20, 20)

            # Present and / or save plot according to the given parameters
            if show:
                plt.show()
            if save:
                dirname = os.path.join(self.temp_plot_dir, PAIR_PLOT_DIRNAME, patient)
                filename = self.mix + ".png"
                filepath = os.path.join(dirname, filename)
                mkdir_p(dirname)
                plt.savefig(filepath, dpi=100)

            # Close all figures to improve performance
            plt.close('all')

    # Plot interpolated medians vs order for both patients in plate
    def plot_median_vs_order_in_plate(self, show=False, save=True):

        # Retreive data and set plot dir if absent
        if self.temp_data is None:
            self.temp_data = self.get_data_and_set_plot_dest()

        # Get the set of variables and drop irrelevant ones
        variables = set(self.temp_data)
        variables.discard("Order")
        for var in IRRELEVANT_VARIABLES:
            variables.discard(var)

        # For every desired variable - perform:
        for var in variables:
            # Create the plot figure
            fig = plt.figure()
            ax = plt.subplot(111)

            # For every patient in plate - perform:
            for patient in self.patients:

                # Get the medians of every well in the patient's subset as Y axis
                median_data = self.temp_data.loc[self.temp_data.Patient == patient][[var, "Order"]].groupby(
                    "Order").median()
                median_y = median_data.groupby("Order").median().dropna()
                # Get the measurement order as X axis
                x = median_y.index.values

                # Plot Y vs X
                ax.plot(x, median_y, label=patient)

            # Set plot title to the variable, add legend to the bottom
            plt.title(var)
            ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), shadow=True, ncol=2)

            # Present and / or save plot according to the given parameters
            if show:
                plt.show()
            if save:
                dir_name = os.path.join(self.temp_plot_dir, FEATURE_MEDIAN_BY_PLATE_DIRNAME, self.mix, self.code)
                mkdir_p(dir_name)
                filename = var + ".png"
                filepath = os.path.join(dir_name, filename)
                plt.savefig(filepath)

            # Close all figures to improve performance
            plt.close('all')

    # Plot interpolated medians and std vs order for every patient in plate
    def plot_sd_and_median_vs_order(self, show=False, save=True):

        # Retreive data and set plot dir if absent
        if self.temp_data is None:
            self.temp_data = self.get_data_and_set_plot_dest()

        # Get the set of variables and drop irrelevant ones
        variables = set(self.temp_data)
        variables.discard("Order")
        for var in IRRELEVANT_VARIABLES:
            variables.discard(var)

        # For every patient in plate - perform:
        for patient in self.patients:

            # Get the patient's subset
            patient_data = self.temp_data.loc[self.temp_data.Patient == patient]

            # Get the median and std grouped by well
            median_data = patient_data.groupby(['Order']).median()
            std_data = patient_data.groupby(['Order']).std()

            # For every desired variable - perform:
            for var in variables:

                # Get the medians and stds of every well in the patient's subset as Y axis
                sd_y = std_data[[var]].dropna()
                median_y = median_data[[var]].dropna()

                # Get the measurement order as X axis
                x = sd_y.index.values

                # Create the plot figure
                fig = plt.figure()
                ax = plt.subplot(111)

                # Plot both Ys vs X
                ax.plot(x, sd_y, label='SD')
                ax.plot(x, median_y, label='Median')

                # Set plot title to the variable, add legend to the bottom
                plt.title(var)
                ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), shadow=True, ncol=2)

                # Present and / or save plot according to the given parameters
                if show:
                    plt.show()
                if save:
                    dir_name = os.path.join(self.temp_plot_dir, SD_MEDIAN_DIRNAME, self.code, patient)
                    mkdir_p(dir_name)
                    filename = var + ".png"
                    filepath = os.path.join(dir_name, filename)
                    plt.savefig(filepath)

                # Close all figures to improve performance
                plt.close('all')

    # Plot interpolated medians and means vs order for every patient in plate
    def plot_mean_and_median_vs_order(self, show=False, save=True):

        # Retreive data and set plot dir if absent
        if self.temp_data is None:
            self.temp_data = self.get_data_and_set_plot_dest()

        # Get the set of variables and drop irrelevant ones
        variables = set(self.temp_data)
        variables.discard("Order")
        for var in IRRELEVANT_VARIABLES:
            variables.discard(var)

        # For every patient in plate - perform:
        for patient in self.patients:

            # Get the patient's subset
            patient_data = self.temp_data.loc[self.temp_data.Patient == patient]

            # Get the median and std grouped by well
            median_data = patient_data.groupby(['Order']).median()
            sd_data = patient_data.groupby(['Order']).std()

            # For every desired variable - perform:
            for var in variables:

                # Get the medians and means of every well in the patient's subset as Y axis
                mean_y = sd_data[[var]].dropna()
                median_y = median_data[[var]].dropna()

                # Get the measurement order as X axis
                x = mean_y.index.values

                # Plot both Ys vs X
                fig = plt.figure()
                ax = plt.subplot(111)

                # Plot both Ys vs X
                ax.plot(x, mean_y, label='Mean')
                ax.plot(x, median_y, label='Median')

                # Set plot title to the variable, add legend to the bottom
                plt.title(var)
                ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), shadow=True, ncol=2)

                # Present and / or save plot according to the given parameters
                if show:
                    plt.show()
                if save:
                    dir_name = os.path.join(self.temp_plot_dir, SD_MEDIAN_DIRNAME, self.code, patient)
                    mkdir_p(dir_name)
                    filename = var + ".png"
                    filepath = os.path.join(dir_name, filename)
                    plt.savefig(filepath)

                # Close all figures to improve performance
                plt.close('all')

    # Plot variables with top Spearman correlation to measurement order
    def plot_top_spearman_corr_vs_order(self, show=False, save=True):

        # Get the correlation vs order matrix and square the values
        corr_data = self.get_corr_vs_order().pow(2)

        # For every patient in plate - perform:
        for patient in self.patients:

            # Create the plot figure
            fig, ax = plt.subplots(figsize=(12, 12))

            # Get the patient's subset of correlation data
            patient_corr = corr_data.loc[patient, :]

            # Sort the correlation values, get top 10, and plot to a heatmap
            sns.heatmap(patient_corr.sort_values().to_frame().tail(10),
                        vmax=1, vmin=0, cmap="YlGnBu", annot=True, ax=ax)

            # Plot cosmetics
            plt.yticks(rotation=0)
            ax.invert_yaxis()
            fig = plt.gcf()
            fig.set_size_inches(20, 12)

            # Present and / or save plot according to the given parameters
            if show:
                plt.show()
            if save:
                dirname = os.path.join(self.temp_plot_dir, PAIR_PLOT_DIRNAME, patient, "TOP_CORR_VS_ORDER")
                filename = self.mix + ".png"
                filepath = os.path.join(dirname, filename)
                mkdir_p(dirname)
                plt.savefig(filepath, dpi=100)

            # Close all figures to improve performance
            plt.close('all')

    # Plot boxplots of every variable vs order for every patient in plate
    def plot_boxplot_vs_order(self, show=False, save=True):

        # Retreive data and set plot dir if absent
        if self.temp_data is None:
            self.temp_data = self.get_data_and_set_plot_dest()

        # Get the set of variables and drop irrelevant ones
        variables = set(self.temp_data)
        variables.discard("Order")
        for var in IRRELEVANT_VARIABLES:
            variables.discard(var)

        # For every patient in plate - perform:
        for patient in self.patients:

            # Get the patient's subset
            patient_data = self.temp_data.loc[self.temp_data.Patient == patient]

            # For every desired variable - perform:
            for var in variables:

                # Plot boxplot of values vs order
                sns.set(style="whitegrid")
                box_plot = sns.boxplot(x="Order", y=var, data=patient_data, color="seagreen")

                # Plot cosmetics
                fig = plt.gcf()
                fig.set_size_inches(20, 20)

                # Present and / or save plot according to the given parameters
                if show:
                    sns.boxplot(x="Order", y=var, data=patient_data, color="seagreen")
                if save:
                    dirname = os.path.join(self.temp_plot_dir, BOXPLOT_CHRONO_ORDER_DIRNAME, patient, self.mix)
                    mkdir_p(dirname)
                    filename = var + ".png"
                    filepath = os.path.join(dirname, filename)
                    box_plot.figure.savefig(filepath)

                # Close all figures to improve performance
                plt.close('all')
