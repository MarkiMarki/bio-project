#########################################################################################
# Name Your features, Take dir with samples                                             #
# Loop on each sample with chosen features & take:                                      #
#                                                                                       #
# sample_group, sample_barcode, observ_num, allfields , allwells, allcols, my_feature,  #
# feature_data_field, feature_sum_fields, feature_avg_fields                            #
# feature_data_well, feature_sum_wells, feature_avg_wells, my_vec                       #
#########################################################################################

import sys, os 
import xlrd
import numpy as np 
import scipy as sc
import pandas as pd

from scipy import stats
from scipy.stats import gmean
from scipy.stats import hmean
from scipy.stats import tstd
from scipy.stats import tvar
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

###### Choose a Feature ######
my_features = ['NUCLEAR_INTENSITY', 'NUCLEAR_AREA', 'CELL_INTENSITY','CELL_AREA']
my_features_data = [[] for x in my_features]
##############################

mydir = 'C:/Users/MarkiMaxI/Desktop/DQE Home/Done/Annotated/ER LYSO/allxls'
locroot = os.chdir(mydir)
path = os.getcwd()
myfiles = []

dirdata = os.listdir(path)

for count,excel in enumerate(dirdata):               
    print('Working on', excel,'- sample #', count,'out of', len(dirdata), 'samples' )
    myfiles.append(excel)
    Data = xlrd.open_workbook(dirdata[count])               
    worksheet = Data.sheet_by_name('Sheet1')
    sample_group, sample_barcode = worksheet.row_values(2)[0], worksheet.row_values(2)[1]
    for i in range(3, worksheet.nrows):
        if worksheet.row_values(i)[0] == sample_group and worksheet.row_values(i)[1] == sample_barcode:
            continue
        else:
            print('The xls file is not parsed correctly- More then one Sample or Group in the xls! check it please')
    for jj in range(len(my_features)):
        my_feature = my_features[jj]
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
        observ_num = worksheet.nrows - 2
        fields_in_wells = [[0] for x in range(0,field_num)]
        for j in range(field_num):
            for i in range(2, worksheet.nrows):
                if sample_fields[j] == worksheet.row_values(i)[4]: 
                    fields_in_wells[j][0] += 1 
        allfields = [field[0] for field in fields_in_wells]
        count_obsrv = 0 
        for i in range(field_num):
            count_obsrv += fields_in_wells[i][0] 
        if count_obsrv >= observ_num:                           ## check size thingi
            print("OK- got all fields")
        else:
            print("Something went wrong- didnt catch all FIELDS observations!")
        obsrv_num_well = [[0] for x in range(0,wells_num)]
        for j in range(wells_num):
            for i in range(2, worksheet.nrows):
                if sample_wells[j] == str.format('{}{}', worksheet.row_values(i)[2],int(worksheet.row_values(i)[3])):
                    obsrv_num_well[j][0] += 1 
        allwells = [well[0] for well in obsrv_num_well]
        ## validate that all observs per well were counted
        total_wells_obsrv = 0
        for well in range(wells_num):
            total_wells_obsrv += obsrv_num_well[well][0] 
        if observ_num == total_wells_obsrv:
            print('Ok - got all Wells')
        else:
            print('Missed obsrv of some well.. check what happend')
        sample_cols = []
        for i in range(2, worksheet.nrows):
            mycol = worksheet.row_values(i)[3]
            if mycol not in sample_cols:
                sample_cols.append(mycol)
        cols_num = len(sample_cols)
        cols_count = [[] for x in range(cols_num)]
        for j in range(cols_num):
            for i in range (2, worksheet.nrows):
                if sample_cols[j] == worksheet.row_values(i)[3]:
                    cols_count[j].append(i)
        allcols = [len(col) for col in cols_count]
        ### Get all Feature
        features = worksheet.row_values(1)[6:] 
        for i in range(len(features)):
            features[i] = features[i].replace(" ","_")
        ## Choose a Feature, take its position
        for feature in features:
            if feature == my_feature:
                feat_pos = features.index(my_feature) 
                print(('My feature is {}; its position\'s index is {}').format(my_features[jj], features.index(my_feature)))
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
        data_pos = feat_pos + 6
        my_vec = worksheet.col_values(data_pos)[2:]
        my_features_data[jj].append([sample_group, sample_barcode, observ_num, allfields , allwells, allcols, my_feature, feature_data_field, feature_sum_fields, feature_avg_fields,feature_data_well, feature_sum_wells, feature_avg_wells, my_vec])

########################################  0 ###########  1  #########  2  #######  3  ######  4  ####  5  ######  6  #########  7  ##############  8  ###################  9  ##############  10  ##########  11  ##########  12  #############  13  ################################################################################



fields_ratio = [[] for z in range(len(my_features_data[0]))] 
                                        
for nn in range(len(my_features_data[0])):                             # go through all samples         
    for mm in range(len(my_features_data[0][nn][10])):
        field_ratio = [my_features_data[1][nn][10][mm][x]/my_features_data[3][nn][10][mm][x] for x in range(len(my_features_data[0][nn][10][mm]))]
        fields_ratio[nn].append(field_ratio) 

y = [len(fields_ratio[0][x]) for x in range(len(fields_ratio[0]))]
yy = sum(y)

#         print(my_features_data[0][nn][4][mm])
    
#     lenratio = range(my_features_data[0]nn[][][])
#     for mm in range(my_features_data[][][][] len(my_features_data[0][nn][10][]))
#     for field in my_features_data[0][nn][4][field]:
#         print(str(field))
#     x = 
#     field_ratio = [my_features_data[1][nn][10][x]/my_features_data[3][nn][10][x] for x in range(len(my_features_data[0][nn][10]))]      # one ratio!
    

suum = sum(field_ratio)



# NUCLEAR_INTENSITY_SUM = []
# NUCLEAR_AREA_SUM = []
# CELL_INTENSITY_SUM = []
# CELL_AREA_SUM = []
# tooki = []
# nucarea = []
# cellarea = []
# cellintens = []