import sys, os


def spoof_barcode(sample_run_id):
    if sample_run_id == 'DMPLibs':
        return "dmpbc"
    return "fakebc"


if __name__ == '__main__':
    fname = sys.argv[1]
    with open(fname, 'r') as f:
        for line in f:
            tab = line.split("\t")
            sample_id = tab[1]
            sample_run_id = tab[2]
            bc = spoof_barcode(sample_run_id)
            print(sample_id + "\t" + bc)
