from src.resources.all_plates import AllPlates
from src.resources.plot_helper import *
from src.resources.tidying_microscopy import *

if __name__ == "__main__":
    all_plates = AllPlates()
    all_plates.plot_merged_spearman_corr_for_mix("ER")
    all_plates.plot_merged_spearman_corr_for_mix("TMRE")

