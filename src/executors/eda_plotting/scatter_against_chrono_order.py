from src.resources.plot_helper import *
from src.resources.tidying_microscopy import *


def plot_all_variables_against_chrono_order(data, code, show=False, save=True):
    variables = set(data)
    variables.remove("CHRONO_ORDER")
    for var in variables:
        measurement_data.plot.scatter(x="CHRONO_ORDER", y=var)
        if show:
            plt.show()
        if save:
            fig = plt.gcf()
            fig.set_size_inches(20, 20)
            filename = code + "\\" + var + ".png"
            plt.savefig(SCATTER_CHRONO_ORDER_DIRECTORY + filename, dpi=100)


if __name__ == "__main__":
    measurement_codes = get_all_measurement_codes("tidy")
    measurement_count = len(measurement_codes)
    i = 0
    for measurement_code in measurement_codes:
        i += 1
        print("Processing " + measurement_code + ": {index} / {length}".format(index=i, length=measurement_count))
        measurement_path = os.path.join(TIDY_DATA_DIRECTORY, measurement_code + ".csv")
        measurement_data = pd.read_csv(measurement_path, index_col=0)
        mkdir_p(SCATTER_CHRONO_ORDER_DIRECTORY + measurement_code + "\\")
        plot_all_variables_against_chrono_order(
            data=measurement_data,
            code=measurement_code
        )
