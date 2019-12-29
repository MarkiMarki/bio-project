from ..resources import tidying_microscopy, qnap_helper
from ..settings import base_settings

if __name__ == "__main__":
    qnap = qnap_helper.QnapHelper()
    pass
    # patient_codes = get_all_patient_codes()
    # for patient in patient_codes:
    #     all_data = get_tidy_data(patient)
    #     all_data.to_csv(TIDY_DATA_DIRECTORY + str(patient)+".csv")