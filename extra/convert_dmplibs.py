import sys, os


BAM_JUNO = os.environ["BAM_JUNO"]


def convert_str(s):
    fpath_split = s.split(os.sep)
    end_dir = fpath_split[len(fpath_split)-1]
    path_converted = gen_path(end_dir)
    return path_converted


def gen_path(end_dir):
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
        print("Unexpected format:", end_dir)


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
