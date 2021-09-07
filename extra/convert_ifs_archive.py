import sys, os

ARCHIVE_IGO=os.environ['ARCHIVE_IGO']
ARCHIVE_IFS=os.environ['ARCHIVE_IFS']

def convert_str(s):
    try:
        if not validate_path(s):
            raise TypeError
        return s.replace(ARCHIVE_IFS, ARCHIVE_IGO)
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
