#####################################
######## Stage 1 (3 steps) ########## 
####### Data pre-processing  ########
#####################################


## Step 1
## upload chosen examples data 
## take Criterions
## run criterion-filters on all data

## Step 2
## Stratify data by: [] with the four situations
## Fit Distributions
## Take moments

## Step 3
## Unify different wells with chosen test
## Start cluster features....

## Classes and Sub Classess

import os
import xlrd




cwd = os.getcwd()
loc = os.chdir('C:/Users/MarkiMaxI/Desktop/DQE Home/Done/Annotated/ER LYSO/S6P2')
dirdata = os.listdir(loc)

for excel in dirdata:               
    print(excel)


Data = xlrd.open_workbook(dirdata[0])    #xlrd.open_workbook(filename=None, logfile=<_io.TextIOWrapper name='<stdout>' mode='w' encoding='UTF-8'>, verbosity=0, use_mmap=1, file_contents=None, encoding_override=None, formatting_info=False, on_demand=False, ragged_rows=False)
#Data = xlrd.open_workbook('6h_Mark.xls')
worksheet = Data.sheet_by_name('Sheet1')
print(worksheet.nrows) 
dir(worksheet)

wells_list = []
for i in range(worksheet.nrows):
    well = str.format('{}{}', worksheet.row_values(i)[2],worksheet.row_values(i)[3])
    if well not in wells_list:
        wells_list.append(well)
wells_list.remove('')





