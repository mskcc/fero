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
