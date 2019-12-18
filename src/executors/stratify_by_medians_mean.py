from src.resources.all_plates import AllPlates

if __name__ == "__main__":
    all_plates = AllPlates("tidy")
    for plate in all_plates.plates:
        print("Plate " + plate.code)
        plate.save_mean_median_stratified_data()