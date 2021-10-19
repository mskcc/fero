#
# Converts mapping files to production paths
#
# Uses convert_dmplibs.py and convert_ifs_archive.py
#

import sys, os
import convert_dmplibs as dmp
import convert_ifs_archive as ifs


def convert_sample_name(s,r):
    # Mimics behavior in .bin.project
    if "pool" in s.lower():
        pn_sample_id = s + "_" + r
        if "ffpe" in s.lower():
            preservation = "FFPE"
        elif "frozen" in s.lower():
            preservation = "FROZEN"
        else:
            preservation = "UNK" # unkown
        if len(pn_sample_id) > 32:
            pn_sample_id = "PN_{p}_{r}".format(
                    p = preservation,
                    r = r
                    )
        return pn_sample_id
    else:
        return s


if __name__ == '__main__':
    fname = sys.argv[1]
    request_id = sys.argv[2]
    with open(fname, 'r') as f:
        for line in f:
            tab = line.split("\t")
            fpath = tab[3]
            sample_name = convert_sample_name(tab[1], request_id)
            s = "\t".join([tab[0], sample_name, tab[2]])
            path_ifs = False
            if ifs.validate_path(fpath):
                path_ifs = True
            if path_ifs:
                path = ifs.convert_to_juno_path(fpath) + os.sep + request_id
            else:
                fpath_split = fpath.split(os.sep)
                end_dir = fpath_split[len(fpath_split)-1]
                path = dmp.gen_path_w_req(end_dir, request_id, sample_name)
            if path:
                print(s + "\t" + path + "\tPE") #PE is always at the end of mapping file
