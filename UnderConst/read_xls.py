## List all .txt files in a specified directory + subdirectories. 

import os

path = 'c:\\projects\\hc2\\'

files = []
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        if '.txt' in file:
            files.append(os.path.join(r, file))

for f in files:
    print(f)


## List all directories in a specified directory + subdirectories.

import os

path = 'c:\\projects\\hc2\\'

folders = []

# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for folder in d:
        folders.append(os.path.join(r, folder))

for f in folders:
    print(f)