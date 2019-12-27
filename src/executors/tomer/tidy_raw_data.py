from src.resources.all_plates import AllPlates

# Execute this file to transform all raw phenotyping data to tidy data

if __name__ == "__main__":
    all_plates = AllPlates("tidy")
    all_plates.save_tidy_data()