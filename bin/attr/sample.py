from .data_clinical import DataClinicalAttr
from .barcode import BarcodeAttr
from .mapping import MappingAttr
from .fastqs import FastqsAttr

class SampleAttr:
    def __init__(self, sample_id):
        self.sample_id = sample_id
        self.data_clinical = DataClinicalAttr()
        self.barcode_attr = BarcodeAttr()
        self.mapping = MappingAttr()
        self.fastqs_attr = FastqsAttr()
        self.metadata = dict()

    def set_data_clinical(self, header, data):
        self.data_clinical.set_attr(header, data)

    def set_barcode(self, header, data):
        self.barcode_attr.set_attr(header, data)

    def set_mapping(self, header, data):
        self.mapping.set_attr(header, data)

    def set_fastqs(self, sample_id, fastqs):
        self.fastqs_attr.set_attr(sample_id, fastqs)
        self.fastqs = self.fastqs_attr.paths

    def complete_sample(self):
        # assignment from data clinical
        self.metadata['sampleName'] = self.sample_id
        self.metadata['cmoSampleName'] = self.sample_id
        self.metadata["patientId"] = self.data_clinical.patient_id
        self.metadata["sampleId"] = self.data_clinical.collab_id
        self.metadata["investigatorSampleId"] = self.data_clinical.collab_id
        self.metadata["externalSampleId"] = self.data_clinical.collab_id
        self.metadata["sampleClass"] = self.data_clinical.sample_type

        self.metadata["recipe"] = self.data_clinical.gene_panel
        self.metadata["oncoTreeCode"] = self.data_clinical.cancer_type
        self.metadata["sampleClass"] = self.data_clinical.sample_class
        self.metadata["preservation"] = self.data_clinical.specimen_preservation_type
        self.metadata["sex"] = self.data_clinical.sex
        self.metadata["tissueLocation"] = self.data_clinical.tissue_site
        # assignment from mapping file
        self.metadata["runId"] = self.mapping.run_id
        self.metadata["flowCellId"] = self.mapping.fcid
        # assignment from barcode
        self.metadata["barcodeIndex"] = self.barcode_attr.barcode
        if 'normal' in self.metadata['sampleClass'].lower():
            self.metadata["tumorOrNormal"] = "Normal"
        else:
            self.metadata["tumorOrNormal"] = 'Tumor'
