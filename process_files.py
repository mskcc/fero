from configparser import SafeConfigParser
import csv
from pprint import pprint
import os
from bin.project import ProjectObj

if __name__ == "__main__":
    parser = SafeConfigParser()
    parser.read("config.ini")

    request_file = parser.get("DATA", "RequestFile")
    data_clinical_file = parser.get("DATA", "DataClinicalFile")
    mapping_file = parser.get("DATA", "MappingFile")
    pairing_file = parser.get("DATA", "PairingFile")
    barcode_file = parser.get("DATA", "BarcodeFile")

    project_obj = ProjectObj(request_file, pairing_file, mapping_file, data_clinical_file, barcode_file)
