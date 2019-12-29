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

# Variables to be rounded after transformation
DISCRETE_VARIABLES = {
    "ER COUNT",
    "LYSO COUNT",
    "TMRE COUNT",
    "MITO COUNT",
    "CELL END NODES",
    "CELL CROSSING POINTS",
    "CELL BRANCH NODES",
    "Order",
    "Passage"
}
