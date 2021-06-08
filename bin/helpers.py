import csv
import os
from json import JSONEncoder

def read_csv(fpath, delim="\t"):
    f = open(fpath, "r")
    reader = csv.reader(f, delimiter=delim)
    return reader


def process_request_file(fpath):
    csv_reader = read_csv(fpath, ":")
    d = dict()
    keys = list()
    for i, line in enumerate(csv_reader):
        heading = line[0]
        value = " ".join(line[1:]).lstrip()
        d[heading] = value
        keys.append(heading)
    return keys, d


def process_barcode_file(fpath):
    csv_reader = read_csv(fpath)
    l = list()
    header = ["SAMPLE_ID", "BARCODE_INDEX"]
    for line in csv_reader:
        sample_id = line[0]
        barcode = line[1]
        l.append({"SAMPLE_ID": sample_id, "BARCODE_INDEX": barcode})
    return header, l


def process_patient_file(fpath):
    csv_reader = read_csv(fpath)
    next(csv_reader)
    data = list()
    header = ["POOL", "SAMPLE_ID", "COLLAB_ID", "PATIENT_ID", "CLASS", "SAMPLE_TYPE",
            "INPUT_NG", "LIBRARY_YIELD", "POOL_INPUT", "BAIT_VERSION", "SEX"]
    for line in csv_reader:
        d = dict()
        for j, value in enumerate(line):
            d[header[j]] = value
        data.append(d)
    return header, data


def process_mapping_file(fpath):
    """
    fastq_paths return dict of list if files per sample
                fastq_paths[SAMPLE_ID] = [ R1_1, R2_1, R1_2, R2_2,... ]
    """
    csv_reader = read_csv(fpath)
    header = ["_1_col", "SAMPLE_ID", "RUNID_FLOWCELLID", "FILEPATH", "PE"]
    data = list()
    fastq_paths = dict()
    for line in csv_reader:
        d = dict()
        for j, value in enumerate(line):
            d[header[j]] = value
        data.append(d)
    for row in data:
        sample_id = row["SAMPLE_ID"]
        fpath = row["FILEPATH"]
        if sample_id not in fastq_paths:
            fastq_paths[sample_id] = get_files_from_dir(fpath)
        else:
            print("SAMPLE_ID %s not unique; check mapping file" % sample_id)
            sys.exit(1)
    return header, data, fastq_paths


def get_files_from_dir(dirpath):
    """
    Look for fastqs (files ending in "fastq.gz" in dirpath)
    """
    fastqs = list()
    for f in os.listdir(dirpath):
        if f.endswith(".fastq.gz"):
            fastqs.append(os.path.join(dirpath, f))
    return fastqs


def process_pairing_file(fpath):
    csv_reader = read_csv(fpath)
    header = ["NORMAL", "TUMOR"]
    data = list()
    for line in csv_reader:
        d = dict()
        for j, value in enumerate(line):
            d[header[j]] = value
        data.append(d)
    return header, data


def process_data_clinical_file(fpath):
    csv_reader = read_csv(fpath)
    data = list()
    for i, line in enumerate(csv_reader):
        if i == 0:
            header = line
        else:
            d = dict()
            for j, value in enumerate(line):
                d[header[j]] = value
            data.append(d)
    return header, data

class MetadataEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
