from configparser import SafeConfigParser
import csv
from pprint import pprint
import os



def read_csv(fpath, delim="\t"):
    f = open(fpath, "r")
    reader = csv.reader(f, delimiter=delim)
    return reader


def process_request_file(fpath):
    csv_reader = read_csv(fpath, ":")
    d = dict()
    for i, line in enumerate(csv_reader):
        heading = line[0]
        value = " ".join(line[1:]).lstrip()
        d[heading] = value
    return d


def process_barcode_file(fpath):
    csv_reader = read_csv(fpath)
    l = list()
    header = ["SAMPLE_ID", "BARCODE_INDEX"]
    for line in csv_reader:
        sample_id = line[0]
        barcode = line[1]
        l.append({sample_id: barcode})
    return header, l

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
            fastqs.append(os.path.join(dirpath,f))
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


if __name__ == "__main__":
    parser = SafeConfigParser()
    parser.read("config.ini")

    request_file = parser.get("DATA", "RequestFile")
    data_clinical_file = parser.get("DATA", "DataClinicalFile")
    mapping_file = parser.get("DATA", "MappingFile")
    pairing_file = parser.get("DATA", "PairingFile")
    barcode_file = parser.get("DATA", "BarcodeFile")

    # reading in data
    header_pf, data_pf = process_pairing_file(pairing_file)
    header_mf, data_mf, fastq_paths = process_mapping_file(mapping_file)
    header_dc, data_dc = process_data_clinical_file(data_clinical_file)
    header_bc, data_bc = process_barcode_file(barcode_file)
    data_rf = process_request_file(request_file)
