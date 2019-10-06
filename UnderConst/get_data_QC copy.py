########################################
########### Step 1 out of 3 ############
## QC for images by chosen parameters ##
########################################

############################################
### The files & folders from read_xls.py ###
########## data type : parsed xls ##########

##### EVERyTHING is OBSERV and NOT CELLS yet, wating for after qc #####

## First: choose good and bad examples, upload then and keep S, P, ID and positions (well & field) 

import os
import xlrd
# import scipy as 

import numpy as np 

from scipy import stats
from scipy.stats import gmean
from scipy.stats import hmean
from scipy.stats import tstd

## use readymade files + folders lists (read_xls. or something)

good_names = ['.xls', '.xls', 'xls']
bad_names  = ['.xls','.xls', '.xls']

# Currently : go to plate's location

# upload a parsed xls file
cwd = os.getcwd()
loc = os.chdir('C:/Users/MarkiMaxI/Desktop/DQE Home/Done/Annotated/ER LYSO/S6P2')
dirdata = os.listdir(loc)

for excel in dirdata:               
    print(excel)

# choose which worksheet, # Choose excel by location in 'dirdata'
Data = xlrd.open_workbook(dirdata[0])               
worksheet = Data.sheet_by_name('Sheet1')
# read and save sheet

## Exam and determined prior cutoffs' of differrent features as variabls for later input as constrains, these are:

'''
Criterions:

1. Uniformity of observations = number per: 
    
    per fields              # determine min-max Threshold's \ cutoff's for all (more?)
    pwe wells               
    per Sample              
    per Group-avg?          
    per plate              
    per Batch              
    per Other data (Passage? Gender?) 

2. Specific Features: [determined by "good" wells\fields]
    
    Intensities per Field\ Well\ Sample\ Group\ Plate\ Batch
    Cell area size (+ 3Xstd as bounderis?) per...
    Denstiy-scaterness per...
    # of nuclei per field\wells\sample  (normalize?) 
    # of nuclei per CELL AREA ratio per...  (for double seg (segmented together), confluency?, what else?)

3. General criterions;

    if Total # of observations that was dismissed exceeds 40% per sample; dismiss sample
    for well?
    for field?
    what else?

'''

############################################ AS A SAMPLE #######################################################


###########################
# read sample's & group's id + verify all rows belongs to a sample
###########################

sample_group, sample_barcode = worksheet.row_values(2)[0], worksheet.row_values(2)[1]
for i in range(3, worksheet.nrows):
    if worksheet.row_values(i)[0] == sample_group and worksheet.row_values(i)[1] == sample_barcode:
        continue
    else:
        print('The xls file is not parsed correctly- More then one Sample or Group in the xls! check it please')



###########################
# Read all wells & fields of experiment
###########################


sample_wells = []
for i in range(2, worksheet.nrows):
    well = str.format('{}{}', worksheet.row_values(i)[2],int(worksheet.row_values(i)[3]))
    if well not in sample_wells:
        sample_wells.append(well)

wells_num = len(sample_wells)

sample_fields = []
for i in range(2, worksheet.nrows):
    field = worksheet.row_values(i)[4]
    if field not in sample_fields:
        sample_fields.append(field)

field_num = len(sample_fields)


###########################
## 1. Take Uniformity' of observations Data
###########################

## total number of obsdervations per Sample

observ_num = worksheet.nrows - 2

###########################
# number of observations per per field

# create a list observ per field per well (loc by list index?)
fields_in_wells = [[0] for x in range(0,field_num)]

for j in range(field_num):
    for i in range(2, worksheet.nrows):
        if sample_fields[j] == worksheet.row_values(i)[4]: 
            fields_in_wells[j][0] += 1 

###########################
# Validate counting all

count_obsrv = 0 
for i in range(field_num):
    count_obsrv += fields_in_wells[i][0] 

if count_obsrv >= observ_num:                           ## check size thingi
    print("OK, Got it")
else:
    print("Something went wrong- didnt catch all observations :(")

min(fields_in_wells)                                        # smallest obsrv per field
minloc = fields_in_wells.index(min(fields_in_wells))        # location of smallest obsrv per field
sample_fields[minloc]                                       # min well identity

max(fields_in_wells)
maxloc = fields_in_wells.index(max(fields_in_wells))
sample_fields[maxloc]
    
full_observ_fields = dict(zip(sample_fields, fields_in_wells))    # Dictionary for fields' data


###########################
# number of observations per Well

