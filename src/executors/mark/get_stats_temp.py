import os

cwd = os.getcwd()
loc = os.chdir('D:\IftachN14\Desktop\DQE\Phenotyping Assay\Data\AOBI')

import xlrd
Data = xlrd.open_workbook('MarkM AOBI.2019.08.22.00.12.30.xls')
sheets = wb.sheet_by_index(0)


for sheets in Data
    print(sheets)