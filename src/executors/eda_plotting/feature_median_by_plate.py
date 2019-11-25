from src.resources.plot_helper import plot_feature_median_by_plate
from src.settings.tidying_settings import PATIENTS_CODES_BY_PLATE

if __name__ == "__main__":
    for plate, data in PATIENTS_CODES_BY_PLATE.items():
        plot_feature_median_by_plate(
            plate=plate,
            patient_list=data['patient_codes'],
            mix=data['mix']
        )
