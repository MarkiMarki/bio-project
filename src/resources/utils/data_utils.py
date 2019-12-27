import re

import numpy as np


# Create a new directory in a given path
def mkdir_p(mypath):
    """Creates a directory. equivalent to using mkdir -p on the command line"""

    from errno import EEXIST
    from os import makedirs, path

    try:
        makedirs(mypath)
    except OSError as exc:  # Python >2.5
        if exc.errno == EEXIST and path.isdir(mypath):
            pass
        else:
            raise


# Returning the indexed number from a string
@np.vectorize
def get_ith_number(input_string, i):
    try:
        return str(re.findall(r'\d+', input_string)[i])
    except TypeError:
        print("Field was not a string")

# Checks if file exists in given path
def does_file_exist(path):
    try:
        f = open(path)
        return True
    except IOError:
        return False
