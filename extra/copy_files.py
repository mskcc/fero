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
                        os.makedirs(os.path.dirname(dest, exist_ok=True))
                        shutil.copy(fastq, dest)
            else: # is dmp bam
                bam_file = dmp.convert_str(fpath, sample_name)
                dest = PATH_BAM + sample_name + ".bam"
                shutil.copy(bam_file, dest)