from src.resources.all_plates import AllPlates

if __name__ == "__main__":
    all_plates = AllPlates()
    all_plates.plot_merged_spearman_corr_for_mix("ER")
    all_plates.plot_merged_spearman_corr_for_mix("TMRE")

