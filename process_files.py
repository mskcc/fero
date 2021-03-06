from configparser import ConfigParser
import csv
import os
import sys
import json
from pprint import pprint
from bin.project import ProjectObj


def make_run_command(fpath, file_group, json_out_path):
    cmd = "beaglecli files create" \
          " {fpath}" \
          " fastq" \
          " {file_group}" \
          "  --metadata-path={json_out_path}\n".format(
                fpath=fpath,
                file_group=file_group,
                json_out_path=json_out_path
                )
    return cmd

def create_pairing_json(pairing_file, pairing_config):
    json_data = dict()
    json_data['pairs'] = list()
    with open(pairing_file, 'r') as pair_file:
        for line in pair_file:
            tab = line.strip().split("\t")
            normal_sample_id = tab[0]
            if "pool" in normal_sample_id.lower(): # hack so that the pooled normal ids are made unique
                normal = dict(sample_id = normal_sample_id + "_" + pairing_config['request_id'])
            else:
                normal = dict(sample_id = normal_sample_id)
            tumor = dict(sample_id =tab[1])
            json_data['pairs'].append(dict(tumor= tumor, normal= normal))
        json_data['pipelines'] = pairing_config['pipelines']
        json_data['pipeline_versions'] = pairing_config['pipeline_versions']
        json_data['name'] = pairing_config['name']
        json_data['output_directory_prefix'] = pairing_config['output_directory_prefix']
        json_data['labHeadName'] = pairing_config['labHeadName']
        json_data['assay'] = pairing_config['assay']
        json_data['investigatorName'] = pairing_config['investigatorName']
    return json_data

if __name__ == "__main__":
    parser = ConfigParser()
    try:
        sys.argv[1]
        parser.read(sys.argv[1])
    except:
        parser.read("config.ini")

    request_file = parser.get("DATA", "RequestFile")
    data_clinical_file = parser.get("DATA", "DataClinicalFile")
    mapping_file = parser.get("DATA", "MappingFile")
    pairing_file = parser.get("DATA", "PairingFile")
    patient_file = parser.get("DATA", "PatientFile")
    barcode_file = parser.get("DATA", "BarcodeFile")
    import_file_group = parser.get("BEAGLE_CONFIG", "ImportFileGroup")
    pipelines = parser.get("PAIR_CONFIG", "Pipelines")
    pipeline_versions = parser.get("PAIR_CONFIG", "PipelineVersions")
    name = parser.get("PAIR_CONFIG", "RunName")
    output_directory_prefix = parser.get("PAIR_CONFIG", "OutputDirPrefix")
    lab_head_name = parser.get("PAIR_CONFIG", "LabHeadName")
    lab_head_pi_email = parser.get("PAIR_CONFIG", "LabHeadEmail")
    investigator_name = parser.get("PAIR_CONFIG", "InvestigatorName")
    assay = parser.get("PAIR_CONFIG", "Assay")

    project_obj = ProjectObj(request_file, patient_file, pairing_file, mapping_file, data_clinical_file, barcode_file)

    file_metadata = project_obj.generate_metadata_json(lab_head_pi_email)
    cmd = ""

    # make metadata jsons for each file
    try:
        json_path = parser.get("METADATA_CONFIG", "MetadataOutputDir")
    except:
        json_path = 'metadata_jsons'
    if not os.path.exists(json_path):
        os.makedirs(json_path)
    for fpath in file_metadata:
        metadata = file_metadata[fpath]
        json_out_path = os.path.join(json_path,os.path.basename(fpath) + ".json")
        json_file = open(json_out_path, 'w')
        json.dump(metadata, json_file)
        cmd += make_run_command(fpath, import_file_group, json_out_path)

    print("\nWriting beagle command script upload.sh...")
    open("upload.sh", 'w').write(cmd)
    pairing_config = dict()
    request_id = project_obj.request.request_id # hack
    pairing_config['request_id'] = request_id
    pairing_config["pipelines"] = [pipelines]
    pairing_config["pipeline_versions"] = [pipeline_versions]
    pairing_config["name"] = name
    pairing_config["output_directory_prefix"] = output_directory_prefix
    pairing_config['labHeadName'] = lab_head_name
    pairing_config['assay'] = assay
    pairing_config['investigatorName'] = investigator_name
    pairing = create_pairing_json(pairing_file, pairing_config)
    try:
        pairing_json = parser.get("METADATA_CONFIG", "OutputJsonFileName")
    except:
        pairing_json = "pairing.json"
    print("\nWriting {pairing_json} file to submit to Voyager...".format(pairing_json=pairing_json))
    json.dump(pairing, open(pairing_json, 'w'))

    print("\nWriting file manifest.txt...")
    file_manifest = project_obj.generate_file_manifest()
    with open("file_manifest.txt", 'w') as fm:
        for line in file_manifest:
            fm.write(line + "\n")

