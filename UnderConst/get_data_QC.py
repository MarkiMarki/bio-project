#################################
### Read data from parsed xls ###
#################################

##### EVERyTHING is OBSERV and NOT CELLS yet, wating for after qc

import os
import xlrd

from scipy import stats
from scipy.stats import gmean
from scipy.stats import hmean
from scipy.stats import tstd

cwd = os.getcwd()
loc = os.chdir('C:/Users/MarkiMaxI/Desktop/DQE Home/Done/Annotated/ER LYSO/S6P2')
dirdata = os.listdir(loc)

for excel in dirdata:               
    print(excel)

Data = xlrd.open_workbook(dirdata[0])               
worksheet = Data.sheet_by_name('Sheet1')


# Choose excel by name
# upload a parsed xls file
# read and save sheet
###########################
# read sample's & group's id + verify all rows
###########################

sample_group = worksheet.row_values(2)[0]
for i in range(3, worksheet.nrows):
    if worksheet.row_values(i)[0] == sample_group:
        continue
    else:
        print('The xls file is not parsed correctly- More then one GROUP!  check it please')

sample_name = worksheet.row_values(2)[1]
for i in range(3, worksheet.nrows):
    if worksheet.row_values(i)[1] == sample_name:
        continue
    else:
        print('The xls file is not parsed correctly- More then one SAMPLE! please check it')

###########################
# read wells of experiment + total number of wells
###########################

sample_wells = []
for i in range(2, worksheet.nrows):
    well = str.format('{}{}', worksheet.row_values(i)[2],int(worksheet.row_values(i)[3]))
    if well not in sample_wells:
        sample_wells.append(well)

wells_num = len(sample_wells)

# total number of obsdervations

observ_num = worksheet.nrows - 2

###########################
# number of observations per well & per field

# sample_fields = []
# for i in range(2, worksheet.nrows):
#     field = str.format('fld{}', worksheet.row_values(i)[4][-3:-1])             
#     field = field.replace(" ","")
#     if field not in sample_fields:
#         sample_fields.append(field)

sample_fields = []
for i in range(2, worksheet.nrows):
    field = worksheet.row_values(i)[4]
    if field not in sample_fields:
        sample_fields.append(field)

field_num = len(sample_fields)


###########################
# create a list observ per field

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

min(fields_in_wells)
minloc = fields_in_wells.index(min(fields_in_wells))
sample_fields[minloc]

max(fields_in_wells)
maxloc = fields_in_wells.index(max(fields_in_wells))
sample_fields[maxloc]
    
full_observ_fields = dict(zip(sample_fields, fields_in_wells))


###########################
# all CELL AREA sizes per field 

features = worksheet.row_values(1)[6:] # Features names

# all cell areas in a field
cell_area_fields = [[] for x in range(0,field_num)]

for j in range(field_num):
    for i in range(2, worksheet.nrows):
        if sample_fields[j] == worksheet.row_values(i)[4]:  #worksheet.row_values(i)[34]: 
            cell_area_fields[j].append(worksheet.row_values(i)[34]) 

#newzip = dict(zip(full_observ_fields,cell_area_fields))

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



######################
## count cells per Well


obsrv_num_well = [[0] for x in range(0,wells_num)]

for j in range(wells_num):
    for i in range(2, worksheet.nrows):
        if sample_wells[j] == str.format('{}{}', worksheet.row_values(i)[2],int(worksheet.row_values(i)[3])):
            obsrv_num_well[j][0] += 1 

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