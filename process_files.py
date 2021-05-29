from configparser import SafeConfigParser
import csv
import os
import json
from pprint import pprint
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

    file_metadata = project_obj.generate_metadata_json()

    # make metadata jsons for each file
    json_path = 'metadata_jsons'
    if not os.path.exists(json_path):
        os.makedirs(json_path)
    for fpath in file_metadata:
        metadata = file_metadata[fpath]
        json_out_path = os.path.join(json_path,os.path.basename(fpath) + ".json")
        json_file = open(json_out_path, 'w')
        json.dump(metadata, json_file)
        print(fpath, os.path.abspath(json_out_path))
