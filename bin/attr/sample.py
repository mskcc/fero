from .data_clinical import DataClinicalAttr
from .barcode import BarcodeAttr
from .mapping import MappingAttr
from .fastqs import FastqsAttr

class SampleAttr:
    def __init__(self, sample_id):
        self.sample_id = sample_id
        self.data_clinical = DataClinicalAttr()
        self.barcode = BarcodeAttr()
        self.mapping = MappingAttr()
        self.fastqs = FastqsAttr()

    def set_data_clinical(self, header, data):
        self.data_clinical.set_attr(header, data)

    def set_barcode(self, header, data):
        self.barcode.set_attr(header, data)

    def set_mapping(self, header, data):
        self.mapping.set_attr(header, data)

    def set_fastqs(self, sample_id, fastqs):
        self.fastqs.set_attr(sample_id, fastqs)
