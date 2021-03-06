from src.resources.all_plates import AllPlates
from src.settings.data_settings import SERPENT_ORDERED_ITERATOR

if __name__ == "__main__":
    plot_dirs = {"tidy", "stratified"}
    for plot_dir in plot_dirs:
        all_plates = AllPlates(plot_dir)
        for plate in all_plates.plates:
            print("Plotting " + plate.code)
            print("BOXPLOT")
            plate.plot_boxplot_vs_order()
            print("HEATMAP")
            plate.plot_corr_heatmap()
            print("MEAN MEDIAN")
            plate.plot_mean_and_median_vs_order()
            print("MEDIAN ON PLATE")
            plate.plot_median_vs_order_in_plate()
            print("SD MEDIAN")
            plate.plot_sd_and_median_vs_order()
            print("TOP CORR")
            plate.plot_top_spearman_corr_vs_order()

            plate.temp_data = None

        print("MERGED CORR")
        all_plates.plot_merged_spearman_corr_for_mix("EL")
        all_plates.plot_merged_spearman_corr_for_mix("MT")