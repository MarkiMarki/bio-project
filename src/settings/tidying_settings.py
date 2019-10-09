import numpy as np

COLUMN_RENAME_MAPPER = {
        'Unnamed: 0': 'Condition',
        'Unnamed: 1': 'Patient',
        ' ': 'Row',
        ' .1': 'Col'
    }
SERPENT_ORDERED_ITERATOR = []
for row in 'BCDEFG':
    sqn = list(np.arange(2, 12))
    if row in 'CEF': sqn.reverse()
    for col in sqn:
        SERPENT_ORDERED_ITERATOR += [(row, col)]