from src.resources.plot_helper import *
from src.resources.tidying_microscopy import *

if __name__ == "__main__":
    for mix in ["er_lyso", "mito_tmre","merged"]:
        print(mix + "\n ======================================")
        i = 0
        plot_merged_spearman_corr_for_params(
            params=None,
            mix=mix
        )
