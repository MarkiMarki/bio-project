from src.resources.all_plates import AllPlates
from src.resources.plot_helper import plot_feature_median_by_plate
from src.settings.tidying_settings import PATIENTS_CODES_BY_PLATE

if __name__ == "__main__":
    all_plates = AllPlates()
    for plate in all_plates.plates:
        print("Plotting " + plate.code)
        plate.plot_median_vs_order_in_plate()
