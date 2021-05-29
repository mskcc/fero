from .helpers import (
    process_mapping_file,
    process_data_clinical_file,
    process_barcode_file,
)
from .attr.sample import SampleAttr
from .attr.data_clinical import DataClinicalAttr


class SamplesObj:
    def __init__(self, mapping_file, data_clinical_file, barcode_file):
        self.header_mf, self.data_mf, self.fastqs = process_mapping_file(mapping_file)
        self.header_dc, self.data_dc = process_data_clinical_file(data_clinical_file)
        self.header_bc, self.data_bc = process_barcode_file(barcode_file)
        self.sample_ids = set()
        self._set_sample_ids()
        self.data = dict()
        for sample_id in self.sample_ids:
            self.data[sample_id] = SampleAttr(sample_id)
        self._assign_sample_data()

    def _set_sample_ids(self):
        """
        Get sample ids from mapping file
        """
        for i in self.data_mf:
            self.sample_ids.add(i["SAMPLE_ID"])

    def _assign_sample_data(self):
        for i in self.data_dc:
            sample_id = i['SAMPLE_ID']
            self.data[sample_id].set_data_clinical(self.header_dc, i)
        for i in self.data_bc:
            sample_id = i['SAMPLE_ID']
            self.data[sample_id].set_barcode(self.header_bc, i)
        for i in self.data_mf:
            sample_id = i['SAMPLE_ID']
            self.data[sample_id].set_mapping(self.header_mf, i)
        for sample_id in self.fastqs:
            self.data[sample_id].set_fastqs(sample_id, self.fastqs[sample_id])
        for sample_id in self.sample_ids:
            self.data[sample_id].complete_sample()
