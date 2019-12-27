from src.resources.all_plates import AllPlates

if __name__ == "__main__":
    all_plates = AllPlates()
    for plate in all_plates.plates:
        print("Plotting "+ plate.code)
        plate.plot_sd_and_median_vs_order()
