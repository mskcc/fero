from .attr.request import RequestAttr
from .samples import SamplesObj
from .helpers import process_request_file


class ProjectObj:
    def __init__(
        self, request_file, pairing_file, mapping_file, data_clinical, barcode_file
    ):
        self.request_file = request_file
        self.pairing_file = pairing_file
        self.mapping_file = mapping_file
        self.data_clinical = data_clinical
        self.barcode_file = barcode_file
        self._set_request()
        self._set_samples()

    def _set_request(self):
        header, data = process_request_file(self.request_file)
        self.request = RequestAttr()
        self.request.set_attr(header, data)
        self.request.set_metadata()

    def _set_samples(self):
        self.samples = SamplesObj(
            self.mapping_file, self.data_clinical, self.barcode_file
        )


    def generate_metadata_json(self):
        metadata = dict()
        request_metadata = self.request.metadata
        request_id = request_metadata['requestId']
        for sample_id in self.samples.data:
            sample = self.samples.data[sample_id]
            sample_metadata = sample.metadata
            if 'pool' in sample_id.lower():
                sample_metadata['sampleId'] = sample_id + "_" + request_id
                sample_metadata['sampleName'] = sample_id + "_" + request_id
                sample_metadata['cmoSampleName'] = sample_id + "_" + request_id
            for fastq in sample.fastqs:
                if "R1" in fastq:
                    sample_metadata['R'] = 'R1'
                else:
                    sample_metadata['R'] = 'R2'
                metadata[fastq] = {**request_metadata, **sample_metadata}
        return metadata