obsrv_num_well = [[0] for x in range(0,wells_num)]
for j in range(wells_num):
    for i in range(2, worksheet.nrows):
        if sample_wells[j] == str.format('{}{}', worksheet.row_values(i)[2],int(worksheet.row_values(i)[3])):
            obsrv_num_well[j][0] += 1 


## validate that all observs per well were counted
total_wells_obsrv = 0
for well in range(wells_num):
    total_wells_obsrv += obsrv_num_well[well][0] 

if observ_num == total_wells_obsrv:
    pass
else:
    print('Missed obsrv of some well.. check what happend')
    
full_observ_wells = dict(zip(sample_wells,obsrv_num_well))    



###########################
## 2. Take Uniformity' of specific features Data;
###########################

### Get all Feature

features = worksheet.row_values(1)[6:] 
for i in range(len(features)):
    features[i] = features[i].replace(" ","_")


## Choose a Feature, take its position

my_feature = 'NUCLEAR_INTENSITY'
for feature in features:
    if feature == my_feature:
        feat_pos = features.index(my_feature) 
        print(('my_feature index position is {}').format(features.index(my_feature))) 


### Collect its data per Field \ Well

## Per field

feature_data_field = [[] for x in range(0,field_num)]
for j in range(field_num):
    for i in range(2, worksheet.nrows):
        if sample_fields[j] == worksheet.row_values(i)[4]:  #worksheet.row_values(i)[34]: 
            feature_data_field[j].append(worksheet.row_values(i)[feat_pos+6])

# Sum of my_feature counts per field 

feature_sum_fields = [[] for x in range(field_num)]
for ii in range(field_num):
    feature_sum_fields[ii] = sum(feature_data_field[ii])

## Feature sum / obsrv number Per Field

feature_avg_fields = [[] for x in range(field_num)]
for ii in range(field_num):
    feature_avg_fields[ii] = sum(feature_data_field[ii])/len(feature_data_field[ii])


## Per Well

feature_data_well = [[] for x in range(0,wells_num)]
for j in range(wells_num):
    for i in range(2, worksheet.nrows):
        if sample_wells[j] == str.format('{}{}', worksheet.row_values(i)[2],int(worksheet.row_values(i)[3])):   
            feature_data_well[j].append(worksheet.row_values(i)[feat_pos+6])

# Sum of my_feature counts per Well 

feature_sum_wells = [[] for x in range(wells_num)]
for ii in range(wells_num):
    feature_sum_wells[ii] = sum(feature_data_well[ii])

## Feature sum / obsrv number Per Well

feature_avg_wells = [[] for x in range(wells_num)]
for ii in range(wells_num):
    feature_avg_wells[ii] = sum(feature_data_well[ii])/len(feature_data_well[ii])


## Per Sample obsrv;
data_pos = feat_pos + 6
my_vec = worksheet.col_values(data_pos)[2:]

# call with: my_feature, my_vec, data_pos
def get_sample_data(feature_name,Vector,Col_num):
    feat_mean =scipy.stats.tmean(my_vec)
    feat_std = scipy.stats.tstd(my_vec)
    feat_min  = min(my_vec)
    feat_median = np.median(my_vec)
    feat_max  = max(my_vec)
return feat_mean, feat_std, feat_min, feat_median, feat_max

my_wells_data = feature_data_well

# call with: my_wells_data
def get_wells_data(wells_data):
    wells_data = [[] for x in sample_wells]
    for j in range(wells_num):
        wells_data[j] = [scipy.stats.tmean(wells_data[j]), scipy.stats.tstd(my_vec), min(wells_data), np.median(wells_data), max(wells_data)]
    return wells_data

def feat_mean_well(wells_data):
    for i in range(len(wells_data)):
        wells_data[]

    wells_tmean = [j for max(feature_data_well[j]) in feature_data_well[j]] 
    wells_tstd  =  
    wells_min   =
    wells_median = 
    wells_max   =
def sample_sum():
    "outputs summed feature's data for a sample"
    print(("Sample {} was have n={} observations in {} wells (and {} fields)").format(sample_barcode,observ_num, wells_num, field_num))
    print(("The feature {} have {}{}{} as mean, avg and std per Well").format(my_feature,))
    print(("Min, Max and Median values per Well are {}{}{}, accordingly").format(,))
    print(("The feature {} have {}{}{} as mean, avg and std per Field").format(my_feature,))
    print(("Min, Max and Median values per Field are {}{}{}, accordingly").format(,))


## ADD: 

##    Plots of: funtions per...


