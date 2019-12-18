
# Variables that are not needed for heatmaps
IRRELEVANT_VARIABLES = {
    "Row",
    "Col",
    "Target",
    "Field",
    "Passage",
    "Condition",
    "Patient",
}

# If True: plot_measurement_corr_heatmap() will plot a sorted list of R squares against HEATMAP_TARGET_VARIABLE
# If False: plot_measurement_corr_heatmap() will plot a correlation heatmap for all variables
RESTRICT_HEATMAP_VARIABLES = False
HEATMAP_TARGET_VARIABLE = "CHRONO_ORDER"
