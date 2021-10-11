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
    fname = sys.argv[1]
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
                        dest = PATH_FASTQ + subdir + os.sep
                        os.makedirs(os.path.dirname(dest), exist_ok=True)
                        print("Copying from %s -> %s" % (path, dest))
                        shutil.copy(path, dest)
            else: # is dmp bam
                try:
                    bam_file = dmp.convert_str(fpath)
                    cmoid = dmp.retrieve_cmoid_from_path(fpath)
                    dest = PATH_BAM + cmoid + ".bam"
                    print("Copying from %s -> %s" % (bam_file, dest))
                    shutil.copy(bam_file, dest)
                except FileNotFoundError:
                    print("File not found, failed to transfer", bam_file, "to", dest)
