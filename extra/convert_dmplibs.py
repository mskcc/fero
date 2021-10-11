#
# This is needed if legacy bam files are located in a directory other than
# what's used in current processes
#
# PATH_BAM is the EXPECTED location of the bam files, typically in /juno/res
#

import sys, os
import requests
from access_beagle_endpoint import AccessBeagleEndpoint


ENDPOINT = AccessBeagleEndpoint()
BAM_JUNO = os.environ["BAM_JUNO"]
PATH_BAM = os.environ["PATH_BAM"]
LOG = open('dmp_convert_err.txt', 'a')


def convert_line(line):
    tab = line.split("\t")
    dmp_path = tab[3]
    return 


def convert_str(s):
    sample_id = retrieve_cmoid_from_path(s)
    fpath_split = s.split(os.sep)
    end_dir = fpath_split[len(fpath_split)-1]
    path_converted = gen_path(end_dir, sample_id)
    return path_converted


# input bam path
def get_juno_bam_location(s):
    fpath_split = s.split(os.sep)
    end_dir = fpath_split[len(fpath_split)-1]
    try:
        if not check_sample_dir(end_dir):
            raise TypeError
        sample_name = end_dir.split("_")[1]
        new_path = os.path.join(BAM_JUNO,
                sample_name[0],
                sample_name[1],
                sample_name) + ".bam"
        return(new_path)
    except TypeError:
        LOG.write("Unexpected format: %s\n" % end_dir)


def get_sample_id(s):
    fpath_split = s.split(os.sep)
    end_dir = fpath_split[len(fpath_split)-1]
    sample_id = fpath_split[-1].replace("Sample_","")   
    return sample_id


def retrieve_cmoid_from_path(fpath):
    sample_id = get_sample_id(fpath)
    try:
        cmoid = ENDPOINT.get_cmoid(sample_id)
        return cmoid
    except:
        LOG.write("Error converting from %s\n" % sample_id)


# outgoing bam path
def gen_path(end_dir, new_sample_name):
    try:
        if not check_sample_dir(end_dir):
            raise TypeError
        sample_name = end_dir.split("_")[1]
        new_path = os.path.join(PATH_BAM,
                new_sample_name) + ".bam"
        return(new_path)
    except TypeError:
        LOG.write("Unexpected format: %s\n" % end_dir)


def check_sample_dir(p):
    if "Sample_" in p:
        return True
    return False


if __name__ == '__main__':
    fname = sys.argv[1]
    with open(fname) as f:
        for line in f:
            tab = line.split("\t")
            dmp_path = tab[3]
            print("\t".join(tab[0:2]) + "\t" +  convert_str(dmp_path))
