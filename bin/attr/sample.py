from .patient import PatientAttr
from .data_clinical import DataClinicalAttr
from .barcode import BarcodeAttr
from .mapping import MappingAttr
from .fastqs import FastqsAttr
from .bam import BamAttr


class SampleAttr:
    def __init__(self, sample_id):
        self.sample_id = sample_id
        self.patient = PatientAttr()
        self.data_clinical = DataClinicalAttr()
        self.barcode_attr = BarcodeAttr()
        self.fastqs_attr = FastqsAttr()
        self.bam = BamAttr()
        self.metadata = dict()
        # instantiating default fields
        self._init_metadata_fields()
        self.library_id = ""
        self.sequencing_center = "GCL@MSK"
        self.igocomplete = True
        self.platform = "Illumina"
        self.sample_origin = "Unknown"
        self.flow_cell_lanes = []

    def set_patient(self, header, data):
        self.patient.set_attr(header, data)

    def set_data_clinical(self, header, data):
        self.data_clinical.set_attr(header, data)

    def set_barcode(self, header, data):
        self.barcode_attr.set_attr(header, data)

    def set_fastqs(self, sample_id, fastqs, data):
        self.fastqs_attr.set_attr(sample_id, fastqs, data)
        self.fastqs = self.fastqs_attr.paths

    def set_bam(self, sample_id, bam):
        self.bam.set_attr(sample_id, bam)

    def complete_sample(self):
        """
        The metadata field names don't always match up
        with the metadata field names in beagle/argos;
        contact CMO Informatics if there are questions

        sampleId for example is usually igoId

        runid/fcid are fastq attributes
        """
        # assign default fields
        self.metadata["libraryIgoId"] = self.library_id
        self.metadata["sequencingCenter"] = self.sequencing_center
        self.metadata["platform"] = self.platform
        self.metadata["sampleOrigin"] = self.sample_origin
        self.metadata["flowCellLanes"] = self.flow_cell_lanes
        self.metadata["igocomplete"] = self.igocomplete
        self.metadata["igoComplete"] = self.igocomplete

        # assignment from patient
        self.metadata["sampleId"] = self.patient.collab_id
        self.metadata["cmoPatientId"] = self.patient.patient_id
        self.metadata["baitSet"] = self.patient.bait_version
        p_sample_class = self.patient.sample_class.lower()
        if "normal" in p_sample_class:
            self.metadata["tumorOrNormal"] = "Normal"
        else:
            self.metadata["tumorOrNormal"] = "Tumor"
        self.metadata["sampleType"] = self.metadata["tumorOrNormal"]
        self.metadata["sampleClass"] = self.metadata["tumorOrNormal"]
        self.metadata["sex"] = self.patient.sex
        self.metadata["preservation"] = self.patient.sample_type

        # assignment from data clinical
        self.metadata["cmoSampleName"] = self.sample_id
        self.metadata["ciTag"] = self.sample_id
        self.metadata["primaryId"] = self.sample_id # assigning primaryId same as ciTag
        self.metadata["sampleName"] = self.data_clinical.collab_id
        self.metadata["oncoTreeCode"] = self.data_clinical.oncotree_code
        self.metadata["tissueLocation"] = self.data_clinical.tissue_site

        # assignment from barcode
        self.metadata["barcodeIndex"] = self.barcode_attr.barcode

        # assignment of sampleAliases
        aliases = list()
        aliases.append(
                {
                    "value": self.data_clinical.collab_id,
                    "namespace": "investigatorId"
                    }
                )
        aliases.append(
                {
                    "value": self.sample_id,
                    "namespace": "igoId"
                    }
                )
        self.metadata["sampleAliases"] = aliases

        self.validate_metadata()

    def validate_metadata(self):
        if not self.metadata["oncoTreeCode"]:
            print("MISSING ONCOTREECODE FOR {sample_id}.".format(
                    sample_id = self.sample_id
                    )
                )

    def _init_metadata_fields(self):
        metadata_fields = [
            "libraryIgoId",
            "sequencingCenter",
            "platform",
            "sampleOrigin",
            "flowCellLanes",
            "igocomplete",
            "igoComplete",
            "cmoPatientId",
            "baitSet",
            "tumorOrNormal",
            "sampleClass",
            "sex",
            "preservation",
            "sampleName",
            "cmoSampleName",
            "sampleId",
            "investigatorSampleId",
            "sampleType",
            "oncotreeCode",
            "tissueLocation",
            "runId",
            "flowCellId",
            "barcodeIndex",
            "R",
            "sampleAliases"
        ]
        for i in metadata_fields:
            self.metadata[i] = ""

    def get_preservation_from_fastqs(self):
        for f in self.fastqs:
            if "ffpe" in f.lower():
                return "FFPE"
            else:
                return "Frozen"
