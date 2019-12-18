from src.resources.all_plates import AllPlates

# Plots correlarion heatmap for all variables / sorted R squared against chronological order (decided in plot_settings)
if __name__ == "__main__":
    all_plates = AllPlates()
    for plate in all_plates.plates:
        print("Plotting " + plate.code)
        plate.plot_corr_heatmap()






