from src.resources.tidying_microscopy import *
from src.settings.base_settings import *
from src.resources.qnap_helper import *

if __name__ == "__main__":
    qnap = QnapHelper()
    True
    # patient_codes = get_all_patient_codes()
    # for patient in patient_codes:
    #     all_data = get_tidy_data(patient)
    #     all_data.to_csv(TIDY_DATA_DIRECTORY + str(patient)+".csv")