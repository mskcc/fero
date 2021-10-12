#
# Converts mapping files to production paths
#
# Uses convert_dmplibs.py and convert_ifs_archive.py
#

import sys, os
import convert_dmplibs as dmp
import convert_ifs_archive as ifs


def convert_sample_name(s,r,p):
    # Mimics behavior in .bin.project
    pn_sample_id = s + "_" + r
    preservation = "FROZEN"
    if "ffpe" in s.lower():
        preservation = "FFPE"
    if len(pn_sample_id) > 32:
        pn_sample_id = "PN_{p}_{r}".format(
                p = preservation,
                r = r
                )
    return pn_sample_id


if __name__ == '__main__':
    fname = sys.argv[1]
    request_id = sys.argv[2]
    with open(fname, 'r') as f:
        for line in f:
            tab = line.split("\t")
            fpath = tab[3]
            sample_name = convert_sample_name(tab[1], request_id)
            s = "\t".join(tab[0:3])
            path_ifs = False
            if ifs.validate_path(fpath):
                path_ifs = True
            if path_ifs:
                path = ifs.convert_to_juno_path(fpath)
            else:
                path = dmp.convert_str(fpath)
            if path:
                print(s + "\t" + path + "\tPE") #PE is always at the end of mapping file
