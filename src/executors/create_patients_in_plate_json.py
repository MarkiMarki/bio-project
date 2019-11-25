from src.resources.tidying_microscopy import group_patients_by_plate
from src.settings.base_settings import *
import json

if __name__ == "__main__":
    patient_vs_plate = group_patients_by_plate()
    with open(BASE_DATA_DIRECTORY+'patient_by_plate.json', 'w') as fp:
        json.dump(patient_vs_plate, fp)