import os
# record file version
file_version_map = {}

def replicate(filename):
    file = open(filename, 'r')
    content = file.read()
    file.close()

def file_operation(filename, RW, content, file_version_map):
    if RW is 'r':
        file_read(filename, file_version_map)
    elif RW is 'rw':
        file_write(filename, file_version_map, content)

def file_read(filename, file_version_map):
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

def file_write(filename, file_version_map, content):
    if filename not in file_version_map:
        file_version_map[filename] = 0
    else:
        file_version_map[filename] = file_version_map[filename] + 1
        print("Updated ", filename, " to version ", str(file_version_map[filename]))

    file = open(filename, 'rw')
    file.write(content)

    print("FILE_VERSION: " + str(file_version_map[filename]))
    return ("Success write", file_version_map[filename])
