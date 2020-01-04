# Iftach Nachman's lab ND project

### Build instructions

1. Clone repository to your local machine
2. Move to project's root folder

    `cd path/to/project/`
3. Install requirements with pip
    
    `pip install -f "requirements.txt"`

4. Download the raw data to /data/raw_data/

5. Verify every .xls file has the following pattern:
    
    [Condition][Patient code]\_[Passage]\_[Mix]\_[Plate code].xls
    
    i.e: FA0337_5_MT_S2P1.xls means:
    - Condition = FA
    - Patient = 0337
    - Mix = MT
    - Plate = S2P1

### Project's structure
data/ - Where datasets and related plots live. After the project's initialization, it should contain 3 datasets: raw, tidy, and stratified

src/ - The project's source code: executors, resources, and settings files

src/executors/ - Scripts to run in order to process the data and create descriptive plots

src/resources/ - Classes and utility functions   

src/settings/ - Global settings for the project

abspath_routing.py - Provides the project's settings with the root absolute path

### How to use

###### Understanding the Plate object:

The Plate object represents a plate measurement. 
The plate consists of 1-3 patients' cells that are dyed with a specific mix: 
ER-LYSO (EL) or MITO-TMRE (MT)

A Plate has 3 purposes:
1. Tidy the raw data into an easily manageable .csv file
2. Stratify the tidy data (Eliminate the between-well effect) and save it as a .csv file
3. Plot descriptive plots for any dataset (tidy or stratified)

Creating a Plate takes a few parameters:

- code: plate's code 
- mix: the plate's mix. Can be "EL" or "MT" 
- raw_data_paths: The paths to the raw data .xls files. By rule these are the files that their name ends with the plate's code
- tidy_data_dir: A path leading to the directory in which the tidy data is stored
- stratified_data_dir: A path leading to the directory in which the stratified data is stored
- patients: A list of the plat patient codes
- plot_from: Determines which dataset to use for plots

Upon instantiation, the object will also generate the filepaths for the tidy and stratified data. 
If these files are absent, it will create them from the raw data by tidying and then stratifying it.

Afterwards, the Plate can be used to plot descriptive statistics. These will be saved in the dataset folder under /figs

###### Understanding the AllPlates object:

An AllPlates object represents the whole database and the functions that can be done with it.
By instantiating an AllPlates objects you don't need to provide any parameter but the defaults can be modified:

- plot_from="tidy": Determines which dataset to use for plots
- raw_data_dir=None : Directory name for the raw data. If left None, it will be set to default (raw_data)
- tidy_data_dir=None : Directory name for the tidy data. If left None, it will be set to default (tidy_data)
- stratified_data_dir=None : The Directory name for the stratified data. If left None, it will be set to default (stratified_data)

Instantiating an AllPlates objects with modified data directories, will create these folders and put the respective data and plots in them.

###### Running the scripts:

To follow defaults, just run the eda_plotting.py file in the executors folder. 
It will process the data as necessary and provide all plots in the respective dataset folders.
On first start, will take lots of time to complete.

If you decided to update tidying/stratification methods, you will have to re-create the tidy and stratified datasets.
In order to do so, run the  tidy_raw_data.py or stratify_tidy_data.py accordingly



