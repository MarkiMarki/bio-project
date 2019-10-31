import numpy as np

# Variable names that didn't read properly are replaced using this mapper
COLUMN_RENAME_MAPPER = {
    'Unnamed: 0': 'Condition',
    'Unnamed: 1': 'Patient',
    ' ': 'Row',
    ' .1': 'Col'
}

# Creation of the serpent iterator - list of (row,col) tuples ordered by chronological order
SERPENT_ORDERED_ITERATOR = []
for row in 'BCDEFG':
    sqn = list(np.arange(2, 12))
    if row in 'CEF': sqn.reverse()
    for col in sqn:
        SERPENT_ORDERED_ITERATOR += [(row, col)]

# Sets of mix-specific variables
TMRE_UNIQUE_VARIABLES = {
    "TMRE AREA",
    "TMRE INTENSITY",
    "TMRE FORM FACTOR",
    "TMRE COUNT",
    "TMRE DxA",
    "MITOTRECKER AREA",
    "MITOTRACKER DxA",
    "MITOTRACKER FORM FACTOR",
    "MITOTRACKER INTENSITY",
    "MITOTRACKER COUNT",
}
ER_LYSO_UNIQUE_VARIABLES = {
    "ER AREA",
    "ER INTENSITY",
    "ER FORM FACTOR",
    "ER COUNT",
    "ER DxA",
    "LYSO AREA",
    "LYSO DxA",
    "LYSO FORM FACTOR",
    "LYSO INTENSITY",
    "LYSO COUNT",
}