'''

describe          -- Descriptive statistics
       gmean             -- Geometric mean
       hmean             -- Harmonic mean
       kurtosis          -- Fisher or Pearson kurtosis
       kurtosistest      --
       mode              -- Modal value
       moment            -- Central moment
       normaltest        --
       skew              -- Skewness
       skewtest          --
       kstat             --
       kstatvar          --
       tmean             -- Truncated arithmetic mean
       tvar              -- Truncated variance
       tmin              --
       tmax              --
       tstd              --
       tsem              --
       variation         -- Coefficient of variation
       find_repeats
       trim_mean


'''






## Nuc Intensity per Field \ Well 


## Nuc Number Per Field \ Well


## Nuc Size Per Field \ Well









'''
Intensities per Field\ Well\ Sample\ Group\ Plate\ Batch
    Cell area size (+ 3Xstd as bounderis?) per...
    Denstiy-scaterness per...
    # of nuclei per CELL AREA ratio per...  (for double seg (segmented together), confluency?, what else?)
'''



## Determined constrains cutt off's and boundries:





# sample_fields = []
# for i in range(2, worksheet.nrows):
#     field = str.format('fld{}', worksheet.row_values(i)[4][-3:-1])             
#     field = field.replace(" ","")
#     if field not in sample_fields:
#         sample_fields.append(field)






###########################
# all CELL AREA sizes per field 



# all cell areas in a field
cell_area_fields = [[] for x in range(0,field_num)]

for j in range(field_num):
    for i in range(2, worksheet.nrows):
        if sample_fields[j] == worksheet.row_values(i)[4]:  #worksheet.row_values(i)[34]: 
            cell_area_fields[j].append(worksheet.row_values(i)[34]) 


# get sum of all CELL AREA per field
cellarea_scoresF = [[] for x in range(field_num)]
for ii in range(field_num):
    cellarea_scoresF[ii] = sum(cell_area_fields[ii])

## density?: Cell area \ observs per field

cellarea_dens_F = [[] for x in range(field_num)]

for jj in range(field_num):
    cellarea_dens_F[jj]=[sample_fields[jj],cellarea_scoresF[jj]/fields_in_wells[jj][0]]
    
print("Density Done!")    

gmean(cellarea_scoresF)
tstd(cellarea_scoresF)
        
# sizeperfield = dict(zip()) # scoresF + num of obsrv per field###########################


###########################
# Cell area sizes per well #

cell_area_wells = [[] for x in range(wells_num)]

for ii in range(wells_num):
    for jj in range(2, worksheet.nrows):
        if str.format('{}{}', worksheet.row_values(jj)[2],int(worksheet.row_values(jj)[3])) == sample_wells[ii]:
            cell_area_wells[ii].append(worksheet.row_values(jj)[34])

# validate: that all observs per well were counted

for i in range(wells_num):
    if len(cell_area_wells[i]) == obsrv_num_well[i][0]:
        continue
    else:
        print('Missed an obsrv of some well.. check what happend')

cellarea_scoresW = [[] for x in range(wells_num)]   # Total obsrvs' areas' per WELL
cellarea_densW   = [[] for y in range(wells_num)]   # Total obsrvs' areas' per WELL

for ii in range(wells_num):
    cellarea_scoresW[ii] = sum(cell_area_wells[ii])

for jj in range(wells_num):
    cellarea_densW[jj] = [sample_wells[jj], sum(cell_area_wells[jj])/len(cell_area_wells[jj])]



#sizeperwells = dict(zip())

gmean(cellarea_scoresW)         # cellarea_densW
tstd(cellarea_scoresW)


###########################
# Cell area size per column

cols = []
for kk in range(wells_num):
    if sample_wells[kk][1:] not in cols:
        cols.append(sample_wells[kk][1:])
        
cellarea_cols = [[] for x in range(len(cols))]

for mm in range(len(cols)):
    for nn in range(2, worksheet.nrows):
        if cols[mm] == str(int(worksheet.row_values(nn)[3])):
            cellarea_cols[mm].append(worksheet.row_values(nn)[34])

# validate full count with summed cellarea_scoresW
if tt in range(len(cols)):
    if sum(cellarea_cols[tt]) == sum 
    




features.cell_area = 1


####################################
## Same for the INTENSITY FEATURE ##
######################################################
## Same for the both Nuc INTENSITY and Area FEATURE ##
######################################################


# keys = ['a', 'b', 'c']
# values = [1, 2, 3]
# dictionary = dict(zip(keys, values))
# print(dictionary)
# {'a': 1, 'b': 2, 'c': 3}



## upload patient data (one by one)

## Test determined constrains cutt-offs, keep result as %: # of passing observations for each sample / from its total observations#  







############################################ AS Groups\ Batchs \ Mixes #######################################################

###########################
# number of observations per Plate \ Batch \ Group