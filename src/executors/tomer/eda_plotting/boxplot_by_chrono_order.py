from src.resources.all_plates import AllPlates

# Plot all variables against chronological order, grouped with boxplots

if __name__ == "__main__":
    all_plates = AllPlates()
    for plate in all_plates.plates:
        print("Plotting " + plate.code)
        plate.plot_boxplot_vs_order()
