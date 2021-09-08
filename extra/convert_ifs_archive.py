#
# This is required if legacy mapping files are not located in /igo/delivery
#
# ARCHIVE_IGO is typically /igo/delivery, the new fastqs delivery directory
#
# ARCHIVE_IFS is typically /ifs/archive/..., the location of old legacy fastq delivery files
#
# ARCHIVE_JUNO is typically the manual

import sys, os

ARCHIVE_IGO=os.environ['ARCHIVE_IGO']
ARCHIVE_IFS=os.environ['ARCHIVE_IFS']
PATH_FASTQ=os.environ['PATH_FASTQ']

def convert_str(s):
    try:
        if not validate_path(s):
            raise TypeError
        return s.replace(ARCHIVE_IFS, ARCHIVE_IGO)
    except TypeError:
        print("Not a valid path", s)

def convert_to_juno_path(s):
    try:
        if not validate_path(s):
            raise TypeError
        folder = s.split(os.sep)[-1]
        return PATH_FASTQ + folder
    except TypeError:
        print("Not a valid path", s)

def validate_path(p):
    if ARCHIVE_IFS in p:
        return True
    return False

if __name__ == '__main__':
    fname = sys.argv[1]
    with open(fname, 'r') as f:
        for line in f:
            fpath = line.split("\t")[3]
            print(convert_str(fpath))
