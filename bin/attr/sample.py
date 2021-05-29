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

    def set_data_clinical(self, header, data):
        self.data_clinical.set_attr(header, data)

    def set_barcode(self, header, data):
        self.barcode_attr.set_attr(header, data)

    def set_mapping(self, header, data):
        self.mapping.set_attr(header, data)

    def set_fastqs(self, sample_id, fastqs):
        self.fastqs_attr.set_attr(sample_id, fastqs)

    def complete_sample(self):
        # assignment from data clinical
        self.patient_id = self.data_clinical.patient_id
        self.collab_id = self.data_clinical.collab_id
        self.sample_type = self.data_clinical.sample_type
        self.gene_panel = self.data_clinical.gene_panel
        self.cancer_type = self.data_clinical.cancer_type
        self.sample_class = self.data_clinical.sample_class
        self.specimen_preservation_type = self.data_clinical.specimen_preservation_type
        self.sex = self.data_clinical.sex
        self.tissue_site = self.data_clinical.tissue_site
        # assignment from mapping file
        self.run_id = self.mapping.run_id
        self.fcid = self.mapping.fcid
        # assignment from barcode
        self.barcode = self.barcode_attr.barcode
        # assignment of fastqs
        self.fastqs = self.fastqs_attr.paths
