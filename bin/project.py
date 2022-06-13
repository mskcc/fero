from .attr.request import RequestAttr
from .samples import SamplesObj
from .helpers import process_request_file


class ProjectObj:
    def __init__(
        self, request_file, patient_file, pairing_file, mapping_file, data_clinical, barcode_file
    ):
        self.request_file = request_file
        self.patient_file = patient_file
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
            self.patient_file, self.mapping_file, self.data_clinical, self.barcode_file
        )


    def generate_metadata_json(self, labhead_pi_email = "solitd@mskcc.org"):
        metadata = dict()
        request_metadata = self.request.metadata
        request_id = request_metadata['igoRequestId']
        recipe = request_metadata['genePanel']
        if not request_metadata['labHeadEmail']:
            request_metadata['labHeadEmail'] = labhead_pi_email
        if not request_metadata['piEmail']:
            request_metadata['piEmail'] = labhead_pi_email
        for sample_id in self.samples.data:
            sample = self.samples.data[sample_id]
            sample_metadata = sample.metadata
            # gotta reformat the sample names because pool normal names are too generic
            # and can span multiple projects
            if 'pool' in sample_id.lower():
                pooled_normal_sample_id = self._generate_pooled_normal_id(sample_id, request_id, sample_metadata)
                sample_metadata['sampleId'] = pooled_normal_sample_id
                sample_metadata['sampleName'] = pooled_normal_sample_id
                sample_metadata['ciTag'] = pooled_normal_sample_id
                sample_metadata['cmoSampleName'] = pooled_normal_sample_id
                sample_metadata['patientId'] = "pooled_normal_patient_id"
            if sample.fastqs:
                for i,fastq in enumerate(sample.fastqs):
                    if "R1" in fastq:
                        sample_metadata['R'] = 'R1'
                    else:
                        sample_metadata['R'] = 'R2'
                    metadata[fastq] = {**request_metadata, **sample_metadata}
                    run_id = sample.fastqs_attr.run_id[i]
                    fcid = sample.fastqs_attr.fcid[i]
                    metadata[fastq]["runId"] = run_id 
                    metadata[fastq]["flowCellid"] = fcid
            if sample.bam.path:
                metadata[sample.bam.path] = {**request_metadata, **sample_metadata}
        return metadata


    def generate_file_manifest(self):
        paths = list()
        for sample_id in self.samples.data:
            sample = self.samples.data[sample_id]
            if sample.fastqs:
                for fastq in sample.fastqs:
                    paths.append(fastq)
            if sample.bam.path:
                paths.append(sample.bam.path)
        return paths


    def _generate_pooled_normal_id(self, sample_id, request_id, sample_metadata):
        pooled_normal_sample_id = sample_id + "_" + request_id
        if len(pooled_normal_sample_id) > 32:
            pooled_normal_sample_id = "PN_{preservation}_{request_id}".format(
                    preservation = sample_metadata['preservation'],
                    request_id = request_id
                    )
        return pooled_normal_sample_id
