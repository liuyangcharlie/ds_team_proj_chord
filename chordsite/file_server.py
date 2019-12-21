import os
import csv
from collections import defaultdict

# record file version
global file_version_map
file_version_map = {}
global filename_lock_map
filename_lock_map = []
global client_waitinglist
client_waitinglist = defaultdict(list)

def replicate(filename):
    file = open(filename, 'r')
    content = file.read()
    file.close()

def file_operation(filename, RW, content):
    if RW is 'r':
        file_read(filename)
    elif RW is 'rw':
        file_write(filename, content)

def file_read(filename):
    try:
        file = open(filename, 'r')
        # read file content into a string
        file_content = file.read()
        if filename not in file_version_map:
            file_version_map[filename] = 0
        return (file_content, file_version_map[filename])
    except IOError:
        print(filename, ' does not exist in directory')
        return (IOError, -1)
        pass

def file_write(filename, content):
    if filename not in file_version_map:
        file_version_map[filename] = 0
    else:
        file_version_map[filename] = file_version_map[filename] + 1
        print("Updated ", filename, " to version ", str(file_version_map[filename]))

    file = open(filename, 'rw')
    file.write(content)

    print("FILE_VERSION: " + str(file_version_map[filename]))
    return ("Success write", file_version_map[filename])

def lock_check(filename):
    if filename in filename_lock_map:
        # if this file is unlocked
        if filename_lock_map[filename] == 0:
            return False
        else:
            return True
    else:
        filename_lock_map[filename] == 0
        return False

def client_waitinglist_check(filename):
    if len(client_waitinglist[filename]) == 0:
        filename_lock_map[filename] = 1
        print("")

def directory_file(filename, id):
    # open the .csv file storing the mappings
    with open("file_mappings.csv", 'rt') as dicfile:
        dicfile = csv.DictReader(dicfile, delimiter = ',')
        header = dicfile.fieldnames
        file_row = ""
        for row in dicfile:
            
