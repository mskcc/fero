class DataClinicalAttr:
   def __init__(self):
        self.sample_id = ""
        self.patient_id = ""
        self.collab_id = ""
        self.sample_type = ""
        self.gene_panel = ""
        self.cancer_type = ""
        self.sample_class = ""
        self.specimen_preservation_type = ""
        self.sex = ""
        self.tissue_site = ""

   def set_attr(self, keys, data):
        """
            data    dictionary containing one sample
                    from data clinical file
        """
        keys_lower = [i.lower() for i in keys]
        for i,key in enumerate(keys_lower):
            val = data[keys[i]]
            if key == "sample_id":
                 self.sample_id = val
            if key == "patient_id":
                 self.patient_id = val
            if key == "collab_id":
                 self.collab_id = val
            if key == "sample_type":
                 self.sample_type = val
            if key == "gene_panel":
                 self.gene_panel = val
            if key == "cancer_type":
                 self.cancer_type = val
            if key == "sample_class":
                 self.sample_class = val
            if key == "specimen_preservation_type":
                 self.specimen_preservation_type = val
            if key == "sex":
                 self.sex = val
            if key == "tissue_site":
                 self.tissue_site = val

   def __repr__(self):
       return "Data Clinical {sample_id}: {patient_id}, {sample_class}".format(
               sample_id = self.sample_id,
               patient_id = self.patient_id,
               sample_class = self.sample_class)
