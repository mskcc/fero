#
# Used to copy from ARCHIVE_IFS paths to PATH_FASTQ based on mapping file
#
# Requires env variables ARCHIVE_IFS, PATH_FASTQ to be defined

import sys, os
sys.path.insert(0,'..')
import convert_dmplibs as dmp
import convert_ifs_archive as ifs
from bin.helpers import get_files_from_dir
import shutil

ARCHIVE_IFS = os.environ['ARCHIVE_IFS']
PATH_FASTQ = os.environ['PATH_FASTQ']
PATH_BAM = os.environ['PATH_BAM']

if __name__ == '__main__':
    LOG = open('copy.log', 'a')
    fname = sys.argv[1]
    request_id = sys.argv[2]
    with open(fname, 'r') as f:
        for line in f:
            fpath = line.split("\t")[3]
            sample_name = line.split("\t")[1]
            if ifs.validate_path(fpath):
                igo_path = ifs.convert_str(fpath)
                igo_files = get_files_from_dir(igo_path)
                subdir = fpath.split(os.sep)[-1]
                for paths in igo_files:
                    for path in paths:
                        dest = PATH_FASTQ + subdir
                        if "pool" in dest.lower():
                            dest = dest + os.sep + request_id
                            os.makedirs(dest, exist_ok=True)
                        else:
                            os.makedirs(os.path.dirname(dest), exist_ok=True)
                        print("Copying from %s -> %s" % (path, dest))
                        shutil.copy(path, dest)
            else: # is dmp bam
                try:
                    bam_file = dmp.get_juno_bam_location(fpath)
                    dest = PATH_BAM + sample_name + ".bam"
#                    cmoid = dmp.retrieve_cmoid_from_path(fpath)
#                    dest = PATH_BAM + cmoid + ".bam"
                    print("Copying from %s -> %s" % (bam_file, dest))
                    shutil.copy(bam_file, dest)
                except FileNotFoundError:
                    s = bam_file + " not found, failed to transfer to " + dest
                    LOG.write(s + "\n")
                    print(s)
    LOG.close()
